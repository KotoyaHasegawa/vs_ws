#!/usr/bin/env python3
#coding: UTF-8

import matplotlib
matplotlib.use('Agg')
import rospy
import numpy as np
import cv2
import tf.transformations
import pandas as pd
import math
import time
import csv
from sensor_msgs.msg import Image

import moveit_commander
import moveit_msgs.msg
# from sensor_msgs.msg import JointState
from cv_bridge import CvBridge
import signal
import sys

import atexit

#for velocity control
from std_msgs.msg import Float64MultiArray
#for joint states servicecall
from moveit_tutorials.srv import GetCurrentJointVel
#for pose servicecall
from moveit_tutorials.srv import GettfPose
#for switch controller
from controller_manager_msgs.srv import SwitchController

from demo_data import DATA

class ServoNode:
    def __init__(self):


        self.nop = 230400
        self.pinv_int_mat_double = np.empty((6,6))
        self.pinv_int_manip = np.empty((6,6))
        self.I_dsr_vec = np.empty((self.nop, 1))
        self.lmbd = 0.05

        self.rmseth = 12.5
        self.iteration = 300

        self.threshhold_value = 128

        self.time_series = []
        self.rmse_data = []
        self.base_joint_data = []
        self.shoulder_joint_data = []
        self.elbow_joint_data = []
        self.wrist1_joint_data = []
        self.wrist2_joint_data = []
        self.wrist3_joint_data = []

        self.joint_vel_values_data = []

        self.pose_data = []
        self.dist_data = []

        self.dist_trans_x = []
        self.dist_trans_y = []
        self.dist_trans_z = []
        self.dist_rot_x = []
        self.dist_rot_y = []
        self.dist_rot_z = []

        self.error_rot_axis = []
        self.error_rot_ang = []

        self.last_msg = None

        ##moveit
        self.moveit_client = moveit_commander.MoveGroupCommander("manipulator")
        self.moveit_client.set_max_velocity_scaling_factor(value=0.2)
        self.moveit_client.set_max_acceleration_scaling_factor(value=0.2)

        # Get the current joint values and store them
        self.initial_joint_values = self.moveit_client.get_current_joint_values()
        # rospy.loginfo("Initial joint values: %s", self.initial_joint_values)

    def switch_controller(start_controllers, stop_controllers):
        switch_service = rospy.ServiceProxy('/controller_manager/switch_controller', SwitchController)
        resp = switch_service(start_controllers=start_controllers, 
                            stop_controllers=stop_controllers,
                            strictness=2,
                            start_asap=False,
                            timeout=5.0)
        print(resp.ok)

    def switch_controller(self, start_controllers, stop_controllers):
        switch_service = rospy.ServiceProxy('/controller_manager/switch_controller', SwitchController)
        resp = switch_service(start_controllers=start_controllers, 
                              stop_controllers=stop_controllers,
                              strictness=2,
                              start_asap=False,
                              timeout=5.0)
        print(resp.ok)

    def switch_to_joint_group_vel(self):
        self.switch_controller(['joint_group_vel_controller'], ['scaled_pos_joint_traj_controller'])

    def switch_to_scaled_pos(self):
        self.switch_controller(['scaled_pos_joint_traj_controller'], ['joint_group_vel_controller'])

    def readpickle(self):
        pickledata = pd.read_pickle('./pinv_int_mat_pickle/pinv_int_mat_double.pickle')
        self.pinv_int_mat_double = pickledata.values

    # def readpickle1(self):
    #     pickledata1 = pd.read_pickle('./pinv_int_mat_pickle/pinv_int_mnipulator_jac.pickle')
    #     self.pinv_int_manip = pickledata1.values

    def gen_dsrimvec(self):
        I_dsr = cv2.imread('./input_dsrim/kensyo_desired_image.png')
        I_dsr_gry = cv2.cvtColor(I_dsr, cv2.COLOR_BGR2GRAY)
        # I_dsr_gry = cv2.threshold(I_dsr_gry, self.threshhold_value, 255, cv2.THRESH_BINARY)#2values
        I_dsr_arr = np.array(I_dsr_gry, dtype = 'float64')
        self.I_dsr_vec = I_dsr_arr.reshape(-1,1)

    def read_dsrpose(self, csv_file):
        with open(csv_file, 'r') as f:
            reader = csv.reader(f)
            for row in reader:
                self.desired_pose = [float(x) for x in row]

    def euler_to_quaternion(self, eule_x, euler_y, euler_z):
        q = tf.transformations.quaternion_from_euler(eule_x, euler_y, euler_z)
        return q[0], q[1], q[2], q[3]

    def quaternion_to_euler(self, current_pose):
        e = tf.transformations.euler_from_quaternion((current_pose[0],current_pose[1],current_pose[2],current_pose[3]))
        return e[0], e[1], e[2]
    

    def ik(self, initial_joint_values, go_pose, current_euler_x, current_euler_y, current_euler_z, moveit_client):
        # Get current joint states

        
        # Create pose goal with current end effector pose
        current_pose = moveit_client.get_current_pose().pose
        current_pose.position.x = current_pose.position.x + go_pose[0]
        current_pose.position.y = current_pose.position.y + go_pose[1]
        current_pose.position.z = current_pose.position.z + go_pose[2]

        # Convert euler angles to quaternion and add to current orientation
        goal_euler = np.array([current_euler_x + go_pose[3], current_euler_y + go_pose[4], current_euler_z + go_pose[5]])
        quat = self.euler_to_quaternion(goal_euler[0], goal_euler[1], goal_euler[2])
        current_pose.orientation.x, current_pose.orientation.y, current_pose.orientation.z, current_pose.orientation.w = quat


        # 制約を定義
        constraints = moveit_msgs.msg.Constraints()
        joints_name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
        joints_goal = initial_joint_values
        tolerances_deg = [90, 120, 120, 120, 120, 120]
        tolerances = [x * np.pi / 180 for x in tolerances_deg]

        for i in range(6):
            joint_constraint = moveit_msgs.msg.JointConstraint()
            joint_constraint.joint_name = joints_name[i]
            joint_constraint.position = joints_goal[i]
            joint_constraint.tolerance_above = tolerances[i]
            joint_constraint.tolerance_below = tolerances[i]
            joint_constraint.weight = 1.0
            constraints.joint_constraints.append(joint_constraint)

        # 制約をMoveGroupに適用
        moveit_client.set_path_constraints(constraints)

        # Cartesian pathの計算
        waypoints = [current_pose]
        (plan, fraction) = moveit_client.compute_cartesian_path(waypoints, eef_step=0.008, jump_threshold=0.0)
        # プランの実行
        success = moveit_client.execute(plan, wait=True)
        # ポーズターゲットを元に戻す
        moveit_client.set_pose_target(current_pose)
        moveit_client.go(wait=True)
        
        # 制約をクリア
        moveit_client.clear_path_constraints()

        return success



    def signal_handler(self, sig, frame):
        if self.last_msg is None:
            print("No image data received.")
            sys.exit(1)

        print('stop')
        # self.vel_input.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # self.vel_pub.publish(self.vel_input)
        print('stop command sent')

        dsr_img = cv2.imread('./input_dsrim/kensyo_desired_image.png', cv2.IMREAD_GRAYSCALE)
        init_img = cv2.imread('./servo_data/kensyo_initial_image.png', cv2.IMREAD_GRAYSCALE)

        image_raw = self.last_msg
        bridge = CvBridge()
        bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
        bgr = bgr[ 200 : 560 ,720 : 1360 ]

        get_data = DATA(bgr, dsr_img, init_img, self.rmse_data, self.dist_trans_x, self.dist_trans_y, self.dist_trans_z, 
                    self.dist_rot_x, self.dist_rot_y, self.dist_rot_z, self.error_rot_axis, self.error_rot_ang, self.dist_data, 
                    self.time_series, self.base_joint_data, self.shoulder_joint_data, self.elbow_joint_data, self.wrist1_joint_data, self.wrist2_joint_data, self.wrist3_joint_data, 
                    self.rmseth, self.iteration)
        
        get_data.main()
        sys.exit(0)



    def main_callback(self, msg):
        self.last_msg = msg

    
        # with open('./dsrth_result/desired_pose.csv', 'r') as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         desired_pose = [float(x) for x in row]

        # with open('./dsrth_result/desired_pose_mid.csv', 'r') as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         desired_pose = [float(x) for x in row]

        # with open('./dsrth_result/desired_pose_down.csv', 'r') as f:
        #     reader = csv.reader(f)
        #     for row in reader:
        #         desired_pose = [float(x) for x in row]
            
    
        image_raw = msg
        bridge = CvBridge()
        bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
        bgr = bgr[200 : 560, 720 : 1360]
        gry = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        # gry = cv2.threshold(gry, self.threshhold_value, 255, cv2.THRESH_BINARY)#2values
        
        gry2 = np.array(gry, dtype='float64')
        I_vec = gry2.reshape(-1, 1)

        dI = self.I_dsr_vec - I_vec
        dI2 = dI**2
        Isum = np.sum(dI2)
        rmse = math.sqrt(Isum / self.nop)
        print('rmse = %f' % rmse)

        rospy.wait_for_service('getpose')
        getpose_client = rospy.ServiceProxy('getpose', GettfPose)
        respose = getpose_client()
        current_pose_x = respose.trans[0]
        current_pose_y = respose.trans[1]
        current_pose_z = respose.trans[2]
        rot = respose.rot 
        euler_x, euler_y, euler_z = self.quaternion_to_euler(rot)
        if euler_z > 0:
            euler_z -= 6.283
   
        if rmse < self.rmseth or len(self.rmse_data) > self.iteration:
            print('stop')
            print('stop command sent')

            dsr_img = cv2.imread('./input_dsrim/kensyo_desired_image.png', cv2.IMREAD_GRAYSCALE)
            init_img = cv2.imread('./servo_data/kensyo_initial_image.png', cv2.IMREAD_GRAYSCALE)

            image_raw = msg
            bridge = CvBridge()
            bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
            bgr = bgr[ 200 : 560 ,720 : 1360 ]

            get_data = DATA(bgr, dsr_img, init_img, self.rmse_data, self.dist_trans_x, self.dist_trans_y, self.dist_trans_z, 
                        self.dist_rot_x, self.dist_rot_y, self.dist_rot_z, self.error_rot_axis, self.error_rot_ang, self.dist_data, 
                        self.time_series, self.base_joint_data, self.shoulder_joint_data, self.elbow_joint_data, self.wrist1_joint_data, self.wrist2_joint_data, self.wrist3_joint_data, 
                        self.rmseth, self.iteration)
            
            get_data.main()

            rospy.signal_shutdown('finish')
    
        else:
            # go_pose = self.lmbd * np.dot(self.pinv_int_mat_double, dI)
            # self.vel_input.data = np.dot(self.pinv_int_manip, go_pose)
            # self.vel_pub.publish(self.vel_input)

            go_pose_deff = self.lmbd*(np.dot(self.pinv_int_mat_double, dI)) 
            go_pose_deff  =go_pose_deff.T     
            go_pose_deff  = go_pose_deff.flatten()
            self.ik(self.initial_joint_values, go_pose_deff,euler_x, euler_y, euler_z ,self.moveit_client)	


            rospy.wait_for_service('getvel')
            getvel_client = rospy.ServiceProxy('getvel', GetCurrentJointVel)
            resvel = getvel_client()

            current_base_vel = resvel.current_joint_vel[0]
            current_shoulder_vel = resvel.current_joint_vel[1]
            current_elbow_vel = resvel.current_joint_vel[2]
            current_wrist1_vel = resvel.current_joint_vel[3]
            current_wrist2_vel = resvel.current_joint_vel[4]
            current_wrist3_vel = resvel.current_joint_vel[5]

            dist = 1000 * math.sqrt((self.desired_pose[0] - current_pose_x)**2 + (self.desired_pose[2] - current_pose_z)**2)
            trans_x_dist = 1000 * math.sqrt((self.desired_pose[0] - current_pose_x)**2)
            trans_y_dist = 1000 * math.sqrt((self.desired_pose[1] - current_pose_y)**2)
            trans_z_dist = 1000 * math.sqrt((self.desired_pose[2] - current_pose_z)**2)
            rot_x_dist = math.sqrt((self.desired_pose[3] - euler_x)**2) * 180 / math.pi
            rot_y_dist = math.sqrt((self.desired_pose[4] - euler_y)**2) * 180 / math.pi
            rot_z_dist = math.sqrt((self.desired_pose[5] - euler_z)**2) * 180 / math.pi      

            desired_quaternion = [0, 0, 0, 0]
            desired_quaternion[0], desired_quaternion[1], desired_quaternion[2], desired_quaternion[3] = self.euler_to_quaternion(self.desired_pose[3], self.desired_pose[4], self.desired_pose[5])
            desired_quaternion = np.array(desired_quaternion)
            current_quaternion = np.abs(np.array(rot))

            lamd_xd = desired_quaternion[0] / math.sqrt(1.0 - (desired_quaternion[3])**2)
            lamd_yd = desired_quaternion[1] / math.sqrt(1.0 - (desired_quaternion[3])**2)
            lamd_zd = desired_quaternion[2] / math.sqrt(1.0 - (desired_quaternion[3])**2)

            lamd_xc = current_quaternion[0] / math.sqrt(1.0 - (current_quaternion[3])**2)
            lamd_yc = current_quaternion[1] / math.sqrt(1.0 - (current_quaternion[3])**2)
            lamd_zc = current_quaternion[2] / math.sqrt(1.0 - (current_quaternion[3])**2)

            error_rotation_axis = np.abs((np.arccos(lamd_xd * lamd_xc + lamd_yd * lamd_yc + lamd_zd * lamd_zc)) * 180 / math.pi)  
            error_rotation_angle = np.abs(np.arccos(desired_quaternion[3]) * 2 - np.arccos(current_quaternion[3]) * 2) * 180 / math.pi

            current_time = time.time() - self.start_time
            self.time_series.append(current_time)
            self.rmse_data.append(rmse)

            self.base_joint_data.append(current_base_vel)
            self.shoulder_joint_data.append(current_shoulder_vel)
            self.elbow_joint_data.append(current_elbow_vel)
            self.wrist1_joint_data.append(current_wrist1_vel)
            self.wrist2_joint_data.append(current_wrist2_vel)
            self.wrist3_joint_data.append(current_wrist3_vel)

            self.joint_vel_values_data.append([current_base_vel, current_shoulder_vel, current_elbow_vel, current_wrist1_vel, current_wrist2_vel, current_wrist3_vel])
            self.pose_data.append([current_pose_x, current_pose_y, current_pose_z])
            self.dist_data.append(dist)

            self.dist_trans_x.append(trans_x_dist)
            self.dist_trans_y.append(trans_y_dist)
            self.dist_trans_z.append(trans_z_dist)
            self.dist_rot_x.append(rot_x_dist)
            self.dist_rot_y.append(rot_y_dist)
            self.dist_rot_z.append(rot_z_dist)  

            self.error_rot_axis.append(error_rotation_axis)
            self.error_rot_ang.append(error_rotation_angle)

    
    def run(self, csv_file):
        # self.switch_to_joint_group_vel()
        # atexit.register(self.switch_to_scaled_pos)
        self.readpickle()
        # self.readpickle1()
        self.gen_dsrimvec()
        self.read_dsrpose(csv_file)
        # self.vel_pub = rospy.Publisher('/joint_group_vel_controller/command', Float64MultiArray, queue_size=10)
        # self.vel_input = Float64MultiArray()
        # self.vel_input.layout.data_offset = 1
        self.start_time = time.time()
        rospy.Subscriber('/camera/color/image_raw', Image, self.main_callback)
        signal.signal(signal.SIGINT, self.signal_handler)
        rospy.spin()
        
    
    
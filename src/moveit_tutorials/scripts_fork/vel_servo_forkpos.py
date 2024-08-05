#!/usr/bin/env python3
#coding: UTF-8

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import rospy
import numpy as np
from math import pi
import quaternion
import cv2
import tf.transformations
import pandas as pd
import math
import time
import csv
from sensor_msgs.msg import Image
# from sensor_msgs.msg import JointState
from cv_bridge import CvBridge
import signal
import sys

import ikpy
from ikpy.chain import Chain
from ikpy.link import URDFLink
from ur_ikfast.ur_ikfast import ur_kinematics
import moveit_commander
import moveit_msgs.msg

import ikfastpy

import atexit

#for velocity control
from std_msgs.msg import Float64MultiArray
#for joint states servicecall
from moveit_tutorials.srv import GetCurrentJointVel
#for pose servicecall
from moveit_tutorials.srv import GettfPose
#for switch controller
from controller_manager_msgs.srv import SwitchController, SwitchControllerRequest, SwitchControllerResponse
from moveit_commander import RobotCommander, MoveGroupCommander, PlanningSceneInterface, roscpp_initialize, roscpp_shutdown
from geometry_msgs.msg import Pose

from robot_helpers.robot_helpers.ros import moveit
from robot_helpers.robot_helpers import spatial
from scipy.spatial.transform import Rotation
#number of pixels
# nop = 2073600
nop = 230400
pinv_int_mat_double = np.empty((6,6))
pinv_int_manip = np.empty((6,6))
I_dsr_vec = np.empty((nop, 1))
lmbd = 0.25

rmseth = 0.0 #5.0 

time_series = []
rmse_data = []

base_joint_data = []
shoulder_joint_data = []
elbow_joint_data = []
wrist1_joint_data = []
wrist2_joint_data = []
wrist3_joint_data = []

joint_vel_values_data = []

pose_data = []
dist_data = []

dist_trans_x = []
dist_trans_y = []
dist_trans_z = []
dist_rot_x = []
dist_rot_y = []
dist_rot_z = []

error_rot_axis = []
error_rot_ang = []

#robot helpers
moveit_client = moveit.MoveItClient("manipulator")

#moveit
# moveit_client = moveit_commander.MoveGroupCommander("manipulator")
# moveit_client.set_max_velocity_scaling_factor(value=0.2)
# moveit_client.set_max_acceleration_scaling_factor(value=0.2)

def switch_controller(start_controllers, stop_controllers):
    switch_service = rospy.ServiceProxy('/controller_manager/switch_controller', SwitchController)
    resp = switch_service(start_controllers=start_controllers, 
                          stop_controllers=stop_controllers,
                          strictness=2,
                          start_asap=False,
                          timeout=5.0)
    print(resp.ok)

def switch_to_joint_group_vel():
    switch_controller(['joint_group_vel_controller'], ['scaled_pos_joint_traj_controller'])

def switch_to_scaled_pos():
    switch_controller(['scaled_pos_joint_traj_controller'], ['joint_group_vel_controller'])

pinv_int_manip

def readpickle():
    global pinv_int_mat_double
    pickledata = pd.read_pickle('./pinv_int_mat_pickle/pinv_int_mat_double.pickle')
    pinv_int_mat_double = pickledata.values
    return pinv_int_mat_double

def readpickle1():
    global pinv_int_manip
    pickledata1 = pd.read_pickle('./pinv_int_mat_pickle/pinv_int_mnipulator_jac.pickle')
    pinv_int_manip = pickledata1.values
    return pinv_int_manip


def gen_dsrimvec(): 
    global I_dsr_vec
    I_dsr = cv2.imread('./input_dsrim/kensyo_desired_image.png')
    I_dsr_gry = cv2.cvtColor(I_dsr, cv2.COLOR_BGR2GRAY)
    I_dsr_arr = np.array(I_dsr_gry, dtype = 'float64')
    I_dsr_vec = I_dsr_arr.reshape(-1,1)
    return I_dsr_vec

def euler_to_quaternion(eule_x, euler_y, euler_z):
    """Convert Euler Angles to Quaternion

    euler: geometry_msgs/Vector3
    quaternion: geometry_msgs/Quaternion
    """
    q = tf.transformations.quaternion_from_euler(eule_x, euler_y, euler_z)
    return q[0], q[1], q[2], q[3]

def quaternion_to_euler(current_pose):
    """Convert Quaternion to Euler Angles

    quarternion: geometry_msgs/Quaternion
    euler: geometry_msgs/Vector3
    """
    e = tf.transformations.euler_from_quaternion((current_pose[0],current_pose[1],current_pose[2],current_pose[3]))
    return e[0], e[1], e[2]




def signal_handler(sig, frame):


    sys.exit(0)

# def ik(go_pose, current_euler_x, current_euler_y, current_euler_z, moveit_client):
    
#     # Get current joint states
#     current_joint_values = moveit_client.get_current_joint_values()
    
#     # Create pose goal with current end effector pose
#     current_pose = moveit_client.get_current_pose().pose
#     pose_goal = Pose()
#     pose_goal.position.x = current_pose.position.x + go_pose[0]
#     pose_goal.position.y = current_pose.position.y + go_pose[1]
#     pose_goal.position.z = current_pose.position.z + go_pose[2]

#     # Convert euler angles to quaternion and add to current orientation
#     goal_euler = [0.0, 0.0, 0.0]
#     goal_euler[0] = current_euler_x #+ go_pose[3]
#     goal_euler[1] = current_euler_y #+ go_pose[4]
#     goal_euler[2] = current_euler_z #+ go_pose[5]
#     goal_euler = np.array(goal_euler)

#     pose_goal.orientation.x ,pose_goal.orientation.y, pose_goal.orientation.z, pose_goal.orientation.w= euler_to_quaternion(goal_euler[0], goal_euler[1], goal_euler[2])   

#     # ## 制約を定義
#     # constraints= moveit_msgs.msg.Constraints()
# 	# # # # 各関節の制限を設定
#     # joints_name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']


#     # joints_goal = current_joint_values  # 目標角度（radians）
	
#     # tolerances_deg=[90,120,120,120,120,120]
#     # tolerances = [x * pi/180 for x in tolerances_deg] # 許容範囲（radians）    
#     # for i in range(6):
#     #     joint_constraint = moveit_msgs.msg.JointConstraint()
#     #     joint_constraint.joint_name = joints_name[i]
#     #     joint_constraint.position = joints_goal[i]
#     #     joint_constraint.tolerance_above = tolerances[i]
#     #     joint_constraint.tolerance_below = tolerances[i]
#     #     joint_constraint.weight = 1.0
#     #     constraints.joint_constraints.append(joint_constraint)

# 	# # # # 制約をMoveGroupに適用
#     # moveit_client.set_path_constraints(constraints)


#     waypoints = [pose_goal]
#     (plan, fraction) =moveit_client.compute_cartesian_path(waypoints , eef_step=0.008, jump_threshold=0.00 )
#     moveit_client.execute(plan, wait=True)
#     moveit_client.set_pose_target(current_pose)
#     moveit_client.go(wait=True)


def ik(go_pose, current_euler_x, current_euler_y, current_euler_z, moveit_client):
    
    # Get current joint states
    current_joint_values = moveit_client.move_group.get_current_joint_values()
    
    # Create pose goal with current end effector pose
    current_pose = moveit_client.move_group.get_current_pose().pose
    pose_goal = Pose()
    pose_goal.position.x = current_pose.position.x + go_pose[0]
    pose_goal.position.y = current_pose.position.y + go_pose[1]
    pose_goal.position.z = current_pose.position.z + go_pose[2]
    pose_goal_position = [pose_goal.position.x, pose_goal.position.y, pose_goal.position.z]
    
    # Convert euler angles to quaternion and add to current orientation
    goal_euler = [0.0, 0.0, 0.0]
    goal_euler[0] = current_euler_x #+ go_pose[3]
    goal_euler[1] = current_euler_y #+ go_pose[4]
    goal_euler[2] = current_euler_z #+ go_pose[5]
    goal_euler = np.array(goal_euler)

    pose_goal.orientation.x ,pose_goal.orientation.y, pose_goal.orientation.z, pose_goal.orientation.w= euler_to_quaternion(goal_euler[0], goal_euler[1], goal_euler[2])   
    goal_quat = np.array([pose_goal.orientation.x, pose_goal.orientation.y, pose_goal.orientation.z, pose_goal.orientation.w])

    pose_goal = spatial.Transform(goal_quat, pose_goal_position)
    print(pose_goal.translation)
    print(pose_goal.rotation)
    # moveit_client.goto(pose_goal)
    # joint_goal = moveit_client.move_group.get_current_joint_values()
    # waypoints = [pose_goal]
    # Plan to the new goal
    success, plan =moveit_client.plan(pose_goal)
    # plan  = group.plan()
    # print(plan)
    print(current_joint_values)
    joint_goal = plan.joint_trajectory.points[-1].positions
    print(joint_goal)
    
    
    # Calculate joint angle differences (current - goal)
    joint_diffs = np.array([[ goal - current for goal, current in zip(joint_goal, current_joint_values)]])
    if np.any(np.abs(joint_diffs) > 1):
        joint_diffs = np.zeros_like(joint_diffs)
    
    print(joint_diffs)

    return joint_diffs

    

# def ik(current_joint, current_euler, pose_euler_deff):
#     pose_dsr = np.array(current_euler) + np.array(pose_euler_deff)
#     pose_quat = [pose_dsr[0], pose_dsr[1], pose_dsr[2], 0.0, 0.0, 0.0, 0.0]
#     # print("\n-----------------------------\n")
#     # print("pose_euler:")
#     # print(pose_dsr)

#     ur5e_arm = ur_kinematics.URKinematics('ur5e')
#     joint_angles = current_joint # in radians
#     pose_quat[3], pose_quat[4], pose_quat[5], pose_quat[6]= euler_to_quaternion(pose_dsr[3],pose_dsr[4], pose_dsr[5] )
#     pose_quat = [pose_dsr[0], pose_dsr[1], pose_dsr[2], -1*pose_quat[3], -1*pose_quat[4], -1*pose_quat[5], -1*pose_quat[6]]

#     # print("\n-----------------------------\n")
#     # print("input_pose_quaternion:")
#     # print(pose_quat)
#     joint_angles_quat = ur5e_arm.inverse(pose_quat, False, q_guess=joint_angles)
#     # print("\n-----------------------------\n")
#     # print("output_joint_angles")
#     # print(joint_angles_quat)
#     # print(ur5e_arm.forward(current_joint))
#     # print("inverse() one from quat", joint_angles_quat)

#     deff = np.array([joint_angles_quat]) - np.array([current_joint]) 
#     # print("\n-----------------------------\n")
#     # print("output_joint_angles - current_joint_angles")
#     # print(deff)
#     return (deff.T)


# def ik(current_joint, current_euler, pose_euler_deff):
#     pose_dsr = np.array(current_euler) + np.array(pose_euler_deff)
#     transform_matrix = pose_to_rigid_transformation_matrix(pose_dsr)
#     # print("\n-----------------------------\n")
#     # print("pose_euler:")
#     # print(pose_dsr)

#     ur5e_arm = ur_kinematics.URKinematics('ur5e')
#     joint_angles = current_joint # in radians
#     pose_quat[3], pose_quat[4], pose_quat[5], pose_quat[6]= euler_to_quaternion(pose_dsr[3],pose_dsr[4], pose_dsr[5] )
#     pose_quat = [pose_dsr[0], pose_dsr[1], pose_dsr[2], -1*pose_quat[3], -1*pose_quat[4], -1*pose_quat[5], -1*pose_quat[6]]

#     # print("\n-----------------------------\n")
#     # print("input_pose_quaternion:")
#     # print(pose_quat)
#     joint_angles_quat = ur5e_arm.inverse(pose_quat, False, q_guess=joint_angles)
#     # print("\n-----------------------------\n")
#     # print("output_joint_angles")
#     # print(joint_angles_quat)
#     # print(ur5e_arm.forward(current_joint))
#     # print("inverse() one from quat", joint_angles_quat)

#     deff = np.array([joint_angles_quat]) - np.array([current_joint]) 
#     # print("\n-----------------------------\n")
#     # print("output_joint_angles - current_joint_angles")
#     # print(deff)
#     return (deff.T)



def main(msg):
    global pinv_int_mat_double
    global pinv_int_manip
    global I_dsr_vec
    
    global rmseth
    
    global base_joint_data
    global shoulder_joint_data
    global elbow_joint_data
    global wrist1_joint_data
    global wrist2_joint_data
    global wrist3_joint_data
    
    global joint_vel_values_data
    
    global time_series
    global rmse_data
    global pose_data
    global dist_data

    global dist_trans_x
    global dist_trans_y
    global dist_trans_z
    global dist_rot_x
    global dist_rot_y
    global dist_rot_z   

    global error_rot_axis
    global error_rot_ang

    global moveit_client
    
    # rmse = 100
    
    with open('./dsrth_result/desired_pose.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            desired_pose = [float(x) for x in row]

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
    bgr= bgr[ 200 : 560 ,720 : 1360 ]
    # bgr = bridge.imgmsg_to_cv2(image_raw, 'mono8') ###UI camera
    gry = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    gry2 = np.array(gry, dtype = 'float64')
    I_vec = gry2.reshape(-1,1)
    
    #画像偏差計算
    dI = I_dsr_vec - I_vec ###目標-現在
    dI2 = dI**2
    Isum = np.sum(dI2)
    rmse = math.sqrt(Isum / nop)
    print("\n-----------------------------\n")
    print("\n-----------------------------\n")
    print('rmse = %f' % rmse)
    
    rospy.wait_for_service('getpose')
    getpose_client = rospy.ServiceProxy('getpose', GettfPose)
    respose = getpose_client()
    # print(respose)
    current_pose_x = respose.trans[0] ###tfも単位[m]で記録されてる
    current_pose_y = respose.trans[1]
    current_pose_z = respose.trans[2]
    rot = respose.rot 
    euler_x, euler_y, euler_z = quaternion_to_euler(rot)
    if euler_z > 0 :
        euler_z = euler_z - 6.283




    
    if rmse < rmseth or len(rmse_data) > 1000:#(time.time() - start_time) > 33.333:
    # if abs(desired_pose[0] - current_pose_x) < 0.0002 and abs(desired_pose[1] - current_pose_y) < 0.0002:
        print('stop')
        vel_input.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        vel_pub.publish(vel_input)
        print('stop command sent')

        dsr_img = cv2.imread('./input_dsrim/kensyo_desired_image.png', cv2.IMREAD_GRAYSCALE)

        image_raw = msg
        bridge = CvBridge()
        bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
        bgr = bgr[ 200 : 560 ,720 : 1360 ]
        cv2.imwrite('./servo_data/kensyo_last_image.png', bgr)
        gry = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
        

        init_img = cv2.imread('./servo_data/kensyo_initial_image.png', cv2.IMREAD_GRAYSCALE)

        # 画素値の差分を計算
        difference_init = cv2.absdiff(dsr_img, init_img)
        difference_image_path = './servo_data/init_difference_image.jpg'
        cv2.imwrite(difference_image_path, difference_init)

        difference_last = cv2.absdiff(dsr_img, gry)
        # 差分画像を保存
        difference_image_path = './servo_data/last_difference_image.jpg'
        cv2.imwrite(difference_image_path, difference_last)
        # filename = './servo_data/loop_rmse_data.csv'
        # filename2 = './servo_data/joint_vel_data.csv'
        # filename3 = './servo_data/pose_data.csv'
        # filename4 = './servo_data/2posedist.csv'
        # with open (filename, 'w') as f, open(filename2, 'w')as f2, open(filename3, 'w')as f3 , open(filename4, 'w')as f4:
        #     writer = csv.writer(f)
        #     writer.writerow(rmse_data)
        #     writer2 = csv.writer(f2)
        #     writer2.writerow(joint_vel_values_data)
        #     writer3 = csv.writer(f3)
        #     writer3.writerow(pose_data)
        #     writer4 = csv.writer(f4)
        #     writer4.writerow(dist_data)

        filename = './servo_data/loop_rmse_data.csv'
        filename2 = './servo_data/2posedist.csv'
        filename3 = './servo_data/y_dist.csv'
        filename4 = './servo_data/rotation_axis.csv'
        filename5 = './servo_data/rotation_angle.csv'
        filename6 = './servo_data/last_position_traslation.csv'

        with open (filename, 'w') as f, open(filename2, 'w')as f2, open(filename3, 'w')as f3, \
        open(filename4, 'w')as f4, open(filename5, 'w')as f5, open(filename6, 'w')as f6:
            writer = csv.writer(f)
            writer.writerow(rmse_data)
            writer2 = csv.writer(f2)
            writer2.writerow(dist_data)
            writer3 = csv.writer(f3)
            writer3.writerow(dist_trans_y)
            writer4 = csv.writer(f4)
            writer4.writerow(error_rot_axis)
            writer5 = csv.writer(f5)
            writer5.writerow(error_rot_ang)
            writer6 = csv.writer(f6)
            writer6.writerow(["2dist", "x", "y", "z", "rx", "ry", "rz"])
            writer6.writerow([dist_data[-1], dist_trans_x[-1], dist_trans_y[-1], dist_trans_z[-1] ,
                              dist_rot_x[-1], dist_rot_y[-1], dist_rot_z[-1]])
            

###################　関節速度グラフ　################################################### 
        #6つのグラフの配置
        fig = plt.figure(figsize = (10,10))
        ax1 = fig.add_subplot(3,2,1)
        ax2 = fig.add_subplot(3,2,2)
        ax3 = fig.add_subplot(3,2,3)
        ax4 = fig.add_subplot(3,2,4)
        ax5 = fig.add_subplot(3,2,5)
        ax6 = fig.add_subplot(3,2,6)
        
        #各ループごとの各ジョイント角プロット
        ax1.plot(time_series, base_joint_data, color = 'blue', label = 'current joint velocity')
        ax2.plot(time_series, shoulder_joint_data, color = 'blue', label = 'current joint velocity')
        ax3.plot(time_series, elbow_joint_data, color = 'blue', label = 'current joint velocity')
        ax4.plot(time_series, wrist1_joint_data, color = 'blue', label = 'current joint velocity')
        ax5.plot(time_series, wrist2_joint_data, color = 'blue', label = 'current joint velocity')
        ax6.plot(time_series, wrist3_joint_data, color = 'blue', label = 'current joint velocity')
        
        # #目標角度をプロットscrewdriver
        ax1.axhline(y = 0.0, color = 'red')
        ax2.axhline(y = 0.0, color = 'red')
        ax3.axhline(y = 0.0, color = 'red')
        ax4.axhline(y = 0.0, color = 'red')
        ax5.axhline(y = 0.0, color = 'red')
        ax6.axhline(y = 0.0, color = 'red')
        
        #x軸のラベル
        ax1.set_xlabel('Time[s]')
        ax2.set_xlabel('Time[s]')
        ax3.set_xlabel('Time[s]')
        ax4.set_xlabel('Time[s]')
        ax5.set_xlabel('Time[s]')
        ax6.set_xlabel('Time[s]')
        
        #y軸のラベル
        ax1.set_ylabel('base joint velocity[rad/s]')
        ax2.set_ylabel('shoulder joint velocity[rad/s]')
        ax3.set_ylabel('elbow joint velocity[rad/s]')
        ax4.set_ylabel('wrist1 joint velocity[rad/s]')
        ax5.set_ylabel('wrist2 joint velocity[rad/s]')
        ax6.set_ylabel('wrist3 joint velocity[rad/s]')
        
        #凡例表示
        ax1.legend(ncol = 2, loc = 'lower right')
        ax2.legend(ncol = 2, loc = 'lower right')
        ax3.legend(ncol = 2, loc = 'lower right')
        ax4.legend(ncol = 2, loc = 'lower right')
        ax5.legend(ncol = 2, loc = 'lower right')
        ax6.legend(ncol = 2, loc = 'lower right')
        
        #重なり解消
        plt.tight_layout()
        
        ax1.grid()
        ax2.grid()
        ax3.grid()
        ax4.grid()
        ax5.grid()
        ax6.grid()
        
        #縦軸横軸の最大値、最小値、目盛り自動設定のグラフ保存
        fig.savefig('./servo_data/joint_vel_values.png')
        
        # y-axisの最大値と最小値を計算
        y_min = min(min(base_joint_data), min(shoulder_joint_data), min(elbow_joint_data), min(wrist1_joint_data), min(wrist2_joint_data), min(wrist3_joint_data))
        y_max = max(max(base_joint_data), max(shoulder_joint_data), max(elbow_joint_data), max(wrist1_joint_data), max(wrist2_joint_data), max(wrist3_joint_data))

        # 各サブプロットのy-axisのスケールを一致させる
        ax1.set_ylim(y_min, y_max)
        ax2.set_ylim(y_min, y_max)
        ax3.set_ylim(y_min, y_max)
        ax4.set_ylim(y_min, y_max)
        ax5.set_ylim(y_min, y_max)
        ax6.set_ylim(y_min, y_max)

        # 保存
        fig.savefig('./servo_data/joint_values_double_scaled.png')
        
########################################################################################################################################

        #generate graph
        # fig_rmse = plt.figure()
        # plt.xlabel('Time[s]')
        # plt.ylabel('RMSE')
        # plt.plot(time_series, rmse_data, 'b-')
        # plt.ylim([rmseth, 50])
        # plt.grid()
        # fig_rmse.savefig('./servo_data/rmse_double.png')

        fig_rmse_it = plt.figure()
        iteration = np.linspace(0, len(rmse_data), len(rmse_data))
        plt.xlabel('iteration')
        plt.ylabel('RMSE')
        plt.plot(iteration, rmse_data, 'b-')
        plt.ylim([rmseth, 35])
        plt.grid()
        fig_rmse_it.savefig('./servo_data/rmse_iteration.png')

        fig_dist = plt.figure()
        iteration = np.linspace(0, len(dist_data), len(dist_data))
        plt.xlabel('iteration')
        plt.ylabel('Distance in XZ plane[mm]')
        plt.plot(iteration, dist_data, 'b-')
        plt.ylim([0.0, 30.0])
        plt.grid()
        fig_dist.savefig('./servo_data/2posedist.png')
    
        fig_y_dist = plt.figure()
        iteration = np.linspace(0, len(dist_trans_y), len(dist_trans_y))
        plt.xlabel('iteration')
        plt.ylabel('Distance on Y axis[mm]')
        plt.plot(iteration, dist_trans_y, 'b-')
        plt.ylim([0.0, 5.0])
        plt.grid()
        fig_y_dist.savefig('./servo_data/ydist.png')

        rot_axis_dist = plt.figure()
        iteration = np.linspace(0, len(error_rot_axis), len(error_rot_axis))
        plt.xlabel('iteration')
        plt.ylabel('Error of rotation axis[deg]')
        plt.plot(iteration, error_rot_axis, 'b-')
        plt.ylim([0.0, 2.0])
        plt.grid()
        rot_axis_dist.savefig('./servo_data/rot_axis.png')

        rot_ang_dist = plt.figure()
        iteration = np.linspace(0, len(error_rot_ang), len(error_rot_ang))
        plt.xlabel('iteration')
        plt.ylabel('Error of rotation angle[deg]')
        plt.plot(iteration, error_rot_ang, 'b-')
        plt.ylim([0.0, 2.0])
        plt.grid()
        rot_ang_dist.savefig('./servo_data/rot_ang.png')      


        print('2dist = %f' % dist_data[-1])        
        print('x = %f' % dist_trans_x[-1])
        print('y = %f' % dist_trans_y[-1])
        print('z = %f' % dist_trans_z[-1])
        print('rx = %f' % dist_rot_x[-1])
        print('ry = %f' % dist_rot_y[-1])
        print('rz = %f' % dist_rot_z[-1])



        fig_rt_dist = plt.figure()
        ax1 = fig_rt_dist.add_subplot()
        ax2 = ax1.twinx() 

        ax1.plot(time_series, dist_trans_x, 'r-', label = "X axis translation")
        ax1.plot(time_series, dist_trans_y, 'b-', label = "Y axis translation")
        ax1.plot(time_series, dist_trans_z,'g-', label = "Z axis translation")
        ax2.plot(time_series, dist_rot_x, 'k--', label = "X axis rotation" ,markersize = 1)
        ax2.plot(time_series, dist_rot_y, 'y--', label = "Y axis rotation" ,markersize = 1)
        ax2.plot(time_series, dist_rot_z, 'm--', label = "Z axis rotation" ,markersize = 1)

        ax1.set_xlabel('Time[s]')  #x軸ラベル
        ax1.set_ylabel("Position error[mm]")  #y1軸ラベル
        ax2.set_ylabel("Rotation error[deg]")  #y2軸ラベル
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2 ,loc='upper right')
        ax1.set_ylim([0, 30])
        ax2.set_ylim([0, 2.0])

        ax1.grid()
        fig_rt_dist.savefig('./servo_data/trans_rot_dist.png')     

        fig_rt_dist = plt.figure()
        iteration = np.linspace(0, len(rmse_data), len(rmse_data))
        ax1 = fig_rt_dist.add_subplot()
        ax2 = ax1.twinx() 

        ax1.plot(iteration, dist_trans_x, 'r-', label = "X axis translation")
        ax1.plot(iteration, dist_trans_y, 'b-', label = "Y axis translation")
        ax1.plot(iteration, dist_trans_z,'g-', label = "Z axis translation")
        ax2.plot(iteration, dist_rot_x, 'k--', label = "X axis rotation" ,markersize = 1)
        ax2.plot(iteration, dist_rot_y, 'y--', label = "Y axis rotation" ,markersize = 1)
        ax2.plot(iteration, dist_rot_z, 'm--', label = "Z axis rotation" ,markersize = 1)

        ax1.set_xlabel('iteration')  #x軸ラベル
        ax1.set_ylabel("Position error[mm]")  #y1軸ラベル
        ax2.set_ylabel("Rotation error[deg]")  #y2軸ラベル
        h1, l1 = ax1.get_legend_handles_labels()
        h2, l2 = ax2.get_legend_handles_labels()
        ax1.legend(h1+h2, l1+l2 ,loc='upper right')
        ax1.set_ylim([0, 30])
        ax2.set_ylim([0, 2.0])

        ax1.grid()
        fig_rt_dist.savefig('./servo_data/trans_rot_dist_iteration.png')  

        rospy.signal_shutdown('finish')
    
    else:
        # # ikfast
        # current_joint = moveit_client.move_group.get_current_joint_values()
        # current_pose_euler = [current_pose_x, current_pose_y, current_pose_z, euler_x, euler_y, euler_z]
        # go_pose_deff = lmbd*(np.dot(pinv_int_mat_double, dI)) 
        # go_pose_deff  =go_pose_deff .T     
        # go_pose_deff  = go_pose_deff.flatten()
        # vel_input.data = ik(current_joint,current_pose_euler,go_pose_deff)		
        # vel_pub.publish(vel_input) #プログラミングROS P109では速度の値だけf分岐させてpublish部分はif分岐の外においてた


        # moveit
        go_pose_deff = np.dot(pinv_int_mat_double, dI)
        # go_pose_deff = lmbd*(np.dot(pinv_int_mat_double, dI)) 
        go_pose_deff  =go_pose_deff.T     
        go_pose_deff  = go_pose_deff.flatten()
        joint_deff = ik(go_pose_deff,euler_x, euler_y, euler_z ,moveit_client)	
        vel_input.data = 0.2*(joint_deff.T)        
        vel_pub.publish(vel_input) #プログラミングROS P109では速度の値だけf分岐させてpublish部分はif分岐の外においてた


        # # マニピュレータヤコビアン
        # go_pose = lmbd*(np.dot(pinv_int_mat_double, dI)) 
        # vel_input.data = np.dot(pinv_int_manip, go_pose)
        # print(vel_input.data)
        # vel_pub.publish(vel_input) #プログラミングROS P109では速度の値だけf分岐させてpublish部分はif分岐の外においてた

        #serviceで関節角速度取得
        rospy.wait_for_service('getvel')
        getvel_client = rospy.ServiceProxy('getvel', GetCurrentJointVel)
        resvel = getvel_client()
        # print(resvel)
        
        current_base_vel = resvel.current_joint_vel[0]
        current_shoulder_vel = resvel.current_joint_vel[1]
        current_elbow_vel = resvel.current_joint_vel[2]
        current_wrist1_vel = resvel.current_joint_vel[3]
        current_wrist2_vel = resvel.current_joint_vel[4]
        current_wrist3_vel = resvel.current_joint_vel[5]
        
        ###pose が単位mで出力される
        ### 距離がしきい値以上で速度計算される場合に距離算出+append
        # dist = 1000*math.sqrt((desired_pose[0] - current_pose_x)**2 + (desired_pose[1] - current_pose_y)**2 + (desired_pose[2] - current_pose_z)**2)
        dist = 1000*math.sqrt((desired_pose[0] - current_pose_x)**2  + (desired_pose[2] - current_pose_z)**2) ###x,z軸方向だけの距離を出す

        trans_x_dist = 1000*math.sqrt((desired_pose[0] - current_pose_x)**2)
        trans_y_dist = 1000*math.sqrt((desired_pose[1] - current_pose_y)**2)
        trans_z_dist = 1000*math.sqrt((desired_pose[2] - current_pose_z)**2)
        rot_x_dist = math.sqrt((desired_pose[3] - euler_x)**2)*180 / math.pi
        rot_y_dist = math.sqrt((desired_pose[4] - euler_y)**2)*180 / math.pi
        rot_z_dist = math.sqrt((desired_pose[5] - euler_z)**2)*180 / math.pi      
 
        desired_quaternion = [0, 0, 0, 0]
        desired_quaternion[0], desired_quaternion[1], desired_quaternion[2], desired_quaternion[3] = euler_to_quaternion(desired_pose[3], desired_pose[4], desired_pose[5])
        desired_quaternion = np.array(desired_quaternion)
        current_quaternion = np.abs(np.array(rot)) #inputのとき
        # current_quaternion = np.array(rot)

        lamd_xd = desired_quaternion[0]/math.sqrt(1.0-(desired_quaternion[3])**2)
        lamd_yd = desired_quaternion[1]/math.sqrt(1.0-(desired_quaternion[3])**2)
        lamd_zd = desired_quaternion[2]/math.sqrt(1.0-(desired_quaternion[3])**2)

        lamd_xc = current_quaternion[0]/math.sqrt(1.0-(current_quaternion[3])**2)
        lamd_yc = current_quaternion[1]/math.sqrt(1.0-(current_quaternion[3])**2)
        lamd_zc = current_quaternion[2]/math.sqrt(1.0-(current_quaternion[3])**2)

        # error_rotation_axis = np.abs((np.arccos(desired_quaternion[0]*current_quaternion[0]+desired_quaternion[1]*current_quaternion[1]+desired_quaternion[2]*current_quaternion[2]))*180 / math.pi)  
        error_rotation_axis =  np.abs((np.arccos(lamd_xd*lamd_xc+lamd_yd*lamd_yc+lamd_zd*lamd_zc))*180 / math.pi)  
        error_rotation_angle = np.abs(np.arccos(desired_quaternion[3])*2- np.arccos(current_quaternion[3])*2)*180 / math.pi

        


        current_time = time.time() - start_time
        time_series.append(current_time)
        rmse_data.append(rmse)

        base_joint_data.append(current_base_vel)
        shoulder_joint_data.append(current_shoulder_vel)
        elbow_joint_data.append(current_elbow_vel)
        wrist1_joint_data.append(current_wrist1_vel)
        wrist2_joint_data.append(current_wrist2_vel)
        wrist3_joint_data.append(current_wrist3_vel)

        joint_vel_values_data.append([current_base_vel, current_shoulder_vel, current_elbow_vel, current_wrist1_vel, current_wrist2_vel, current_wrist3_vel])
        pose_data.append([current_pose_x, current_pose_y, current_pose_z])
        dist_data.append(dist)

        dist_trans_x.append(trans_x_dist)
        dist_trans_y.append(trans_y_dist)
        dist_trans_z.append(trans_z_dist)
        dist_rot_x.append(rot_x_dist)
        dist_rot_y.append(rot_y_dist)
        dist_rot_z.append(rot_z_dist)  

        error_rot_axis.append(error_rotation_axis)
        error_rot_ang.append(error_rotation_angle)


        
        return rmse, time_series, rmse_data, base_joint_data, shoulder_joint_data, elbow_joint_data, wrist1_joint_data, wrist2_joint_data, wrist3_joint_data, joint_vel_values_data, 
    pose_data, dist_data,dist_trans_x, dist_trans_y, dist_trans_z, dist_rot_x, dist_rot_y, dist_rot_z, error_rot_axis, error_rot_ang
        

    
if __name__ == '__main__':
    try:
        rospy.init_node('servo_node')
        rospy.loginfo('servo node started')
        switch_to_joint_group_vel()
        atexit.register(switch_to_scaled_pos)
        readpickle()
        readpickle1()
        gen_dsrimvec()
        vel_pub = rospy.Publisher('/joint_group_vel_controller/command', Float64MultiArray, queue_size=10)
        vel_input = Float64MultiArray()
        vel_input.layout.data_offset = 1
        start_time = time.time()
        rospy.Subscriber('/camera/color/image_raw', Image, main)
        # rospy.Subscriber('/camera/image_raw', Image, main) #for UI camera 
        signal.signal(signal.SIGINT, signal_handler)
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        switch_to_scaled_pos()
        rospy.signal_shutdown('finish')
    
    
#     Exception RuntimeError: 'main thread is not in main loop' in <bound method StringVar.__del__ of <Tkinter.StringVar instance at 0x7f63d3100460>> ignored
# Error in atexit._run_exitfuncs:
# Traceback (most recent call last):
#   File "/usr/lib/python2.7/atexit.py", line 24, in _run_exitfuncs
#     func(*targs, **kargs)
#   File "/home/kappa/.local/lib/python2.7/site-packages/matplotlib/_pylab_helpers.py", line 78, in destroy_all
#     manager.destroy()
#   File "/home/kappa/.local/lib/python2.7/site-packages/matplotlib/backends/_backend_tk.py", line 560, in destroy
#     self.window.destroy()
#   File "/usr/lib/python2.7/lib-tk/Tkinter.py", line 1872, in destroy
#     for c in self.children.values(): c.destroy()
#   File "/home/kappa/.local/lib/python2.7/site-packages/matplotlib/backends/_backend_tk.py", line 658, in destroy
#     Tk.Frame.destroy(self, *args)
#   File "/usr/lib/python2.7/lib-tk/Tkinter.py", line 2109, in destroy
#     for c in self.children.values(): c.destroy()
#   File "/usr/lib/python2.7/lib-tk/Tkinter.py", line 2110, in destroy
#     self.tk.call('destroy', self._w)
# RuntimeError: main thread is not in main loop

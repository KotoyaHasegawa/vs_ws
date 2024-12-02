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
import random

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
from geometry_msgs.msg import Pose, Vector3

from robot_helpers.robot_helpers.ros import moveit
from robot_helpers.robot_helpers import spatial
from scipy.spatial.transform import Rotation

from jikken_data import DATA
#number of pixels
# nop = 2073600
# nop = 230400
nop = 72044
pinv_int_mat_double = np.empty((6,6))
pinv_int_manip = np.empty((6,6))
I_dsr_vec = np.empty((nop, 1))
# lmbd = 0.075 #withdraw
lmbd = 0.035#input

# rmseth = 5.0 #5.0 #withdraw
rmseth = 0.0#8.0 #input


iteration = 500
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

last_msg = None

# #robot helpers
# moveit_client = moveit.MoveItClient("manipulator")

##moveit
moveit_client = moveit_commander.MoveGroupCommander("manipulator")
moveit_client.set_max_velocity_scaling_factor(value=0.2)
moveit_client.set_max_acceleration_scaling_factor(value=0.2)

# Get the current joint values and store them
initial_joint_values = moveit_client.get_current_joint_values()
rospy.loginfo("Initial joint values: %s", initial_joint_values)

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
    return -1*q[0], -1*q[1], -1*q[2], -1*q[3]

def quaternion_to_euler(current_pose):
    """Convert Quaternion to Euler Angles

    quarternion: geometry_msgs/Quaternion
    euler: geometry_msgs/Vector3
    """
    e = tf.transformations.euler_from_quaternion((current_pose[0],current_pose[1],current_pose[2],current_pose[3]))
    return e[0], e[1], e[2]

def ik(initial_joint_values, go_pose, current_euler_x, current_euler_y, current_euler_z, moveit_client):
    # Get current joint states

    
    # Create pose goal with current end effector pose
    current_pose = moveit_client.get_current_pose().pose
    current_pose.position.x = current_pose.position.x + go_pose[0]
    current_pose.position.y = current_pose.position.y + go_pose[1]
    current_pose.position.z = current_pose.position.z + go_pose[2]

    # Convert euler angles to quaternion and add to current orientation
    goal_euler = np.array([current_euler_x + go_pose[3], current_euler_y + go_pose[4], current_euler_z + go_pose[5]])
    quat = euler_to_quaternion(goal_euler[0], goal_euler[1], goal_euler[2])
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
    (plan, fraction) = moveit_client.compute_cartesian_path(waypoints, eef_step=0.008)
    # プランの実行
    success = moveit_client.execute(plan, wait=True)
    # ポーズターゲットを元に戻す
    moveit_client.set_pose_target(current_pose)
    moveit_client.go(wait=True)
    
    # 制約をクリア
    moveit_client.clear_path_constraints()

    return success


def signal_handler(sig, frame):

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

    global last_msg

    global initial_joint_values

    if last_msg is None:
        print("No image data received.")
        sys.exit(1)


    print('stop')
    # vel_input.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    # vel_pub.publish(vel_input)
    print('stop command sent')

    dsr_img = cv2.imread('./input_dsrim/kensyo_desired_image.png', cv2.IMREAD_GRAYSCALE)
    init_img = cv2.imread('./servo_data/kensyo_initial_image.png', cv2.IMREAD_GRAYSCALE)

    image_raw = last_msg
    bridge = CvBridge()
    bgr_full = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
    # bgr = bgr[ 200 : 560 ,720 : 1360 ]#withdraw
    bgr = bgr_full[ 83 : 145 ,470 : 1632 ]  #input

    get_data = DATA( bgr_full,bgr, dsr_img, init_img, rmse_data, dist_trans_x, dist_trans_y, dist_trans_z, 
                 dist_rot_x, dist_rot_y, dist_rot_z, error_rot_axis, error_rot_ang, dist_data, 
                 time_series, base_joint_data, shoulder_joint_data, elbow_joint_data, wrist1_joint_data, wrist2_joint_data, wrist3_joint_data, 
                 rmseth, iteration)
    
    get_data.main()

    sys.exit(0)

    

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

    global initial_joint_values
    
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

    #withdraw
    # if desired_pose[5] > 0 :
    #     desired_pose[5] = desired_pose[5] - 6.283    
    
    image_raw = msg
    bridge = CvBridge()
    bgr_full = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
    # bgr= bgr[ 200 : 560 ,720 : 1360 ]
    bgr= bgr_full[ 83 : 145 ,470 : 1632 ] #input
    # bgr = bridge.imgmsg_to_cv2(image_raw, 'mono8') ###UI camera6
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

    #withdraw
    # if euler_z > 0 :
    #     euler_z = euler_z - 6.283



    if rmse < rmseth or len(rmse_data) > iteration:#(time.time() - start_time) > 33.333:
    # if abs(desired_pose[0] - current_pose_x) < 0.0002 and abs(desired_pose[1] - current_pose_y) < 0.0002:
        print('stop')
        # vel_input.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        # vel_pub.publish(vel_input)
        print('stop command sent')

        dsr_img = cv2.imread('./input_dsrim/kensyo_desired_image.png', cv2.IMREAD_GRAYSCALE)
        init_img = cv2.imread('./servo_data/kensyo_initial_image.png', cv2.IMREAD_GRAYSCALE)

        image_raw = msg
        bridge = CvBridge()
        bgr_full = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
        # bgr = bgr[ 200 : 560 ,720 : 1360 ]#withdraw
        bgr= bgr_full[ 83 : 145 ,470 : 1632 ] #input

        get_data = DATA(bgr_full,bgr, dsr_img, init_img, rmse_data, dist_trans_x, dist_trans_y, dist_trans_z, 
                 dist_rot_x, dist_rot_y, dist_rot_z, error_rot_axis, error_rot_ang, dist_data, 
                 time_series, base_joint_data, shoulder_joint_data, elbow_joint_data, wrist1_joint_data, wrist2_joint_data, wrist3_joint_data, 
                 rmseth, iteration)
        
        get_data.main()

        rospy.signal_shutdown('finish')
    
    else:
        # moveit
        # go_pose_deff = np.dot(pinv_int_mat_double, dI)
        go_pose_deff = lmbd*(np.dot(pinv_int_mat_double, dI)) 
        go_pose_deff  =go_pose_deff.T     
        go_pose_deff  = go_pose_deff.flatten()
        ik(initial_joint_values, go_pose_deff,euler_x, euler_y, euler_z ,moveit_client)	
        # joint_deff = ik(go_pose_deff,euler_x, euler_y, euler_z ,moveit_client)	
        # vel_input.data = 0.2*(joint_deff.T)        
        # vel_pub.publish(vel_input) #プログラミングROS P109では速度の値だけf分岐させてpublish部分はif分岐の外においてた

##############################################################################################################################
#################################    data      ###############################################################################
##############################################################################################################################

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
        # switch_to_joint_group_vel()
        # atexit.register(switch_to_scaled_pos)
        readpickle()
        readpickle1()
        gen_dsrimvec()
        # vel_pub = rospy.Publisher('/joint_group_vel_controller/command', Float64MultiArray, queue_size=10)
        # vel_input = Float64MultiArray()
        # vel_input.layout.data_offset = 1
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
    














##################################################################################################################
##################################### IK Define #################################################################



# def ik(go_pose, current_euler_x, current_euler_y, current_euler_z, moveit_client):
#     # Get current joint states
#     current_joint_values = moveit_client.get_current_joint_values()
#     rospy.loginfo("Current joint values: %s", current_joint_values)
    
#     # Create pose goal with current end effector pose
#     current_pose = moveit_client.get_current_pose().pose
#     rospy.loginfo("Current end effector pose: %s", current_pose)

#     with open('./dsrth_result/desired_pose.csv', 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             desired_pose = [float(x) for x in row]

#     current_pose.position.x = random.uniform(desired_pose[0] - 0.025, desired_pose[0] + 0.025) #差+-0.025
#     current_pose.position.y = desired_pose[1] #差0.02
#     current_pose.position.z = random.uniform(desired_pose[2] - 0.025, desired_pose[2] + 0.025)#差+-0.025

#     # Convert euler angles to quaternion and add to current orientation
#     euler_x = desired_pose[3]#差5度
#     euler_y = desired_pose[4]#差5度
#     euler_z = desired_pose[5]#差5度


#     current_pose.orientation.x, current_pose.orientation.y, current_pose.orientation.z ,current_pose.orientation.w = euler_to_quaternion(euler_x, euler_y, euler_z)

#     rospy.loginfo("Pose goal: %s", current_pose)

#     # 制約を定義
#     constraints = moveit_msgs.msg.Constraints()
#     joints_name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
#     joints_goal = current_joint_values
#     tolerances_deg = [90, 120, 120, 120, 120, 120]
#     tolerances = [x * np.pi / 180 for x in tolerances_deg]

#     for i in range(6):
#         joint_constraint = moveit_msgs.msg.JointConstraint()
#         joint_constraint.joint_name = joints_name[i]
#         joint_constraint.position = joints_goal[i]
#         joint_constraint.tolerance_above = tolerances[i]
#         joint_constraint.tolerance_below = tolerances[i]
#         joint_constraint.weight = 1.0
#         constraints.joint_constraints.append(joint_constraint)

#     # 制約をMoveGroupに適用
#     moveit_client.set_path_constraints(constraints)

#     # Cartesian pathの計算
#     waypoints = [current_pose]
#     (plan, fraction) = moveit_client.compute_cartesian_path(waypoints, eef_step=0.008, jump_threshold=0.0)
#     rospy.loginfo("Computed Cartesian path with fraction: %f", fraction)

#     # プランの確認
#     if not plan or len(plan.joint_trajectory.points) == 0:
#         rospy.logerr("Plan was not created correctly.")
#         return False

#     rospy.loginfo("Plan: %s", plan)

#     # プランの詳細を出力
#     for point in plan.joint_trajectory.points:
#         rospy.loginfo("Positions: %s", point.positions)
#         rospy.loginfo("Velocities: %s", point.velocities)
#         rospy.loginfo("Accelerations: %s", point.accelerations)
#         rospy.loginfo("Time from start: %s", point.time_from_start)

#     # プランの実行
#     success = moveit_client.execute(plan, wait=True)

#     if success:
#         rospy.loginfo("Plan executed successfully")
#     else:
#         rospy.logwarn("Plan execution failed")

#     # ポーズターゲットを元に戻す
#     moveit_client.set_pose_target(current_pose)
#     moveit_client.go(wait=True)
    
#     # 制約をクリア
#     moveit_client.clear_path_constraints()

#     return success



##robot helpers
# def ik(go_pose, current_euler_x, current_euler_y, current_euler_z, moveit_client):
    
#     # Get current joint states
#     current_joint_values = moveit_client.move_group.get_current_joint_values()
    
#     # Create pose goal with current end effector pose
#     current_pose = moveit_client.move_group.get_current_pose().pose
#     pose_goal = Pose()
#     pose_goal.position.x = current_pose.position.x + go_pose[0]
#     pose_goal.position.y = current_pose.position.y + go_pose[1]
#     pose_goal.position.z = current_pose.position.z + go_pose[2]
#     pose_goal_position = [pose_goal.position.x, pose_goal.position.y, pose_goal.position.z]
    
#     # Convert euler angles to quaternion and add to current orientation
#     goal_euler = [0.0, 0.0, 0.0]
#     goal_euler[0] = current_euler_x #+ go_pose[3]
#     goal_euler[1] = current_euler_y #+ go_pose[4]
#     goal_euler[2] = current_euler_z #+ go_pose[5]
#     goal_euler = np.array(goal_euler)

#     pose_goal.orientation.x ,pose_goal.orientation.y, pose_goal.orientation.z, pose_goal.orientation.w= euler_to_quaternion(goal_euler[0], goal_euler[1], goal_euler[2])   
#     goal_quat = np.array([pose_goal.orientation.x, pose_goal.orientation.y, pose_goal.orientation.z, pose_goal.orientation.w])

#     pose_goal = spatial.Transform(goal_quat, pose_goal_position)
#     print(pose_goal.translation)
#     print(pose_goal.rotation)
#     # moveit_client.goto(pose_goal)
#     # joint_goal = moveit_client.move_group.get_current_joint_values()
#     # waypoints = [pose_goal]
#     # Plan to the new goal
#     success, plan =moveit_client.plan(pose_goal)
#     # plan  = group.plan()
#     # print(plan)
#     print(current_joint_values)
#     joint_goal = plan.joint_trajectory.points[-1].positions
#     print(joint_goal)
    
    
#     # Calculate joint angle differences (current - goal)
#     joint_diffs = np.array([[ goal - current for goal, current in zip(joint_goal, current_joint_values)]])
#     if np.any(np.abs(joint_diffs) > 1):
#         joint_diffs = np.zeros_like(joint_diffs)
    
#     print(joint_diffs)

#     return joint_diffs
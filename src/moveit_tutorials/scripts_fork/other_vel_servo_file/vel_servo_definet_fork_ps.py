#!/usr/bin/env python3
#coding: UTF-8

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import rospy
from geometry_msgs.msg import Pose
import moveit_commander
import tf.transformations
import torchvision.transforms as transforms
from torchvision.transforms import functional as F
import numpy as np
import cv2
from ur_ikfast.ur_ikfast import ur_kinematics
from PIL import Image
import torch
import imageio.v2 as imageio
from geometry_msgs.msg import Vector3
import pandas as pd
import math
import time
import csv
from definet.use_in_vs import DefiNet
from sensor_msgs.msg import Image
# from sensor_msgs.msg import JointState
from cv_bridge import CvBridge
import signal
import sys

import atexit

#for velocity control
from std_msgs.msg import Float64MultiArray
from sensor_msgs.msg import JointState
import sensor_msgs
#for joint states servicecall
from moveit_tutorials.srv import GetCurrentJointVel
#for pose servicecall
from moveit_tutorials.srv import GettfPose
#for switch controller
from controller_manager_msgs.srv import SwitchController

from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

#number of pixels
# nop = 1105920 ###UI camera 1080*1024
# nop = 65536 ###realsense 250 250
nop = 2073600
pinv_int_mat_double = np.empty((6,6))
I_dsr_vec = np.empty((nop, 1))
lmbd = 0.2


device = torch.device("cuda")
net = DefiNet(device=device, input_dim=(3,512,512),
                        conv_param = {'filter_num': 64, 'filter_size': 3, 'pad': 1, 'stride': 1},
                        hidden_size=512, output_size=6,  loss_alfa=1, loss_beta=1).to(device)
params = torch.load('./definet/definet_params_epoch150_full.pt', map_location=torch.device(device))

net.load_state_dict(params)
net.eval()

rmseth = 0.0#13.3

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

def switch_controller(start_controllers, stop_controllers):
    switch_service = rospy.ServiceProxy('/controller_manager/switch_controller', SwitchController)
    resp = switch_service(start_controllers=start_controllers, 
                          stop_controllers=stop_controllers,
                          strictness=2,
                          start_asap=False,
                          timeout=0.0)
    print(resp.ok)



def get_joint_state(data):
    global joint
    joint = []
    joint = data.position
    # print(data.position)
    # print('vel')
    return joint

def switch_to_joint_group_vel():
    switch_controller(['joint_group_vel_controller'], ['scaled_pos_joint_traj_controller'])

def switch_to_scaled_pos():
    switch_controller(['scaled_pos_joint_traj_controller'], ['joint_group_vel_controller'])


def readpickle():
    global pinv_int_mat_double
    pickledata = pd.read_pickle('./pinv_int_mat_pickle/pinv_int_mat_double.pickle')
    pinv_int_mat_double = pickledata.values
    return pinv_int_mat_double

def gen_dsrimvec(): 
    global I_dsr_vec
    global I_dsr_gry
    # I_dsr = imageio.imread('./input_dsrim/kensyo_desired_image.png')
    I_dsr = cv2.imread('./input_dsrim/kensyo_desired_image.png')
    # image_tensor = F.to_tensor(I_dsr).float().to("cuda")
    # gaussina_blur = transforms.GaussianBlur(kernel_size = (5, 5), sigma = (1.0, 1.0))
    # blurred_tensor = gaussina_blur(image_tensor)
    # resized_tensor = F.resize(blurred_tensor, [256, 256], antialias=True)
    # processed_image = F.to_pil_image(resized_tensor)
    # I_dsr_vec = np.array(processed_image).transpose(2, 0, 1)

    I_dsr_gry = cv2.cvtColor(I_dsr, cv2.COLOR_BGR2GRAY)
    I_dsr_arr = np.array(I_dsr_gry, dtype = 'float64')
    I_dsr_gry = I_dsr_arr.reshape(-1,1)

    I_dsr_vec = np.array(I_dsr).transpose(2, 0, 1)
    I_dsr_vec = np.expand_dims(I_dsr_vec, axis=0)
    return I_dsr_vec, I_dsr_gry


def euler_to_quaternion(euler):
    """Convert Euler Angles to Quaternion

    euler: geometry_msgs/Vector3
    quaternion: geometry_msgs/Quaternion
    """
    q = tf.transformations.quaternion_from_euler(euler.x, euler.y, euler.z)
    return q[0], q[1], q[2], q[3]

def quaternion_to_euler(current_pose):
    """Convert Quaternion to Euler Angles

    quarternion: geometry_msgs/Quaternion
    euler: geometry_msgs/Vector3
    """
    e = tf.transformations.euler_from_quaternion((current_pose[0],current_pose[1],current_pose[2],current_pose[3]))
    return e[0], e[1], e[2]




def signal_handler(sig, frame):
    global time_series
    global rmse_data
    
    global base_joint_data
    global shoulder_joint_data
    global elbow_joint_data
    global wrist1_joint_data
    global wrist2_joint_data
    global wrist3_joint_data
    
    global joint_vel_values_data
    
    global pose_data
    global dist_data

    global dist_trans_x
    global dist_trans_y
    global dist_trans_z
    global dist_rot_x
    global dist_rot_y
    global dist_rot_z

    
    vel_input.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    vel_pub.publish(vel_input)
    print('stop command sent')

    
    filename = './servo_data/loop_rmse_data.csv'
    filename2 = './servo_data/joint_vel_data.csv'
    filename3 = './servo_data/pose_data.csv'
    with open (filename, 'w') as f, open(filename2, 'w')as f2, open(filename3, 'w')as f3:
        writer = csv.writer(f)
        writer.writerow(rmse_data)
        writer2 = csv.writer(f2)
        writer2.writerow(joint_vel_values_data)
        writer3 = csv.writer(f3)
        writer3.writerow(pose_data)

    #generate graph
    fig_rmse = plt.figure()
    plt.xlabel('Time[s]')
    plt.ylabel('RMSE')
    plt.plot(time_series, rmse_data, 'b-')
    plt.ylim([rmseth, 90])
    plt.grid()
    fig_rmse.savefig('./servo_data/rmse_double.png')
    
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
    
    base_axis_array = np.arange(-0.04, 0.04, 0.01)
    shoulder_axis_array = np.arange(-0.04, 0.04, 0.01)
    elbow_axis_array = np.arange(-0.04, 0.04, 0.01)
    wrist1_axis_array = np.arange(-0.04, 0.04, 0.01)
    wrist2_axis_array = np.arange(-0.04, 0.04, 0.01)
    wrist3_axis_array = np.arange(-0.04, 0.04, 0.01) 
    
    #グラフの目盛りのスケールを合わせる
    ax1.set_yticks(base_axis_array)
    ax2.set_yticks(shoulder_axis_array)
    ax3.set_yticks(elbow_axis_array)
    ax4.set_yticks(wrist1_axis_array)
    ax5.set_yticks(wrist2_axis_array)
    ax6.set_yticks(wrist3_axis_array)
    
    #スケールを合わせたグラフを保存
    fig.savefig('./servo_data/joint_values_double_scaled.png')
    
    fig_dist = plt.figure()
    plt.xlabel('Time[s]')
    plt.ylabel('Three-Dimensional Distance[mm]')
    plt.plot(time_series, dist_data, 'b-')
    plt.grid()
    fig_dist.savefig('./servo_data/3dposedist.png')


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
    sys.exit(0)

def main(msg):
    global pinv_int_mat_double
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

    global joint

 
    # rmse = 100
    # group_name = "manipulator"
    # move_group = moveit_commander.MoveGroupCommander(group_name)
    # ur5e_arm = ur_kinematics.URKinematics('ur5e')
    

    
    with open('./dsrth_result/desired_pose.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            desired_pose = [float(x) for x in row]
        
    image_raw = msg
    bridge = CvBridge()
    bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
    # bgr = bgr[ 422 : 678, 862 : 1118 ] 
    # bgr = bgr[ 200 : 712, 750 : 1262 ] 
    # bgr = bridge.imgmsg_to_cv2(image_raw, 'mono8') ###UI camera

    # image_tensor = F.to_tensor(bgr).float().to("cuda")
    # gaussina_blur = transforms.GaussianBlur(kernel_size = (5, 5), sigma = (1.0, 1.0))
    # blurred_tensor = gaussina_blur(image_tensor)
    # resized_tensor = F.resize(blurred_tensor, [256, 256], antialias=True)
    # processed_image = F.to_pil_image(resized_tensor)
    # I_vec = np.array(processed_image).transpose(2, 0, 1)

    I_vec = np.array(bgr).transpose(2, 0, 1)
    I_vec = np.expand_dims(I_vec, axis=0)
        
    # グレースケール化
    # gry = np.mean(I_dsr_vec, axis=0).astype(np.uint8)
    # I_dsr_gry = gry.reshape(-1,1)

    # gry2 =  np.mean(I_vec, axis=0).astype(np.uint8)
    # I_gry = gry2.reshape(-1,1)

    I_gry = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
    I_arr = np.array(I_gry, dtype = 'float64')
    I_gry = I_arr.reshape(-1,1)

    #画像偏差計算
    dI = I_dsr_gry - I_gry ###目標-現在
    dI2 = dI**2
    Isum = np.sum(dI2)
    rmse = math.sqrt(Isum / nop)
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
    if euler_z < 0 :
        euler_z = euler_z + 6.283


    
    if rmse < rmseth or (time.time() - start_time) > 120:
    # if abs(desired_pose[0] - current_pose_x) < 0.0002 and abs(desired_pose[1] - current_pose_y) < 0.0002:
        print('stop')
        vel_input.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        vel_pub.publish(vel_input)
        print('stop command sent')
        
        filename = './servo_data/loop_rmse_data.csv'
        filename2 = './servo_data/joint_vel_data.csv'
        filename3 = './servo_data/pose_data.csv'
        with open (filename, 'w') as f, open(filename2, 'w')as f2, open(filename3, 'w')as f3: 
            writer = csv.writer(f)
            writer.writerow(rmse_data)
            writer2 = csv.writer(f2)
            writer2.writerow(joint_vel_values_data)
            writer3 = csv.writer(f3)
            writer3.writerow(pose_data)

        #generate graph
        fig_rmse = plt.figure()
        plt.xlabel('Time[s]')
        plt.ylabel('RMSE')
        plt.plot(time_series, rmse_data, 'b-')
        plt.ylim([rmseth, 90])
        plt.grid()
        fig_rmse.savefig('./servo_data/rmse_double.png')
        
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
        
        base_axis_array = np.arange(-0.04, 0.04, 0.01)
        shoulder_axis_array = np.arange(-0.04, 0.04, 0.01)
        elbow_axis_array = np.arange(-0.04, 0.04, 0.01)
        wrist1_axis_array = np.arange(-0.04, 0.04, 0.01)
        wrist2_axis_array = np.arange(-0.04, 0.04, 0.01)
        wrist3_axis_array = np.arange(-0.04, 0.04, 0.01) 
        
        #グラフの目盛りのスケールを合わせる
        ax1.set_yticks(base_axis_array)
        ax2.set_yticks(shoulder_axis_array)
        ax3.set_yticks(elbow_axis_array)
        ax4.set_yticks(wrist1_axis_array)
        ax5.set_yticks(wrist2_axis_array)
        ax6.set_yticks(wrist3_axis_array)
        
        #スケールを合わせたグラフを保存
        fig.savefig('./servo_data/joint_values_double_scaled.png')
        
        fig_dist = plt.figure()
        plt.xlabel('Time[s]')
        plt.ylabel('Three-Dimensional Distance[mm]')
        plt.plot(time_series, dist_data, 'b-')
        plt.grid()
        fig_dist.savefig('./servo_data/3dposedist.png')


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

        rospy.signal_shutdown('finish')
    
    else:
        joint_pub = rospy.Subscriber('/joint_states', JointState, get_joint_state)
        # pose = Pose()
        # joint_values = move_group.get_current_joint_values()
        # pose_quat = ur5e_arm.forward(joint_values)
        # definetへ
        
        dr = net.forward(I_dsr_vec, I_vec)
        # dr = net.forward(I_dsr_vec, I_dsr_vec)
        dr = dr.to("cpu").detach().numpy()
        # dr = dr.T
        dr = lmbd*dr
        current_pose = (current_pose_x, current_pose_y, current_pose_z, euler_x, euler_y, euler_z)
        for_pose = current_pose + dr

        for_pose_euler = Vector3(for_pose[0, 3], for_pose[0, 4], for_pose[0, 5])
        # pose.position.x = for_pose[0, 0] #差0.05
        # pose.position.y = for_pose[0, 1] #差0.02
        # pose.position.z = for_pose[0, 2] #差0.05
        # pose.orientation.x, pose.orientation.y, pose.orientation.z ,pose.orientation.w = euler_to_quaternion(for_pose_euler)
        # kin_pose = (pose.position.x, pose.position.y, pose.position.z, pose.orientation.x, pose.orientation.y, pose.orientation.z ,pose.orientation.w)
        # for_theta = ur5e_arm.inverse(kin_pose, all_solutions=False, q_guess=joint_values)
        # vel_input.position = for_theta
        # vel_input.data = lmbd*(for_theta - joint_values)


        # # ランダムなポーズを目標として設定
        # move_group.set_pose_target(target_pose)

        # vel_input.data = 0.01*(np.dot(pinv_int_mat_double, dr)) 
        # vel_input.data = lmbd*dr
        vel_pub.publish(vel_input) #プログラミングROS P109では速度の値だけf分岐させてpublish部分はif分岐の外においてた

        # # 移動計画と実行
        # #wait=Trueにすることで動作が終わるまで待機



        #serviceで関節角速度取得
        rospy.wait_for_service('getvel')
        getvel_client = rospy.ServiceProxy('getvel', GetCurrentJointVel)
        resvel = getvel_client()
        # resvel = move_group.get_current_joint_values()
        # # print(resvel)

        # current_base_vel = resvel[0]
        # current_shoulder_vel = resvel[1]
        # current_elbow_vel = resvel[2]
        # current_wrist1_vel = resvel[3]
        # current_wrist2_vel = resvel[4]
        # current_wrist3_vel = resvel[5]

        
        current_base_vel = resvel.current_joint_vel[0]
        current_shoulder_vel = resvel.current_joint_vel[1]
        current_elbow_vel = resvel.current_joint_vel[2]
        current_wrist1_vel = resvel.current_joint_vel[3]
        current_wrist2_vel = resvel.current_joint_vel[4]
        current_wrist3_vel = resvel.current_joint_vel[5]
        
        ###pose が単位mで出力される
        ### 距離がしきい値以上で速度計算される場合に距離算出+append
        # dist = 1000*math.sqrt((desired_pose[0] - current_pose_x)**2 + (desired_pose[1] - current_pose_y)**2 + (desired_pose[2] - current_pose_z)**2)
        dist = 1000*math.sqrt((desired_pose[0] - current_pose_x)**2 + (desired_pose[2] - current_pose_z)**2) ###x,z軸方向だけの距離を出す

        trans_x_dist = 1000*math.sqrt((desired_pose[0] - current_pose_x)**2)
        trans_y_dist = 1000*math.sqrt((desired_pose[1] - current_pose_y)**2)
        trans_z_dist = 1000*math.sqrt((desired_pose[2] - current_pose_z)**2)
        rot_x_dist = math.sqrt((desired_pose[3] - euler_x)**2)*180 / math.pi
        rot_y_dist = math.sqrt((desired_pose[4] - euler_y)**2)*180 / math.pi
        rot_z_dist = math.sqrt((desired_pose[5] - euler_z)**2)*180 / math.pi


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

        
        return rmse, time_series, rmse_data, base_joint_data, shoulder_joint_data, elbow_joint_data, wrist1_joint_data, wrist2_joint_data, wrist3_joint_data, joint_vel_values_data, pose_data, dist_data,dist_trans_x, dist_trans_y, dist_trans_z, dist_rot_x, dist_rot_y, dist_rot_z
        

    
if __name__ == '__main__':
    try:
        rospy.init_node('servo_node')
        rospy.loginfo('servo node started')
        switch_to_joint_group_vel()
        atexit.register(switch_to_scaled_pos)
        readpickle()
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

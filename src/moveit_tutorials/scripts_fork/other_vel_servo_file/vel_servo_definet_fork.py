#!/usr/bin/env python3
#coding: UTF-8

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import rospy
import moveit_commander
import tf.transformations
import torchvision.transforms as transforms
from torchvision.transforms import functional as F
import numpy as np
import cv2
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
lmbd = 0.25


device = torch.device("cuda")
net = DefiNet(device=device, input_dim=(3,512,512),
                        conv_param = {'filter_num': 64, 'filter_size': 3, 'pad': 1, 'stride': 1},
                        hidden_size=512, output_size=6,  loss_alfa=1, loss_beta=1).to(device)
# params = torch.load('./definet/definet_params_epoch150_full.pt', map_location=torch.device(device))
# params = torch.load('./definet/definet_params_epoch150_input.pt', map_location=torch.device(device))
# params = torch.load('./definet/definet_params_epoch250_remove_normal.pt', map_location=torch.device(device))
params = torch.load('./definet/definet_params_epoch140_input.pt', map_location=torch.device(device))

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

error_rot_axis = []
error_rot_ang = []

def switch_controller(start_controllers, stop_controllers):
    switch_service = rospy.ServiceProxy('/controller_manager/switch_controller', SwitchController)
    resp = switch_service(start_controllers=start_controllers, 
                          stop_controllers=stop_controllers,
                          strictness=2,
                          start_asap=False,
                          timeout=0.0)
    print(resp.ok)

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
    filename4 = './servo_data/3dist.csv'
    with open (filename, 'w') as f, open(filename2, 'w')as f2, open(filename3, 'w')as f3 , open(filename4, 'w')as f4:
        writer = csv.writer(f)
        writer.writerow(rmse_data)
        writer2 = csv.writer(f2)
        writer2.writerow(joint_vel_values_data)
        writer3 = csv.writer(f3)
        writer3.writerow(pose_data)
        writer4 = csv.writer(f4)
        writer4.writerow(dist_data)

    #generate graph
    fig_rmse = plt.figure()
    plt.xlabel('Time[s]')
    plt.ylabel('RMSE')
    plt.plot(time_series, rmse_data, 'b-')
    plt.ylim([rmseth, 90])
    plt.grid()
    fig_rmse.savefig('./servo_data/rmse_double.png')

    fig_rmse_it = plt.figure()
    iteration = np.linspace(0, len(rmse_data), len(rmse_data))
    plt.xlabel('iteration')
    plt.ylabel('RMSE')
    plt.plot(iteration, rmse_data, 'b-')
    plt.ylim([rmseth, 90])
    plt.grid()
    fig_rmse_it.savefig('./servo_data/rmse_iteration.png')
    
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
    
    print('3dist = %f' % dist_data[-1])
    fig_dist = plt.figure()
    plt.xlabel('Time[s]')
    plt.ylabel('Three-Dimensional Distance[mm]')
    plt.plot(time_series, dist_data, 'b-')
    plt.grid()
    fig_dist.savefig('./servo_data/3dposedist.png')

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

 
    # rmse = 100

    
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


    
    if rmse < rmseth or len(rmse_data) > 1000:# (time.time() - start_time) > 33:
     # if abs(desired_pose[0] - current_pose_x) < 0.0002 and abs(desired_pose[1] - current_pose_y) < 0.0002:
        print('stop')
        vel_input.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        vel_pub.publish(vel_input)
        print('stop command sent')

        dsr_img = cv2.imread('./input_dsrim/kensyo_desired_image.png', cv2.IMREAD_GRAYSCALE)

        image_raw = msg
        bridge = CvBridge()
        bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
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

        with open (filename, 'w') as f, open(filename2, 'w')as f2, open(filename3, 'w')as f3, open(filename4, 'w')as f4, open(filename5, 'w')as f5:
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
        plt.ylim([rmseth, 50])
        plt.grid()
        fig_rmse_it.savefig('./servo_data/rmse_iteration.png')

        fig_dist = plt.figure()
        iteration = np.linspace(0, len(dist_data), len(dist_data))
        plt.xlabel('iteration')
        plt.ylabel('Distance in XZ plane[mm]')
        plt.plot(iteration, dist_data, 'b-')
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
        # plt.ylim([0.0, 5.0])
        plt.grid()
        rot_axis_dist.savefig('./servo_data/rot_axis.png')

        rot_ang_dist = plt.figure()
        iteration = np.linspace(0, len(error_rot_ang), len(error_rot_ang))
        plt.xlabel('iteration')
        plt.ylabel('Error of rotation angle[deg]')
        plt.plot(iteration, error_rot_ang, 'b-')
        # plt.ylim([0.0, 5.0])
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
        # definetへ
        dr = net.forward(I_dsr_vec, I_vec)
        # dr = net.forward(I_dsr_vec, I_dsr_vec)
        dr = dr.to("cpu").detach().numpy()
        dr = dr.T
        # dr = lmbd*dr

        # euler_x = dr[:, 3]
        # euler_y = dr[:, 4]
        # euler_z = dr[:, 5]
        # euler = Vector3(euler_x, euler_y, euler_z)    
        # current_pose = move_group.get_current_pose().pose    
        # target_pose = current_pose
        # orientation_x, orientation_y, orientation_z ,orientation_w = euler_to_quaternion(euler)


        # target_pose.position.x = current_pose.position.x  +  dr[:, 0].item()                  ###一回目の中継地点
        # target_pose.position.y = current_pose.position.y  +  dr[:, 1].item()      
        # target_pose.position.z = current_pose.position.z  +  dr[:, 2].item()        
        # target_pose.orientation.x = current_pose.orientation.x + orientation_x
        # target_pose.orientation.y = current_pose.orientation.y + orientation_y
        # target_pose.orientation.z = current_pose.orientation.z + orientation_z
        # target_pose.orientation.w = current_pose.orientation.w + orientation_w

        # # ランダムなポーズを目標として設定
        # move_group.set_pose_target(target_pose)
        vel_input.data = lmbd*(np.dot(pinv_int_mat_double, dr)) 
        # vel_input.data = lmbd*dr
        vel_pub.publish(vel_input) #プログラミングROS P109では速度の値だけf分岐させてpublish部分はif分岐の外においてた

        # # 移動計画と実行
        # #wait=Trueにすることで動作が終わるまで待機
        # move_group.go(wait=True)



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
        dist = 1000*math.sqrt((desired_pose[0] - current_pose_x)**2 + (desired_pose[1] - current_pose_y)**2+(desired_pose[2] - current_pose_z)**2) ###x,z軸方向だけの距離を出す

        trans_x_dist = 1000*math.sqrt((desired_pose[0] - current_pose_x)**2)
        trans_y_dist = 1000*math.sqrt((desired_pose[1] - current_pose_y)**2)
        trans_z_dist = 1000*math.sqrt((desired_pose[2] - current_pose_z)**2)
        rot_x_dist = math.sqrt((desired_pose[3] - euler_x)**2)*180 / math.pi
        rot_y_dist = math.sqrt((desired_pose[4] - euler_y)**2)*180 / math.pi
        rot_z_dist = math.sqrt((desired_pose[5] - euler_z)**2)*180 / math.pi

        desired_quaternion = [0, 0, 0, 0]
        desired_quaternion[0], desired_quaternion[1], desired_quaternion[2], desired_quaternion[3] = euler_to_quaternion(desired_pose[3], desired_pose[4], desired_pose[5])
        desired_quaternion = np.array(desired_quaternion)
        current_quaternion = np.abs(np.array(rot))


        error_rotation_axis = np.abs((np.arccos(desired_quaternion[0]*current_quaternion[0]+desired_quaternion[1]*current_quaternion[1]+desired_quaternion[2]*current_quaternion[2]))*180 / math.pi)  
        error_rotation_angle = np.abs(np.arccos(desired_quaternion[3])/2- np.arccos(current_quaternion[3])/2)*180 / math.pi



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
        pose_data.append([current_pose_x, current_pose_y, current_pose_z, euler_x, euler_y, euler_z,])
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

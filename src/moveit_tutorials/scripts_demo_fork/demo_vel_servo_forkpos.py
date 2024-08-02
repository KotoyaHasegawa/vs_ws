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

from jikken_data_python.demo_data import DATA

#number of pixels
# nop = 2073600
nop = 230400
pinv_int_mat_double = np.empty((6,6))
pinv_int_manip = np.empty((6,6))
I_dsr_vec = np.empty((nop, 1))
lmbd = 0.25

rmseth = 10.0 #5.0 
iteration = 1000

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

# Global variable to store the last received message
last_msg = None


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

    if last_msg is None:
        print("No image data received.")
        sys.exit(1)


    print('stop')
    vel_input.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    vel_pub.publish(vel_input)
    print('stop command sent')

    dsr_img = cv2.imread('./input_dsrim/kensyo_desired_image.png', cv2.IMREAD_GRAYSCALE)
    init_img = cv2.imread('./servo_data/kensyo_initial_image.png', cv2.IMREAD_GRAYSCALE)

    image_raw = last_msg
    bridge = CvBridge()
    bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
    bgr = bgr[ 200 : 560 ,720 : 1360 ]

    get_data = DATA(bgr, dsr_img, init_img, rmse_data, dist_trans_x, dist_trans_y, dist_trans_z, 
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

    global last_msg  # Use the global variable
    last_msg = msg

    
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
    # print("\n-----------------------------\n")
    # print("\n-----------------------------\n")
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

   
    if rmse < rmseth or len(rmse_data) > iteration:#(time.time() - start_time) > 33.333:
    # if abs(desired_pose[0] - current_pose_x) < 0.0002 and abs(desired_pose[1] - current_pose_y) < 0.0002:
        print('stop')
        vel_input.data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        vel_pub.publish(vel_input)
        print('stop command sent')

        dsr_img = cv2.imread('./input_dsrim/kensyo_desired_image.png', cv2.IMREAD_GRAYSCALE)
        init_img = cv2.imread('./servo_data/kensyo_initial_image.png', cv2.IMREAD_GRAYSCALE)

        image_raw = msg
        bridge = CvBridge()
        bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8') 
        bgr = bgr[ 200 : 560 ,720 : 1360 ]

        get_data = DATA(bgr, dsr_img, init_img, rmse_data, dist_trans_x, dist_trans_y, dist_trans_z, 
                 dist_rot_x, dist_rot_y, dist_rot_z, error_rot_axis, error_rot_ang, dist_data, 
                 time_series, base_joint_data, shoulder_joint_data, elbow_joint_data, wrist1_joint_data, wrist2_joint_data, wrist3_joint_data, 
                 rmseth, iteration)
        
        get_data.main()

        rospy.signal_shutdown('finish')
    
    else:

        # マニピュレータヤコビアン
        go_pose = lmbd*(np.dot(pinv_int_mat_double, dI)) 
        vel_input.data = np.dot(pinv_int_manip, go_pose)
        # print(vel_input.data)
        vel_pub.publish(vel_input) #プログラミングROS P109では速度の値だけf分岐させてpublish部分はif分岐の外においてた

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
#!/usr/bin/env python3
# coding: UTF-8

import sys
from math import pi

import moveit_commander
import rospy

from tf import transformations
from geometry_msgs.msg import Vector3

# import random
import numpy as np

from time import sleep

def quaternion_to_euler(current_pose):
    """Convert Quaternion to Euler Angles

    quarternion: geometry_msgs/Quaternion
    euler: geometry_msgs/Vector3
    """
    e = transformations.euler_from_quaternion((current_pose.orientation.x,current_pose.orientation.y,current_pose.orientation.z,current_pose.orientation.w))
    return Vector3(x=e[0], y=e[1], z=e[2])

def Move():
	moveit_commander.roscpp_initialize(sys.argv)
	move_group = moveit_commander.MoveGroupCommander("manipulator")
	move_group.set_max_velocity_scaling_factor(value=0.2)
	move_group.set_max_acceleration_scaling_factor(value=0.2)
	current_pose = move_group.get_current_pose().pose
	
	# joint_goal = [1.514, -1.165, 0.746, 0.433, 0.986, -3.16]

	joint_goal_deg = [-30.01, -76.55, -111.21, -171.46, -31.68, -0.30] ### A
	# joint_goal_deg = [-29.39, -78.67, -113.11, -171.35, -29.20, 3.66] ### B
	# joint_goal_deg = [-33.88, -75.62, -116.95, -171.77, -36.08, 3.76] ### C
	# joint_goal_deg = [-32.62, -74.11, -114.58, -168.71, -33.65, -2.46] ### D
	# joint_goal_deg = [-29.42, -77.35, -114.90, -164.93, -30.95, -2.23] ### E
	# joint_goal_deg = [-30.49, -77.80, -115.97, -168.25, -29.30, 0.54] ### F
	# joint_goal_deg = [-31.73, -77.25, -119.13, -164.71, -29.89, 1.58] ### G
	# joint_goal_deg = [-34.34, -73.32, -116.43, -168.56, -34.16, -4.19] ### H
 
	# joint_goal_deg = [-11.34, -67.75, -117.81, -177.69, -10.65, 2.81] ##AA-
	# joint_goal_deg = [-13.26, -63.36, -120.23, -179.24, -12.55, 2.38] ### BB
	# joint_goal_deg = [-14.04, -62.40, -125.56, -174.66, -13.31, 2.17] ### CC
	# joint_goal_deg = [-12.28, -65.87, -122.40, -174.69, -11.55, 2.53] ### DD
	# joint_goal_deg = [-12.39, -65.35, -120.78, -176.85, -11.68, 2.54] ##EE
	# joint_goal_deg = [-12.26, -65.87, -122.41, -174.69, -11.55, 2.53] ### FF
	# joint_goal_deg = [-13.07, -64.51, -125.64, -172.59, -12.34, 2.32] ### GG
	# joint_goal_deg = [-13.73, -62.46, -120.96, -179.30, -13.05, 2.29] ### HH

	# joint_goal_deg = [-31.13, -85.01, -129.31, -147.45, -27.36, 0.53] ##spexial
	# joint_goal_deg = [-19.66, -74.24, -135.71, -152.71, -18.89, 3.63] 
	# joint_goal_deg = [-26.76, -104.29, -139.45, -118.43, -22.45, -0.82] 
	# joint_goal_deg = [-21.56, -98.50, -144.79, -117.50, -20.75, 0.31] 
	

	# joint_goal_deg = [87.25, -112.66, 88.14, 23.24, 85.93, 180.04] ### B5
	# joint_goal_deg = [65.15, -122.07, 96.74, 24.60, 63.53, 179.71] ### B6
	# joint_goal_deg = [79.94, -118.54, 104.17, 13.62, 78.90, 180.73] ### B7 
	# joint_goal_deg = [88.57, -114.13, 98.16, 15.18, 87.51, 180.64] ### B8 
	# joint_goal_deg = [-30.95, -78.76, -112.90, -179.19, -31.58, 7.78] ### 見下ろす
	# joint_goal_deg = [-31.43, -73.00, -120.97, -149.38, -32.25, -14.48] ##見上げる
	# joint_goal_deg = [-33.46, -74.95, -116.78, -167.78, -43.69, 4.00] ##左を見る
	# joint_goal_deg = [-30.02, -77.81, -114.57, -168.06, -22.22, -3.79] ##右を見る
	# joint_goal_deg = [-31.20, -76.61, -115.37, -169.00, -31.03, 12.04] ##回転
	# joint_goal_deg = [-31.17, -76.66, -115.34, -169.05, -31.83, -12.76] ##回転２

 
	joint_goal = [x * pi/180 for x in joint_goal_deg]
	# print(joint_goal_deg)
	# joint_goal = [-0.5385950247394007, -1.3360947233489533, -1.9782096147537231, -2.9876705608763636, -0.5343516508685511, 0.010870436206459999]#remove

	move_group.set_joint_value_target(joint_goal)
	# print(joint_goal)
	move_group.go(wait=True)
	print(move_group.get_current_pose())
	current_pose = move_group.get_current_pose().pose
	# print(move_group.get_end_effector_link())
	# print(move_group.get_current_rpy(end_effector_link = 'tool0'))
	print(quaternion_to_euler(current_pose))
	print('moved to initial pose')
	moveit_commander.roscpp_shutdown()

if __name__ == "__main__":
	rospy.init_node('init_pose')
	Move()
#!/usr/bin/env python3
# coding: UTF-8

import sys
from math import pi

import moveit_commander
import rospy
import csv

from tf import transformations
from geometry_msgs.msg import Vector3

import moveit_msgs.msg

import random
import os
import numpy as np


from ur_ikfast.ur_ikfast import ur_kinematics


def ik(current_joint,pose_quat):
    ur5e_arm = ur_kinematics.URKinematics('ur5e')
    joint_angles = current_joint # in radians
    joint_angles_quat = ur5e_arm.inverse(pose_quat, False, q_guess=joint_angles)
    print("inverse() one from quat", joint_angles_quat)
    return (joint_angles_quat)



def quaternion_to_euler(current_pose):
    """Convert Quaternion to Euler Angles

    quarternion: geometry_msgs/Quaternion
    euler: geometry_msgs/Vector3
    """
    e = transformations.euler_from_quaternion((current_pose.orientation.x,current_pose.orientation.y,current_pose.orientation.z,current_pose.orientation.w))
    return Vector3(x=e[0], y=e[1], z=e[2])

def euler_to_quaternion(euler):
    """Convert Euler Angles to Quaternion

    euler: geometry_msgs/Vector3
    quaternion: geometry_msgs/Quaternion
    """
    q = transformations.quaternion_from_euler(euler.x, euler.y, euler.z)
    return q[0], q[1], q[2], q[3]

def pose_to_rigid_transformation_matrix(pose):
    """
    pose: [x, y, z, roll, pitch, yaw]
          並進ベクトルとオイラー角を含む1次元配列
          x, y, z: 並進成分
          roll, pitch, yaw: オイラー角（ラジアン）
    """
    # 並進ベクトルを抽出
    translation = np.array(pose[:3]).reshape(3, 1)
    
    # オイラー角（ラジアン）を抽出
    roll, pitch, yaw = pose[3:]
    
    # 回転行列を計算
    R_x = np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll), np.cos(roll)]])
    
    R_y = np.array([[np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])
    
    R_z = np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw), np.cos(yaw), 0],
                    [0, 0, 1]])
    
    # 合成回転行列
    rotation_matrix = np.dot(R_z, np.dot(R_y, R_x))
    
    # 3x4のリジッド変換行列を作成
    transform_matrix = np.hstack((rotation_matrix, translation))
    
    return transform_matrix

def Move():
	moveit_commander.roscpp_initialize(sys.argv)
	move_group = moveit_commander.MoveGroupCommander("manipulator")
	move_group.set_max_velocity_scaling_factor(value=0.2)
	move_group.set_max_acceleration_scaling_factor(value=0.2)
	current_pose = move_group.get_current_pose().pose
	current_joint = move_group.get_current_joint_values()

	# with open('./dsrth_result/desired_pose.csv', 'r') as f:
	# 	reader = csv.reader(f)
	# 	for row in reader:
	# 		desired_pose = [float(x) for x in row]

	with open('./dsrth_result/desired_pose_mid.csv', 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			desired_pose = [float(x) for x in row]


    # #本格
	# current_pose.position.x = desired_pose[0] #+ 0.025 #差+-0.025
	# current_pose.position.y = desired_pose[1] #差0.02
	# current_pose.position.z = desired_pose[2] #+ 0.025#差+-0.025
	# euler_x = desired_pose[3]#差5度
	# euler_y = desired_pose[4]#差5度
	# euler_z = desired_pose[5]#差5度
	


	# # if euler_z > 3.1415 :
	# # 	euler_z = euler_z - 6.283	

	
	# shoki_pose = ["shoki  pose",current_pose.position.x ,current_pose.position.y,  current_pose.position.z, euler_x, euler_y ,euler_z]
	# shoki_delta = ["shoki  delata",current_pose.position.x - desired_pose[0] ,current_pose.position.y - desired_pose[1],  current_pose.position.z - desired_pose[2]
	# 			,euler_x - desired_pose[3], euler_y - desired_pose[4],euler_z - desired_pose[5]]
	# shoki_delta = [shoki_delta[0]] + [shoki_delta[1],shoki_delta[2],shoki_delta[3]] + [float(x) * 180 / pi for x in shoki_delta[4:]]
	# filename = './servo_data/shoki_pose.csv'
	# with open (filename, 'w') as f:
	# 	writer = csv.writer(f)
	# 	writer.writerow(["Name", "x", "y", "z", "rx", "ry", "rz"])
	# 	writer.writerow(shoki_pose)
	# 	writer.writerow(shoki_delta)

	# euler = Vector3(euler_x, euler_y, euler_z)
	
	# current_pose.orientation.x, current_pose.orientation.y, current_pose.orientation.z ,current_pose.orientation.w = euler_to_quaternion(euler)
	
	go_joint = ik(current_joint,[current_pose.position.x, current_pose.position.y, current_pose.position.z, 
				current_pose.orientation.x,current_pose.orientation.y, current_pose.orientation.z, current_pose.orientation.w])		
	# deff = current_joint - go_joint
	     
	move_group.set_joint_value_target(go_joint)
	print(go_joint)
	move_group.go(wait=True)
	print('moved to desired pose')
	print(move_group.get_current_pose())
	current_pose = move_group.get_current_pose().pose
	print(quaternion_to_euler(current_pose))

	c = quaternion_to_euler(current_pose)
	print(quaternion_to_euler(current_pose))
	current_pose_euler = [current_pose.position.x, current_pose.position.y, current_pose.position.z, c.x, c.y, c.z]
    
	# print(move_group.get_current_rpy())
 
	moveit_commander.roscpp_shutdown()


if __name__ == "__main__":
	rospy.init_node('init_pose')
	Move()
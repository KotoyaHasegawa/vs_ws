#!/usr/bin/env python3
# coding: UTF-8

import sys
from math import pi

import moveit_commander
import rospy
import csv

from tf import transformations
from geometry_msgs.msg import Vector3
from scipy.spatial.transform import Rotation as R

import moveit_msgs.msg

import random
import numpy as np

from time import sleep

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
    return -1*q[0], -1*q[1], -1*q[2], -1*q[3]

def plan_and_excute(target_pose, text, move_group):
	waypoints = [target_pose]
	(plan, fraction) = move_group.compute_cartesian_path(waypoints, eef_step=0.06, jump_threshold=0.00)
	move_group.execute(plan, wait=True)
	move_group.set_pose_target(target_pose)
	move_group.go(wait=True)
	print("\n-----------------------------\n")
	print("\n-----------------------------\n")
	print(text)
	print("\n-----------------------------\n")
	print("\n-----------------------------\n")

def Move():
	moveit_commander.roscpp_initialize(sys.argv)
	move_group = moveit_commander.MoveGroupCommander("manipulator")
	move_group.set_max_velocity_scaling_factor(value=0.2)
	move_group.set_max_acceleration_scaling_factor(value=0.2)
	current_pose = move_group.get_current_pose().pose


	with open('./dsrth_result/withdraw/desired_pose.csv', 'r') as f:
		reader = csv.reader(f)
		for row in reader:
			desired_pose = [float(x) for x in row]

	# with open('./dsrth_result/withdraw/desired_pose_mid.csv', 'r') as f:
	# 	reader = csv.reader(f)
	# 	for row in reader:
	# 		desired_pose = [float(x) for x in row]

	# with open('./dsrth_result/withdraw/desired_pose_down.csv', 'r') as f:
	# 	reader = csv.reader(f)
	# 	for row in reader:
	# 		desired_pose = [float(x) for x in row]
        

    #本格
	current_pose.position.x = random.uniform(desired_pose[0] - 0.025, desired_pose[0] + 0.025) #差+-0.025
	current_pose.position.y = desired_pose[1] #差0.02
	current_pose.position.z = random.uniform(desired_pose[2] - 0.025, desired_pose[2] + 0.025)#差+-0.025
	# euler_x = random.uniform(desired_pose[3] - 0.04366, desired_pose[3] + 0.04366)#差5度
	# euler_y = random.uniform(desired_pose[4] - 0.04366, desired_pose[4] + 0.04366)#差5度
	# euler_z = random.uniform(desired_pose[5] - 0.04366, desired_pose[5] + 0.04366)#差5度


	# current_pose.position.x = desired_pose[0] #+ 0.01 #差+-0.025
	# current_pose.position.y = desired_pose[1] #差0.02
	# current_pose.position.z = desired_pose[2] #+ 0.01#差+-0.025
	euler_x = desired_pose[3]#差5度
	euler_y = desired_pose[4]#差5度
	euler_z = desired_pose[5]#差5度

	if euler_z > 0 :
		euler_z = euler_z - 6.283	

	if desired_pose[5] > 0 :
		desired_pose[5] = desired_pose[5] - 6.283
	
	shoki_pose = ["shoki  pose",current_pose.position.x ,current_pose.position.y,  current_pose.position.z, euler_x, euler_y ,euler_z]
	shoki_delta = ["shoki  delata",current_pose.position.x - desired_pose[0] ,current_pose.position.y - desired_pose[1],  current_pose.position.z - desired_pose[2]
				,euler_x - desired_pose[3], euler_y - desired_pose[4],euler_z - desired_pose[5]]
	shoki_delta = [shoki_delta[0]] + [shoki_delta[1],shoki_delta[2],shoki_delta[3]] + [float(x) * 180 / pi for x in shoki_delta[4:]]
	filename = './servo_data/shoki_pose.csv'
	with open (filename, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["Name", "x", "y", "z", "rx", "ry", "rz"])
		writer.writerow(shoki_pose)
		writer.writerow(shoki_delta)

	if euler_z < 0 :
		euler_z = euler_z + 6.283	
	
    #remove
	# current_pose.position.x = random.uniform(-0.19819, -0.14819) #差+-0.025
	# current_pose.position.y = 0.36056842392143607 #差0.02
	# current_pose.position.z = random.uniform(0.36766, 0.41766) #差+-0.025
	# euler_x = random.uniform(1.536355, 1.6236815)#差5度
	# euler_y = random.uniform(-0.038589, 0.048737)#差5度
	# euler_z = random.uniform(3.093573, 3.180895)#差5度
	# # if euler_z > 3.1415 :
	# # 	euler_z = euler_z - 6.283

	euler = Vector3(euler_x, euler_y, euler_z)
	
	current_pose.orientation.x, current_pose.orientation.y, current_pose.orientation.z ,current_pose.orientation.w = euler_to_quaternion(euler)
     
    ## 制約を定義
	constraints= moveit_msgs.msg.Constraints()
	# # # 各関節の制限を設定
	joints_name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
	## 目標角度設定
	joint_goal_deg = [-31.18, -76.67, -115.35, -169.04, -30.93, 0.60] #remove
    # joint_goal_deg = [-12.56, -64.98, -121.27, -176.68, -11.85, 2.50] #input
	joint_goal = [x * pi/180 for x in joint_goal_deg]
	joints_goal = joint_goal  # 目標角度（radians）
	
	tolerances_deg=[90,120,120,120,120,120]
	tolerances = [x * pi/180 for x in tolerances_deg] # 許容範囲（radians）    
	for i in range(6):
		joint_constraint = moveit_msgs.msg.JointConstraint()
		joint_constraint.joint_name = joints_name[i]
		joint_constraint.position = joints_goal[i]
		joint_constraint.tolerance_above = tolerances[i]
		joint_constraint.tolerance_below = tolerances[i]
		joint_constraint.weight = 1.0
		constraints.joint_constraints.append(joint_constraint)
    
	# # # 制約をMoveGroupに適用
	move_group.set_path_constraints(constraints)
	
	plan_and_excute(current_pose, 'Move to a point near the target', move_group)


if __name__ == "__main__":
	rospy.init_node('init_pose')
	Move()
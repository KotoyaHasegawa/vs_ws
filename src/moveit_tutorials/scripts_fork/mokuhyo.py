#!/usr/bin/env python3
# coding: UTF-8

import sys
import moveit_commander
import rospy
import numpy as np
from math import pi

from tf import transformations
from tf.transformations import quaternion_multiply, quaternion_conjugate

from scipy.spatial.transform import Rotation as R
from geometry_msgs.msg import Vector3

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


def Move():
	moveit_commander.roscpp_initialize(sys.argv)
	move_group = moveit_commander.MoveGroupCommander("manipulator")
	move_group.set_max_velocity_scaling_factor(value=0.6)
	move_group.set_max_acceleration_scaling_factor(value=0.6)
	print(move_group.get_current_joint_values())


	joint_goal2_deg = [-31.19, -76.68, -115.36, -169.03, -30.93, 0.60] #remove
	# joint_goal2_deg = [-30.82, -86.41, -130.33, -144.34, -30.53,  0.62] #remove2fromimg	
	# joint_goal2_deg = [-30.86, -107.27, -138.50, -115.26, -30.53,  0.55] #remove3fromimg	

      
	# joint_goal2_deg = [-27.60, -71.65, -118.28, -169.50, -26.60, -1.68] #input
	# joint_goal2_deg = [-27.59, -80.72, -134.37, -144.35, -26.55, -1.69] #input2_img0  
	# joint_goal2_deg = [-27.16, -103.70, -143.18, -112.48, -26.08, -1.78] #input3_imgs


	# joint_goal2_deg = [-30.34, -75.84, -114.86, -170.59, -29.35, 1.27] #input?
	joint_goal2 = [x * pi/180 for x in joint_goal2_deg]

 
# 	joint_goal2 = [-0.544193660771832,	-1.33814393750405,	-2.01323729217546,	-2.95030456757121	,-0.539830337641846	,0.010471975511966]
#  ##desired2
	# joint_goal2 = [-0.52953289505508	,-1.3231341059369	,-2.0015435861871	,-2.98137142825671	,-0.511905069609937	,0.03682644721708]#remove
      
	
	move_group.set_joint_value_target(joint_goal2)
	print(joint_goal2)
	move_group.go(wait=True)
	print('moved to desired pose')
	print(move_group.get_current_pose())
	current_pose = move_group.get_current_pose().pose
	print(quaternion_to_euler(current_pose))
	current_pose_euler = move_group.get_current_rpy()

    

	c = quaternion_to_euler(current_pose)
	current_pose_euler = [current_pose.position.x, current_pose.position.y, current_pose.position.z, c.x, c.y, c.z]
	euler_to_quaternionbymoveit = np.array([current_pose.orientation.x, current_pose.orientation.y, current_pose.orientation.z, current_pose.orientation.w])
	print(euler_to_quaternionbymoveit)
	euler_to_quaternionbytf = np.array(euler_to_quaternion(c))
	print(euler_to_quaternionbytf)
      
	difference = quaternion_multiply(euler_to_quaternionbymoveit, quaternion_conjugate(euler_to_quaternionbytf))
      
	corrected_quat = quaternion_multiply(difference, euler_to_quaternionbytf)

	print("補正後のクォータニオン:", corrected_quat)

	# print(move_group.get_current_rpy())

	
    
	# print(move_group.get_current_rpy())
	
 
	moveit_commander.roscpp_shutdown()

if __name__ == "__main__":
	rospy.init_node('desired_pose')
	Move()

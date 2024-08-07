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


	# joint_goal2_deg = [-31.18, -76.67, -115.35, -169.04, -30.93, 0.60] #remove
	# joint_goal2_deg = [-31.00, -86.12, -130.29, -144.43, -30.70,  0.43] #remove2fromimg	
	# joint_goal2_deg = [-32.13, -106.53, -138.06, -117.63, -31.81, 1.32] #remove3
	joint_goal2_deg = [-31.95, -106.57, -138.21, -116.09, -31.77,  0.21] #remove3fromimg	

      
	# joint_goal2_deg = [-30.34, -75.81, -114.68, -170.82, -29.33, 2.11] #input
	# joint_goal2_deg = [-30.36, -84.37, -130.29, -146.43, -29.29, 1.86] #input2
	# joint_goal2_deg = [-31.22, -105.18, -138.58, -117.00, -30.11, 1.53] #input3


	joint_goal2 = [x * pi/180 for x in joint_goal2_deg]

 
	# joint_goal2 = [1.60414, -1.90515, 2.10868, -0.18457, 1.31903, -3.15687] ###desired2
 
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

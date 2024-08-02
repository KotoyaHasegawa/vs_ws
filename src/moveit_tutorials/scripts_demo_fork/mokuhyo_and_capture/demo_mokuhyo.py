#!/usr/bin/env python3
# coding: UTF-8

import sys
import moveit_commander
import rospy
import numpy as np
from math import pi

from tf import transformations
from scipy.spatial.transform import Rotation as R
from geometry_msgs.msg import Vector3

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


def Move():
	moveit_commander.roscpp_initialize(sys.argv)
	move_group = moveit_commander.MoveGroupCommander("manipulator")
	move_group.set_max_velocity_scaling_factor(value=0.6)
	move_group.set_max_acceleration_scaling_factor(value=0.6)

	joint_goal2_deg = [-31.18, -76.67, -115.35, -169.04, -30.93, 0.60] #remove
	# joint_goal2_deg = [-31.43, -86.04, -130.66, -144.02, -30.80,  0.27] #remove2
	# joint_goal2_deg = [-31.03, -86.21, -130.15, -144.52, -30.41,  0.14] #remove2fromimg	
	# joint_goal2_deg = [-32.13, -106.53, -138.06, -117.63, -31.81, 1.32] #remove3
	# joint_goal2_deg = [-31.69, -106.47, -137.63, -118.14, -31.35,  1.73] #remove3fromimg	


	# joint_goal2_deg = [-12.56, -64.98, -121.27, -176.68, -11.85, 2.50] #input
	# joint_goal2_deg = [-13.27, -72.62, -138.99, -149.90, -13.04, 1.92] #input2
	# joint_goal2_deg = [-13.32, -96.34, -148.97, -119.36, -13.44, 4.76] #input3

	joint_goal2 = [x * pi/180 for x in joint_goal2_deg]

	# joint_goal2 = [1.60414, -1.90515, 2.10868, -0.18457, 1.31903, -3.15687] ###desired2
 
	move_group.set_joint_value_target(joint_goal2)
	print("\njoint angle:")   
	print(joint_goal2)
    
	move_group.go(wait=True)
	print('\nmoved to desired pose\n')
    
	current_pose = move_group.get_current_pose().pose
	print("\ncurrent pose:")   
	print(move_group.get_current_pose())
	print(quaternion_to_euler(current_pose))   
	# print(move_group.get_current_rpy())
	
	moveit_commander.roscpp_shutdown()

if __name__ == "__main__":
	rospy.init_node('desired_pose')
	Move()

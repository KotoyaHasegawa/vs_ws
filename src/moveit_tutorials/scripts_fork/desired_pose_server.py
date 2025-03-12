#!/usr/bin/env python3
# coding: UTF-8

import sys
from math import pi

import moveit_commander
import rospy

import numpy as np

# import datetime
# import time

import actionlib
from moveit_tutorials.msg import EmptyAction, EmptyGoal, EmptyResult
import csv

# dataset = 400

def MovetoGoal(goal):
	moveit_commander.roscpp_initialize(sys.argv)
	move_group = moveit_commander.MoveGroupCommander('manipulator')
	move_group.set_max_velocity_scaling_factor(value = 0.1)
	move_group.set_max_acceleration_scaling_factor(value = 0.1)

	# joint_goal = [1.60414, -1.90515, 2.10868, -0.18457, 1.31903, -3.15687] 
 
	joint_goal_deg = [-31.18, -76.67, -115.35, -169.04, -30.93, 0.60] #remove
	# joint_goal_deg = [-27.60, -71.65, -118.28, -169.50, -26.60, -1.68]#input

	joint_goal = [x * pi/180 for x in joint_goal_deg]
	# joint_goal = [-0.5441883246051233, -1.338113473062851, -2.013108253479004, 
	# 		   -2.95029940227651, -0.5396583716021937, 0.010434690862894058]#remove

	move_group.set_joint_value_target(joint_goal)
	move_group.go(wait=True)
	print('moved to desires pose')

	result = EmptyResult()
	motion_server.set_succeeded(result)
	
if __name__ == "__main__":
	rospy.init_node('motion_server')
	rospy.loginfo('motion server started. ready to serve.')
	motion_server = actionlib.SimpleActionServer('ugoke', EmptyAction, MovetoGoal, False)
	motion_server.start()
	rospy.spin()
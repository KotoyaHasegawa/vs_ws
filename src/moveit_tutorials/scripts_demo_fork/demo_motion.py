#!/usr/bin/env python3
# coding: UTF-8

import sys
import rospy
import moveit_commander
from math import pi
from time import sleep
import tf.transformations


class Motion():
    def __init__(self, move_group):
        moveit_commander.roscpp_initialize(sys.argv)
        # rospy.init_node('withdraw', anonymous=True)
        self.move_group = move_group
        self.move_group.set_max_velocity_scaling_factor(0.3)
        self.move_group.set_max_acceleration_scaling_factor(0.3)

    def euler_to_quaternion(self, eule_x, euler_y, euler_z):
        q = tf.transformations.quaternion_from_euler(eule_x, euler_y, euler_z)
        return -1*q[0], -1*q[1], -1*q[2], -1*q[3]

    def quaternion_to_euler(self, current_pose):
        e = tf.transformations.euler_from_quaternion((current_pose.x, current_pose.y, current_pose.z, current_pose.w))
        return e[0], e[1], e[2]

    def plan_and_excute(self, target_pose, text):
        waypoints = [target_pose]
        (plan, fraction) = self.move_group.compute_cartesian_path(waypoints, eef_step=0.06, jump_threshold=0.00)
        self.move_group.execute(plan, wait=True)
        self.move_group.set_pose_target(target_pose)
        self.move_group.go(wait=True)
        print("\n-----------------------------\n")
        print("\n-----------------------------\n")
        print(text)
        print("\n-----------------------------\n")
        print("\n-----------------------------\n")


    def home_motion(self):
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
    
        self.move_group.set_joint_value_target(joint_goal2)
        print("\njoint angle:")   
        print(joint_goal2)
        
        self.move_group.go(wait=True)
        print('\nmoved to desired pose\n')
        
        current_pose = self.move_group.get_current_pose().pose
        print("\ncurrent pose:")   
        print(self.move_group.get_current_pose())  
        
    def people_with_robot(self):
        # get current pose and taget pose
        joint_goal2_deg = [-21.80, -87.40, -97.90, -174.91, -109.56, -0.22] #moveplay
        joint_goal2 = [x * pi/180 for x in joint_goal2_deg]
        self.move_group.set_joint_value_target(joint_goal2)
        print("Delivering drawers to people")
        self.move_group.go(wait=True)


class MotionAfterVS():
    def __init__(self, move_group):
        moveit_commander.roscpp_initialize(sys.argv)
        # rospy.init_node('withdraw', anonymous=True)
        self.move_group = move_group
        self.move_group.set_max_velocity_scaling_factor(0.08)
        self.move_group.set_max_acceleration_scaling_factor(0.08)

    def euler_to_quaternion(self, eule_x, euler_y, euler_z):
        q = tf.transformations.quaternion_from_euler(eule_x, euler_y, euler_z)
        return -1*q[0], -1*q[1], -1*q[2], -1*q[3]

    def quaternion_to_euler(self, current_pose):
        e = tf.transformations.euler_from_quaternion((current_pose.x, current_pose.y, current_pose.z, current_pose.w))
        return e[0], e[1], e[2]

    def plan_and_excute(self, target_pose, text):
        waypoints = [target_pose]
        (plan, fraction) = self.move_group.compute_cartesian_path(waypoints, eef_step=0.06, jump_threshold=0.00)
        self.move_group.execute(plan, wait=True)
        self.move_group.set_pose_target(target_pose)
        self.move_group.go(wait=True)
        print("\n-----------------------------\n")
        print("\n-----------------------------\n")
        print(text)
        print("\n-----------------------------\n")
        print("\n-----------------------------\n")

    def withdraw_motion(self):
        current_pose = self.move_group.get_current_pose().pose
        target_pose = current_pose

        target_pose.position.x = current_pose.position.x + 0.0037
        target_pose.position.y = current_pose.position.y + 0.2947
        target_pose.position.z = current_pose.position.z - 0.00756

        current_pose_euler = [0, 0, 0]
        current_pose_euler[0], current_pose_euler[1], current_pose_euler[2] = self.quaternion_to_euler(target_pose.orientation)
        rx = current_pose_euler[0] - 0.00267
        ry = current_pose_euler[1] - 0.01276
        rz = current_pose_euler[2] + 0.00428 + 0.0028645111

        if rz > 3.141592:
            rz = rz - 6.283

        target_pose.orientation.x, target_pose.orientation.y, target_pose.orientation.z, target_pose.orientation.w = self.euler_to_quaternion(rx, ry, rz)
        self.plan_and_excute(target_pose, 'inpuit shelf')

        current_pose = self.move_group.get_current_pose().pose
        target_pose = current_pose
        target_pose.position.z = current_pose.position.z + 0.011
        self.plan_and_excute(target_pose, 'input holl')

        target_pose.position.y = 0.28018
        self.plan_and_excute(target_pose, 'finish withdraw motion')

    def input(self):

        # Get current pose
        # このときorientationも取得されるのでz方向の制御量だけ入力すればいい
        current_pose = self.move_group.get_current_pose().pose
        print (current_pose)

        # Update Z coordinate
        target_pose = current_pose
        ##上段
        # target_pose.position.y = current_pose.position.y + 0.33063 ###一回目の中継地点
        # target_pose.position.z = current_pose.position.z - 0.006

        ##上段（治具変更）
        target_pose.position.y = current_pose.position.y + 0.33063 ###一回目の中継地点
        target_pose.position.z = current_pose.position.z -0.010

        #中段
        # target_pose.position.y = current_pose.position.y + 0.29963 ###一回目の中継地点
        # target_pose.position.z = current_pose.position.z - 0.003

        #下段
        # target_pose.position.y = current_pose.position.y + 0.28963 ###一回目の中継地点
        # target_pose.position.z = current_pose.position.z - 0.003


        self.plan_and_excute(target_pose, 'inpuit shelf')

        target_pose = current_pose
        target_pose.position.z =  current_pose.position.z - 0.0065 ###二回目の中継地点
        self.plan_and_excute(target_pose, 'withdraw io bottom hole')

        target_pose = current_pose
        target_pose.position.y =  current_pose.position.y + 0.04523 ###二回目の中継地点
        self.plan_and_excute(target_pose, 'push drawer')

        # # target_pose = current_pose
        # # target_pose.position.z =  current_pose.position.z - 0.0015 ###二回目の中継地点
        # # waypoints = [target_pose]
        # # (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.01, jump_threshold=0.00 )
        # # move_group.execute(plan, wait=True)
        # # print('chukei')
        # # print(target_pose)
        # # move_group.set_pose_target(target_pose)
        # # move_group.go(wait=True)
        
        target_pose.position.y = 0.36018 ###ボルトの頭当たるくらい
        waypoints = [target_pose]
        self.plan_and_excute(target_pose, 'finish input motion')




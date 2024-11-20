#!/usr/bin/env python3
# coding: UTF-8

import sys
import rospy
import moveit_commander
from math import pi

def zdescend():
    moveit_commander.roscpp_initialize(sys.argv)
    move_group = moveit_commander.MoveGroupCommander("manipulator")
    move_group.set_max_velocity_scaling_factor(value=0.08)
    move_group.set_max_acceleration_scaling_factor(value=0.08) ###magnetのときこのスピードで抜けたwas0.01
 
    # Get current pose
    # このときorientationも取得されるのでz方向の制御量だけ入力すればいい
    current_pose = move_group.get_current_pose().pose
    print (current_pose)

    # Update Z coordinate
    target_pose = current_pose
    ##上段
    # target_pose.position.y = current_pose.position.y + 0.33063 ###一回目の中継地点
    # target_pose.position.z = current_pose.position.z - 0.006

    ##上段（治具変更）
    # target_pose.position.y = current_pose.position.y + 0.33063 ###一回目の中継地点
    # target_pose.position.z = current_pose.position.z -0.010

    ##上段（変更）
    target_pose.position.y = current_pose.position.y + 0.253


    #中段
    # target_pose.position.y = current_pose.position.y + 0.29963 ###一回目の中継地点
    # target_pose.position.z = current_pose.position.z - 0.003

    #下段
    # target_pose.position.y = current_pose.position.y + 0.28963 ###一回目の中継地点
    # target_pose.position.z = current_pose.position.z - 0.003



    waypoints = [target_pose]
    (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06)
    move_group.execute(plan, wait=True)
    print('chukei')
    print(target_pose)
    move_group.set_pose_target(target_pose)
    move_group.go(wait=True)

    target_pose = current_pose
    target_pose.position.z =  current_pose.position.z - 0.013 ###二回目の中継地点
    waypoints = [target_pose]
    (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06)
    move_group.execute(plan, wait=True)
    print('chukei')
    print(target_pose)
    move_group.set_pose_target(target_pose)
    move_group.go(wait=True)

    target_pose = current_pose
    target_pose.position.y =  current_pose.position.y + 0.04523 ###二回目の中継地点
    waypoints = [target_pose]
    (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06)
    move_group.execute(plan, wait=True)
    print('chukei')
    print(target_pose)
    move_group.set_pose_target(target_pose)
    move_group.go(wait=True)

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
    (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06)
    move_group.execute(plan, wait=True)
    print('sasarucyokuzen')
    print(target_pose)
    move_group.set_pose_target(target_pose)
    move_group.go(wait=True)
    ### taiki
    print('ascended to z=22.4mm')


    moveit_commander.roscpp_shutdown()

if __name__ == '__main__':
    rospy.init_node('descend')
    try:
        zdescend()
    except rospy.ROSInterruptException:
        pass

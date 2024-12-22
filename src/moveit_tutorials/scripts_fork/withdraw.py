#!/usr/bin/env python3
# coding: UTF-8

import sys
import rospy
import moveit_commander
from math import pi
import time
import tf.transformations

# def zdescend():
#     moveit_commander.roscpp_initialize(sys.argv)
#     move_group = moveit_commander.MoveGroupCommander("manipulator")
#     move_group.set_max_velocity_scaling_factor(value=0.08)
#     move_group.set_max_acceleration_scaling_factor(value=0.08) ###magnetのときこのスピードで抜けたwas0.01
 
#     # Get current pose
#     # このときorientationも取得されるのでz方向の制御量だけ入力すればいい
#     current_pose = move_group.get_current_pose().pose
#     print (current_pose)

#     # Update Z coordinate
#     target_pose = current_pose
#     # target_pose.position.x = current_pose.position.x + 0.005
#     target_pose.position.x = current_pose.position.x + 0.007
#     target_pose.position.y = current_pose.position.y + 0.28666 ###上段
#     # target_pose.position.z = current_pose.position.z - 0.003
#     target_pose.position.z = current_pose.position.z 

#     # target_pose.position.x = current_pose.position.x - 0.005
#     # target_pose.position.y = current_pose.position.y + 0.29066 ##中断
#     # target_pose.position.z = current_pose.position.z - 0.003

#     # target_pose.position.y = current_pose.position.y + 0.30066 ##下段
#     # target_pose.position.z = current_pose.position.z + 0.001

#     waypoints = [target_pose]
#     (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06, jump_threshold=0.00 )
#     move_group.execute(plan, wait=True)
#     print('chukei')
#     print(target_pose)
#     move_group.set_pose_target(target_pose)
#     move_group.go(wait=True)
    
#     # Update Z coordinate
#     target_pose = current_pose
#     # target_pose.position.z = current_pose.position.z + 0.008##上段
#     target_pose.position.z = current_pose.position.z + 0.005##上段
#     waypoints = [target_pose]
#     (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06, jump_threshold=0.00 )
#     move_group.execute(plan, wait=True)
#     print('chukei')
#     print(target_pose)
#     move_group.set_pose_target(target_pose)
#     move_group.go(wait=True)
    
#     target_pose.position.y = 0.28018 ###ボルトの頭当たるくらい
#     waypoints = [target_pose]
#     (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06, jump_threshold=0.00 )
#     move_group.execute(plan, wait=True)
#     print('sasarucyokuzen')
#     print(target_pose)
#     move_group.set_pose_target(target_pose)
#     move_group.go(wait=True)
#     ### taiki
#     print('ascended to z=22.4mm')

#     # joint_goal2_deg = [-21.80, -87.40, -97.90, -174.91, -109.56, -0.22] #moveplay
#     # joint_goal2 = [x * pi/180 for x in joint_goal2_deg]
#     # move_group.set_joint_value_target(joint_goal2)
#     # print(joint_goal2)
#     # move_group.go(wait=True)


#     moveit_commander.roscpp_shutdown()

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
    e = tf.transformations.euler_from_quaternion((current_pose.x,current_pose.y,current_pose.z,current_pose.w))
    return e[0], e[1], e[2]


def zdescend():
    moveit_commander.roscpp_initialize(sys.argv)
    move_group = moveit_commander.MoveGroupCommander("manipulator")
    move_group.set_max_velocity_scaling_factor(value=0.08)
    move_group.set_max_acceleration_scaling_factor(value=0.08) ###magnetのときこのスピードで抜けたwas0.01
 
    # Get current pose
    # このときorientationも取得されるのでz方向の制御量だけ入力すればいい
    current_pose = move_group.get_current_pose().pose
    print (current_pose)

    # # Update Z coordinate(dist=200mm)
    # target_pose = current_pose
    # target_pose.position.y = current_pose.position.y + 0.21809 ###上段
    # target_pose.position.z = current_pose.position.z 

    # Update Z coordinate(dist=300mm)
    target_pose = current_pose
    target_pose.position.x = current_pose.position.x + 0.0067 ###上段
    target_pose.position.y = current_pose.position.y + 0.272 ###上段
    target_pose.position.z = current_pose.position.z - 0.00456

    current_pose_euler = [0, 0, 0]
    current_pose_euler[0], current_pose_euler[1], current_pose_euler[2] = quaternion_to_euler(target_pose.orientation)
    rx = current_pose_euler[0] - 0.00267
    ry = current_pose_euler[1] - 0.01276
    rz = current_pose_euler[2] #+ 0.00428 + 0.0028645111

    if rz > 3.141592:
        rz = rz - 6.283   

    target_pose.orientation.x, target_pose.orientation.y, target_pose.orientation.z, target_pose.orientation.w = euler_to_quaternion(rx, ry, rz)
    # target_pose.orientation.w = 0.0038659277028896453
    # target_pose.orientation.x = -0.01612507986769021
    # target_pose.orientation.y = -0.7097065735034274
    # target_pose.orientation.z = -0.7043022191703507



    waypoints = [target_pose]
    # (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06, jump_threshold=0.00 )
    (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06)
    move_group.execute(plan, wait=True)
    # print('chukei')
    # print(target_pose)
    move_group.set_pose_target(target_pose)
    move_group.go(wait=True)

    
    # Update Z coordinate
    current_pose = move_group.get_current_pose().pose
    target_pose = current_pose
    target_pose.position.z = current_pose.position.z + 0.013#上段
    # target_pose.position.z = current_pose.position.z + 0.005##上段
    waypoints = [target_pose]
    (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06)
    move_group.execute(plan, wait=True)
    # print('chukei')
    # print(target_pose)
    move_group.set_pose_target(target_pose)
    move_group.go(wait=True)
    
    target_pose.position.y = 0.28018 ###ボルトの頭当たるくらい
    waypoints = [target_pose]
    (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06)
    move_group.execute(plan, wait=True)
    print('sasarucyokuzen')
    print(target_pose)
    move_group.set_pose_target(target_pose)
    move_group.go(wait=True)
    ### taiki
    # print('ascended to z=22.4mm')

    # joint_goal2_deg = [-21.80, -87.40, -97.90, -174.91, -109.56, -0.22] #moveplay
    # joint_goal2 = [x * pi/180 for x in joint_goal2_deg]
    # move_group.set_joint_value_target(joint_goal2)
    # print(joint_goal2)
    # move_group.go(wait=True)


    moveit_commander.roscpp_shutdown()    

if __name__ == '__main__':
    rospy.init_node('descend')
    try:
        zdescend()
    except rospy.ROSInterruptException:
        pass

#!/usr/bin/env python3
# coding: UTF-8

import sys
import rospy
import moveit_commander
from math import pi
import time
import tf.transformations


def euler_to_quaternion(eule_x, euler_y, euler_z):
    """Convert Euler Angles to Quaternion

    euler: geometry_msgs/Vector3
    quaternion: geometry_msgs/Quaternion
    """
    q = tf.transformations.quaternion_from_euler(eule_x, euler_y, euler_z)
    return -1*q[0], -1*q[1], -1*q[2], -1*q[3]

def quaternion_to_euler(current_pose):
    """Convert Quaternion to Euler Angles

    quarternion: geometry_msgs/Quaternion
    euler: geometry_msgs/Vector3
    """
    e = tf.transformations.euler_from_quaternion((current_pose.x,current_pose.y,current_pose.z,current_pose.w))
    return e[0], e[1], e[2]


def plan_and_excute(target_pose, move_group, text):
    waypoints = [target_pose]
    (plan, fraction) =move_group.compute_cartesian_path(waypoints , eef_step=0.06, jump_threshold=0.00 )
    move_group.execute(plan, wait=True)
    move_group.set_pose_target(target_pose)
    move_group.go(wait=True)
    return print(text)


def people_with_robot():
    moveit_commander.roscpp_initialize(sys.argv)
    move_group = moveit_commander.MoveGroupCommander("manipulator")
    move_group.set_max_velocity_scaling_factor(value=0.3)
    move_group.set_max_acceleration_scaling_factor(value=0.3) ###magnetのときこのスピードで抜けたwas0.01
 
    # get current pose and taget pose
    current_pose = move_group.get_current_pose().pose
    target_pose = current_pose

    joint_goal2_deg = [-21.80, -87.40, -97.90, -174.91, -109.56, -0.22] #moveplay
    joint_goal2 = [x * pi/180 for x in joint_goal2_deg]
    move_group.set_joint_value_target(joint_goal2)
    print("Delivering drawers to people")
    move_group.go(wait=True)
    

    moveit_commander.roscpp_shutdown()    

if __name__ == '__main__':
    rospy.init_node('descend')
    try:
        people_with_robot()
    except rospy.ROSInterruptException:
        pass

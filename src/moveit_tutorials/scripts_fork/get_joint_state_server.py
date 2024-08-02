#!/usr/bin/env python3
#coding: UTF-8

import rospy
from sensor_msgs.msg import JointState
from moveit_tutorials.srv import GetCurrentJointVel, GetCurrentJointVelResponse

# グローバル変数
current_joint_angles = []

# サブスクライバーのコールバック関数
def joint_states_callback(data):
    global current_joint_angles
    current_joint_angles = data.position  # 関節の角度情報を保存

# サービスコールのコールバック関数
def handle_get_joint_angles(req):
    global current_joint_angles
    return GetCurrentJointVelResponse(current_joint_angles)

if __name__ == "__main__":
    rospy.init_node('joint_angle_server')
    rospy.Subscriber('/joint_states', JointState, joint_states_callback)
    rospy.Service('get_joint_angles', GetCurrentJointVel, handle_get_joint_angles)  # サービス名と型を適切に設定
    rospy.loginfo("Ready to get joint angles.")
    rospy.spin()

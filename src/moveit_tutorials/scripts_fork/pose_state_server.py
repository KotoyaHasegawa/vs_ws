#!/usr/bin/env python3
#coding: UTF-8

import rospy
import tf
from geometry_msgs.msg import PoseStamped
from moveit_tutorials.srv import GettfPose, GettfPoseResponse  # サービス定義を適切に変更する

# グローバル変数
current_pose = PoseStamped()

# サブスクライバーのコールバック関数
def pose_callback(data):
    global current_pose
    current_pose = data

# サービスコールのコールバック関数
def return_pose(res):
    return GettfPoseResponse(current_pose)

def main():
    rospy.init_node('pose_server')
    rospy.loginfo('Pose server ready to serve')
    
    # サブスクライバーの設定
    rospy.Subscriber('/robot_pose', PoseStamped, pose_callback)
    
    # サービスの設定
    rospy.Service('get_pose', GettfPose, return_pose)
    
    rospy.spin()

if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException:
        pass


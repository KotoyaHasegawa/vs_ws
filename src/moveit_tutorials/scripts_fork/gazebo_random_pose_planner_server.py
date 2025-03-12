#!/usr/bin/env python3
# coding: UTF-8

import rospy
import moveit_commander
import moveit_msgs.msg
from geometry_msgs.msg import Pose
from geometry_msgs.msg import Quaternion
from geometry_msgs.msg import PoseStamped
from moveit_msgs.msg import CollisionObject, PlanningScene
from shape_msgs.msg import SolidPrimitive

import tf.transformations
from geometry_msgs.msg import Vector3

import sys
from math import pi

import random 

import actionlib
from moveit_tutorials.msg import EmptyAction, EmptyResult
import csv

from time import sleep

def add_object(planning_scene_pub, object_id, object_pose, object_size):
    planning_scene = PlanningScene()
    planning_scene.world.collision_objects.append(CollisionObject())
    object_msg = planning_scene.world.collision_objects[-1]
    object_msg.id = object_id

    primitive = SolidPrimitive()
    primitive.type = SolidPrimitive.BOX
    primitive.dimensions = object_size

    object_msg.primitives.append(primitive)
    object_msg.primitive_poses.append(object_pose.pose)

    # Publish the planning scene
    planning_scene.is_diff = True
    planning_scene_pub.publish(planning_scene)

def euler_to_quaternion(euler):
    """Convert Euler Angles to Quaternion

    euler: geometry_msgs/Vector3
    quaternion: geometry_msgs/Quaternion
    """
    q = tf.transformations.quaternion_from_euler(euler.x, euler.y, euler.z)
    return q[0], q[1], q[2], q[3]

def quaternion_to_euler(current_pose):
    """Convert Quaternion to Euler Angles

    quarternion: geometry_msgs/Quaternion
    euler: geometry_msgs/Vector3
    """
    e = tf.transformations.euler_from_quaternion((current_pose.orientation.x,current_pose.orientation.y,current_pose.orientation.z,current_pose.orientation.w))
    return e[0], e[1], e[2]




def random_pose(goal):
    joint_data = []
    pose_data = []
    pose_data2 = []
    moveit_commander.roscpp_initialize(sys.argv)
    moveit_commander.RobotCommander()
    moveit_commander.PlanningSceneInterface()
    group_name = "manipulator"
    move_group = moveit_commander.MoveGroupCommander(group_name)
    
    ###一旦desired pose に移動
    # joint_goal_deg =  [-31.19, -76.68, -115.36, -169.03, -30.93, 0.60] #remove
    joint_goal_deg = [-27.60, -71.65, -118.28, -169.50, -26.60, -1.68] #input

    joint_goal = [x * pi/180 for x in joint_goal_deg]
    move_group.set_joint_value_target(joint_goal)
    move_group.go(wait=True)
    
    print('ittan desired pose')
    
    pose = Pose()
    
    #remove
    # with open('./dsrth_result/desired_pose.csv', 'r') as f:
    #     reader = csv.reader(f)
    #     for row in reader:
    #         desired_pose = [float(x) for x in row]

    # #input
    with open('./dsrth_result/desired_pose.csv', 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            desired_pose = [float(x) for x in row]

    # add box
    # plan.add_plane(name="plane",pose=pose,normal=(0,0,1),offset=0)
    # box_pose = PoseStamped()
    # box_pose.header.frame_id = "world"
    # box_pose.pose.orientation.w = 1.0
    # box_pose.pose.position.x=0
    # box_pose.pose.position.y=0
    # box_pose.pose.position.z = 0  # panda_handフレームの上
    # box_name = "box"
    # scene.add_box(box_name, box_pose, size=(100, 100, 0.1))

    # box_pose1 = PoseStamped()
    # box_pose1.header.frame_id = "world"
    # box_pose1.pose.orientation.w = 1.0
    # box_pose1.pose.position.x=0
    # box_pose1.pose.position.y=0
    # box_pose1.pose.position.z = 0.8  # panda_handフレームの上
    # box_name = "box1"
    # box_size=[100,100,0.2]
    # # Add object to the planning scene
    # # Create a planning scene publisher
    # planning_scene_pub = rospy.Publisher('/planning_scene', PlanningScene, queue_size=10)

    # # Add object to the planning scene
    # add_object(planning_scene_pub, object_id, box_pose1,box_size)

    # box_pose2 = PoseStamped()
    # box_pose2.header.frame_id = "panda_hand"
    # box_pose2.pose.orientation.w = 1.0
    # box_pose2.pose.position.x=0.5
    # box_pose2.pose.position.y=0
    # box_pose2.pose.position.z = 0 # panda_handフレームの上
    # box_name = "box2"
    # box_size2=(0.1, 100, 100)
    
    # # Add object to the planning scene
    # # Create a planning scene publisher
    # planning_scene_pub = rospy.Publisher('/planning_scene', PlanningScene, queue_size=10)

    # # Add object to the planning scene
    # add_object(planning_scene_pub, object_id, box_pose2,box_size2)



    
    # # *********************
    # fixed_orientation = move_group.get_current_pose().pose.orientation
    # sleep(0.1)
    # print(fixed_orientation)
    ###なんかだんだんずれていってた
    # # **********************
    
    ### gazeboでvalid_joint_values取得のためにsimするとき、poseをrandomで決めて入力するが、実機の手先座標と異なる
    ### 実機 desired pose[-0.142, 0.270, 0.255]だがgazebo desired pose [-0.14351, 0.26766, 0.2527]
    ### その差は[-0.00151, -0.00234, -0.0023]
    ### real desired pose [-0.17326, 0.36051, 0.39392]の値を元に各成分+-25mm, +-25mm, +-10mmでrandom.uniformする田中
    ### gazebo desired pose[-0.17241, 0.35987, 0.39084]の値を元に各成分+-25mm, +-10mm, +-25mmでrandom.uniformする
    
    # ## real pose 
    # pose.position.x = random.uniform(-0.19826, -0.14826) #差0.05
    # pose.position.y = random.uniform(0.35051, 0.37051) #差0.02
    # pose.position.z = random.uniform(0.36892, 0.41892) #差0.05

    # # remove
    # pose.position.x = random.uniform(-0.20326, -0.14326) #差0.06
    # pose.position.y = random.uniform(0.35051, 0.37051) #差0.02
    # pose.position.z = random.uniform(0.38392, 0.43392) #差+4,  -1


    #本格
    pose.position.x = random.uniform(desired_pose[0] - 0, desired_pose[0] + 0.025) #差+-0.025
    pose.position.y = random.uniform(desired_pose[1] - 0.01, desired_pose[1] + 0.01) #差0.02
    pose.position.z = random.uniform(desired_pose[2] - 0.025, desired_pose[2] + 0)#差+-0.025

    # #input
    # pose.position.x = random.uniform(-0.194880588, -0.144880588) #差0.05
    # pose.position.y = random.uniform(0.27327808, 0.27527808) #差0.02
    # pose.position.z = random.uniform(0.3893255971, 0.429325971) #差0.05



    ###gasebo pose
    # pose.position.x = random.uniform(-0.19741, -0.14741) #差0.05
    # pose.position.y = random.uniform(0.34987, 0.36987) #差0.02
    # pose.position.z = random.uniform(0.36584, 0.41584) #差0.05
    
    # # ***********************
    # pose.orientation = fixed_orientation
    # # ***********************
    # pose.orientation.w = 1.0  # ランダムな姿勢を設定する場合はこれも変更する必要
    # pose.orientation = pose.orientation


    # remove
    # euler_x = random.uniform(1.536355, 1.6236815)
    # euler_y = random.uniform(-0.038589, 0.048737)
    # euler_z = random.uniform(3.093573, 3.180895)
    # euler = Vector3(euler_x, euler_y, euler_z)

    # remove
    euler_x = desired_pose[3]
    euler_y = desired_pose[4]
    euler_z = desired_pose[5]
    euler = Vector3(euler_x, euler_y, euler_z)

    # #input
    # euler_x = 1.5812612704694948
    # euler_y = 0.006258518764927413
    # euler_z = 3.129045497905123
    # euler = Vector3(euler_x, euler_y, euler_z)


    ### desired 
    # pose.orientation.x = -0.00025091
    # pose.orientation.y = 0.7103727
    # pose.orientation.z = 0.7038182
    # pose.orientation.w = 0.0032341
    ##gazebo
    # pose.orientation.x = -0.0024873
    # pose.orientation.y = 0.71162312
    # pose.orientation.z = 0.70253760
    # pose.orientation.w = 0.005490795

    pose.orientation.x, pose.orientation.y, pose.orientation.z ,pose.orientation.w = euler_to_quaternion(euler)
    
    # # *********************************************************************************
    # # 制約を定義
    constraints = moveit_msgs.msg.Constraints()

    # # # 各関節の制限を設定
    joints_name = ['shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
    joints_goal = joint_goal  # 目標角度（radians）
    tolerances_deg=[90,120,120,120,120,50]
    tolerances = [x * pi/180 for x in tolerances_deg] # 許容範囲（radians）
    # tolerances = [1.0, 1.0, 2.0, 1.0, 1.0, 0.2]

    
    for i in range(5):
        joint_constraint = moveit_msgs.msg.JointConstraint()
        joint_constraint.joint_name = joints_name[i]
        joint_constraint.position = joints_goal[i]
        joint_constraint.tolerance_above = tolerances[i]
        joint_constraint.tolerance_below = tolerances[i]
        joint_constraint.weight = 1.0
        constraints.joint_constraints.append(joint_constraint)
        # if i == 5 :
        #     joint_constraint.tolerance_below = 0.174
            
            
    
    
    # # # 制約をMoveGroupに適用
    move_group.set_path_constraints(constraints)


    # # *********************************************************************************

    # ランダムなポーズを目標として設定
    move_group.set_pose_target(pose)

    # 移動計画と実行
    #wait=Trueにすることで動作が終わるまで待機
    move_group.go(wait=True)
    
    print('moved to random pose')
    
    joint_values = move_group.get_current_joint_values()
    
    print(joint_values) ###この形[]でした
    print('desired')
    print(pose)
    
    current_pose = move_group.get_current_pose().pose
    euler_x1 ,euler_y1, euler_z1= quaternion_to_euler(current_pose)
    print('current')
    print(current_pose)
    


    
    joint_data.append(joint_values)
    
    # pose_data.append([pose.position.x, pose.position.y, pose.position.z, pose.orientation.x, pose.orientation.y, pose.orientation.z])
    pose_data.append([current_pose.position.x, current_pose.position.y, current_pose.position.z])
    # pose_data2.append([current_pose.position.x, current_pose.position.y, current_pose.position.z,
    #                    current_pose.orientation.x,current_pose.orientation.y,current_pose.orientation.z,current_pose.orientation.w]) 
    pose_data2.append([current_pose.position.x, current_pose.position.y, current_pose.position.z,
                       euler_x1, euler_y1, euler_z1]) 

    ### gazebo+rviz(moveit)のとき手先posiotionもorientationもずれてるので注意
    ### 実際には上のget_current_poseとget_current_jointで取得されてる値怪しい->jointの方はrobot_info.pyから取得してみたら大丈夫そうだった
    ### get_current_poseで取得される手先座標は怪しそう（距離データ取得くらいにしか使わない）
    ### vel_servo_sig.py内で距離データ取得するときjoint_planner_serverで取得したdesired_pose.csv読んでるけどこれ多分正しくない（gazeboから取得した値だから）
    ### vel_servo_sig.pyで距離デーら取得するとき目標位置直打ちしたほうがいいかも
    filename = './rndmth_result/random_theta_result.csv'
    filename2 = './rndmth_result/random_pose.csv'
    filename3 = './rndmth_result/random_poseor.csv'
    
    with open (filename, 'a') as f, open(filename2, 'a') as f2, open(filename3, 'a') as f3:
        writer = csv.writer(f)
        writer.writerows(joint_data)
        writer2 = csv.writer(f2)
        writer2.writerows(pose_data)
        writer3 = csv.writer(f3)
        writer3.writerows(pose_data2)       
        
    # # *********************************************************************************
    # # 移動が終了したら制約をクリア
    # move_group.clear_path_constraints()
    # # *********************************************************************************
    
    result2 = EmptyResult()
    motion_server2.set_succeeded(result2)
    # moveit_commander.roscpp_shutdown()


if __name__ == "__main__":
    rospy.init_node('random_motion_server')
    rospy.loginfo('Random motion sever started. Ready to serve.')
    motion_server2 = actionlib.SimpleActionServer('ugoke_random', EmptyAction, random_pose, False)
    motion_server2.start()
    rospy.spin()
#!/usr/bin/env python3
# coding: UTF-8

import sys
import rospy
import time

from demo_shoki import ShokiMotion
from demo_motion import Motion, MotionAfterVS
import moveit_commander
from demo_vel_servo_forkpos import ServoNode

class DEMO():
    def __init__(self):
        self.move_group = moveit_commander.MoveGroupCommander("manipulator")

        self.motion = Motion(self.move_group)
        self.motion_after_avs = MotionAfterVS(self.move_group)
        self.shoki_motion = ShokiMotion(self.move_group)
        # self.AVS = ServoNode()

    def shoki_AVS_withdraw(self, csv):
        #shoki
        self.shoki_motion.move(csv)
        time.sleep(1)
        #AVS
        self.AVS = ServoNode()
        self.AVS.run(csv)
        rospy.signal_shutdown('AVS withdraw complete')
        #wait for shutdown
        while not rospy.is_shutdown():
            pass
        #withdraw
        self.motion_after_avs.withdraw_motion()
        #collaborative
        self.motion.people_with_robot()


    def shoki_AVS_input(self, csv):
        #shoki
        self.shoki_motion.move(csv)
        # rospy.signal_shutdown('finish')
        #AVS
    ####################################################################
    ####################################################################
        #input
        self.motion_after_avs.input()


    def main(self):

        # Ask the user for the number of loops
        loop_count = int(input("How many times?: "))

        for i in range(loop_count):
            #上段
            self.shoki_AVS_withdraw('./dsrth_result/withdraw/desired_pose.csv')
            # self.shoki_AVS_input('./dsrth_result/input/desired_pose.csv')
            time.sleep(15)

            #中断
            self.shoki_AVS_withdraw('./dsrth_result/withdraw/desired_pose_mid.csv')
            # shoki_AVS_input('./dsrth_result/input/desired_pose_mid.csv')
            time.sleep(15)

            #下段
            self.shoki_AVS_withdraw('./dsrth_result/withdraw/desired_pose_down.csv')
            # shoki_AVS_input('./dsrth_result/input/desired_pose_down.csv')
            time.sleep(15)

            
            print("\n-----------------------------\n")
            print("\n-----------------------------\n")
            print(f"Completed iteration {i + 1}")
            print("\n-----------------------------\n")
            print("\n-----------------------------\n")

        self.motion.home_motion()

if __name__ == "__main__":
    moveit_commander.roscpp_initialize(sys.argv)
    rospy.init_node('main_robot_node', anonymous=True)
    try:
        demo = DEMO()
        demo.main()
    except rospy.ROSInterruptException:
        pass 
    finally:
        moveit_commander.roscpp_shutdown()
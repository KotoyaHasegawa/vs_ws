#!/usr/bin/env python3
# coding: UTF-8

import sys
import rospy
import time

from motion_python.demo_shoki import ShokiMotion
from motion_python.demo_motion import Motion, MotionAfterVS
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

        #下段
        self.shoki_AVS_withdraw('./dsrth_result/withdraw/desired_pose_down.csv')
        # shoki_AVS_input('./dsrth_result/input/desired_pose_down.csv')
        time.sleep(10)
       
        print("\n-----------------------------\n")
        print("\n-----------------------------\n")
        print(f"Completed to get down drawer")
        print("\n-----------------------------\n")
        print("\n-----------------------------\n")

        # self.motion.home_motion()

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
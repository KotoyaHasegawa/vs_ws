#!/usr/bin/env python3
# coding: UTF-8

import sys
import rospy
from demo_shoki import ShokiMotion
from demo_motion import HomeMotion, CollaborativeMotion, WithdrawMotion, InputMotion
import moveit_commander


class DEMO():
    def __init__(self):
        self.move_group = moveit_commander.MoveGroupCommander("manipulator")

        self.homo_motion = HomeMotion(self.move_group)
        self.collaborative_motion = CollaborativeMotion(self.move_group)
        self.shoki_motion = ShokiMotion(self.move_group)
        self.withdraw_motion = WithdrawMotion(self.move_group)
        self.input_motion  = InputMotion(self.move_group)


    def shoki_AVS_withdraw(self, csv):
        #shoki
        self.shoki_motion.move(csv)
        #AVS
    ####################################################################
    ####################################################################
        #withdraw
        self.withdraw_motion.zdescend()


    def shoki_AVS_input(self, csv):
        #collaborative
        self.collaborative_motion.people_with_robot()
        #shoki
        self.shoki_motion.move(csv)
        #AVS
    ####################################################################
    ####################################################################
        #input
        self.input_motion.input()


    def main(self):

        # Ask the user for the number of loops
        loop_count = int(input("How many times?: "))

        for i in range(loop_count):
            #上段
            self.shoki_AVS_withdraw('./dsrth_result/withdraw/desired_pose.csv')
            self.shoki_AVS_input('./dsrth_result/input/desired_pose.csv')

            #中断
            self.shoki_AVS_withdraw('./dsrth_result/withdraw/desired_pose_mid.csv')
            # shoki_AVS_input('./dsrth_result/input/desired_pose_mid.csv')

            #下段
            self.shoki_AVS_withdraw('./dsrth_result/withdraw/desired_pose_down.csv')
            # shoki_AVS_input('./dsrth_result/input/desired_pose_down.csv')

            
            print("\n-----------------------------\n")
            print("\n-----------------------------\n")
            print(f"Completed iteration {i + 1}")
            print("\n-----------------------------\n")
            print("\n-----------------------------\n")

        self.homo_motion.move()



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















































#######################################################################################################################################
#######################################################################################################################################





# #!/usr/bin/env python3
# # coding: UTF-8
# import subprocess
# import sys
# import time
# import os
# import signal
# def run_script(script_name, with_error_img=False):
#     try:
#         if with_error_img:
#             # Start the error image process in a new process group
#             error_img_process = subprocess.Popen(
#                 ["rosrun", "moveit_tutorials", "demo_error_video.py"],
#                 preexec_fn=os.setsid
#             )
#             main_process = subprocess.run(
#                 ["rosrun", "moveit_tutorials", script_name],
#                 check=True
#             )
#             # Send the terminate signal to the process group
#             os.killpg(os.getpgid(error_img_process.pid), signal.SIGTERM)
#             error_img_process.wait()
#             time.sleep(3)  # プロセス終了後に短時間待機
#         else:
#             subprocess.run(["rosrun", "moveit_tutorials", script_name], check=True)
#     except subprocess.CalledProcessError as e:
#         print(f"Failed to run {script_name}: {e}")

# if __name__ == "__main__":
#     scripts = [
#         ("demo_people_robot.py", False),
#         ("demo_shoki2.py", False),
#         ("demo_init_image.py", False),
#         ("demo_vel_servo_forkpos.py", True),
#         ("demo_withdraw.py", False)
#     ]
#     start_script = scripts[0][0]
#     if len(sys.argv) > 1:
#         start_script = sys.argv[1]
#     if start_script not in [script[0] for script in scripts]:
#         print(f"Invalid start script: {start_script}")
#         sys.exit(1)
#     start_index = next(i for i, script in enumerate(scripts) if script[0] == start_script)
#     loop_count = 1

#     for _ in range(loop_count):
#         for script, with_error_img in scripts[start_index:]:
#             run_script(script, with_error_img)
#             # time.sleep(2)
#         for script, with_error_img in scripts[:start_index]:
#             run_script(script, with_error_img)
#             # time.sleep(2)
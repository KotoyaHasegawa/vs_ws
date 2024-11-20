#!/usr/bin/env python3
# coding: UTF-8
import subprocess
import sys
import time
import os
import signal
def run_script(script_name, with_error_img=False):
    try:
        if with_error_img:
            # Start the error image process in a new process group
            error_img_process = subprocess.Popen(
                ["rosrun", "moveit_tutorials", "error_img.py"],
                preexec_fn=os.setsid
            )
            main_process = subprocess.run(
                ["rosrun", "moveit_tutorials", script_name],
                check=True
            )
            # Send the terminate signal to the process group
            os.killpg(os.getpgid(error_img_process.pid), signal.SIGTERM)
            error_img_process.wait()
            time.sleep(3)  # プロセス終了後に短時間待機
        else:
            subprocess.run(["rosrun", "moveit_tutorials", script_name], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {script_name}: {e}")

if __name__ == "__main__":
    scripts = [
        #("demo_people_robot.py", False),
        ("shoki2.py", False),
        ("demo_init_image.py", False),
        # ("vel_servo_fork.py", True),
        # ("vel_servo_definet_fork.py", True),
        ("vel_servo_definet_fork_theta.py", True),
        # ("vel_servo_forkpos_moveit_input.py", True),
        # ("vel_servo_forkpos_moveit_withdraw.py", True),

        ("withdraw.py", False),
        ("mokuhyo.py", False),
        ("input.py", False),
        

        
    ]
    start_script = scripts[0][0]
    if len(sys.argv) > 1:
        start_script = sys.argv[1]
    if start_script not in [script[0] for script in scripts]:
        print(f"Invalid start script: {start_script}")
        sys.exit(1)
    start_index = next(i for i, script in enumerate(scripts) if script[0] == start_script)
    loop_count = 9

    for _ in range(loop_count):
        for script, with_error_img in scripts[start_index:]:
            run_script(script, with_error_img)
            # time.sleep(2)
        for script, with_error_img in scripts[:start_index]:
            run_script(script, with_error_img)

        # time.sleep(5)
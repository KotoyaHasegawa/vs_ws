import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
from ur_ikfast.ur_ikfast import ur_kinematics
# ur5e_arm は、UR5eロボットの逆運動学を計算するライブラリが必要です
# ここでは仮の関数として定義しますが、実際にはURのAPIなどを使用します。

ur5e_arm = ur_kinematics.URKinematics('ur5e')

# 手先座標の読み込みとz座標の変更
random_pose = pd.read_csv("~/vs_ws/src/moveit_tutorials/scripts_fork/rndmth_result/random_poseordel.csv", header=None)
random_pose[2] = -300  # z座標をすべて-300に変更

# 関節角度の初期推定を読み込む
joint_anglesUP = pd.read_csv("~/vs_ws/src/moveit_tutorials/scripts_fork/dsrth_result/desired_theta_result.csv", header=None)

# 各行の姿勢をクォータニオンに変換して逆運動学を解く
joint_angles = []

for index, row in random_pose.iterrows():
    x, y, z, rx, ry, rz = row
    r = R.from_euler('xyz', [rx, ry, rz], degrees=False)
    quat = r.as_quat()  # クォータニオンに変換 [qx, qy, qz, w]
    pose_quat = [x, y, z, quat[3], quat[0], quat[1], quat[2]]  # [x, y, z, w, qx, qy, qz]
    
    # 逆運動学を解く
    angles = ur5e_arm.inverse(pose_quat, False, q_guess=joint_anglesUP.loc[index])
    joint_angles.append(angles)

# 関節角度をCSVに保存
joint_angles_df = pd.DataFrame(joint_angles)
joint_angles_df.to_csv("~/vs_ws/src/moveit_tutorials/scripts_fork/output_joint_angles.csv", index=False, header=False)

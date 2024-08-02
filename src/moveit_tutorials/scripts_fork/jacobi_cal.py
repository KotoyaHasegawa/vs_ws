import torch
import numpy as np
import pandas as pd
import cv2
import glob

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# 設定数
set = 1500

# 目標ジョイント角をCSVファイルから読み込み
po = pd.read_csv("~/vs_ws/src/moveit_tutorials/scripts_fork/dsrth_result/desired_pose.csv", header=None)
PO = np.tile(po.values.T, (1, set))
PO = torch.tensor(PO, dtype=torch.float32).to(device)

# ランダムに動かしたジョイント角をCSVファイルから読み込み
por = pd.read_csv("~/vs_ws/src/moveit_tutorials/scripts_fork/rndmth_result/random_poseordel.csv", header=None)
POR = por.T
POR = torch.tensor(POR.values, dtype=torch.float32).to(device)

# カラーのPNG目標画像を読み込み
I_dsr = cv2.imread("./data/desired_im.png", cv2.IMREAD_GRAYSCALE)
I_dsr_gry2 = I_dsr.astype(np.double)
I_dsr_gry_cvec = I_dsr_gry2.T.reshape(-1, 1)
I_DSR = np.tile(I_dsr_gry_cvec, (1, set))
I_DSR = torch.tensor(I_DSR, dtype=torch.float32).to(device)

# ランダムにn回動作を繰り返した画像データセットをまとめて処理
image_paths = glob.glob("./data/*_image.png")
I_RNDM_list = []

for image_path in image_paths:
    I_rndm = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    I_rndm_gry2 = I_rndm.astype(np.double)
    I_rndm_gry_c_vec = I_rndm_gry2.T.reshape(-1, 1)
    I_RNDM_list.append(I_rndm_gry_c_vec)

I_RNDM = np.hstack(I_RNDM_list)
I_RNDM = torch.tensor(I_RNDM, dtype=torch.float32).to(device)

# 目標 - 現在のジョイント角度差
d_pose = PO - POR

# 目標 - 現在の画像差分
d_img = I_DSR - I_RNDM
d_img_t = d_img.T

# 疑似逆行列の計算
pinv_d_img = torch.linalg.inv(d_img_t @ d_img) @ d_img_t
pinv_int_mat = d_pose @ pinv_d_img

# 最小二乗法の精度計算
hyoka = (pinv_int_mat @ d_img) - d_pose
norm = torch.norm(hyoka)
print(norm)

# 結果の保存
# np.savetxt('~/vs_ws/src/moveit_tutorials/scripts_fork/pinv_int_mat/pinv_int_mat_double_remove_avspos.csv', pinv_int_mat.cpu().numpy(), delimiter=',')



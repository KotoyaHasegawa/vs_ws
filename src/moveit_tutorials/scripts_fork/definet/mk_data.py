# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import pandas as pd
import csv
import math
import random
import itertools
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


# CSVファイルのパス

# folder_path = './data'
# # folder_path = '/home/nattomaki/vs_ws/src/moveit_tutorials/scripts_fork/ch07/data'
# file_path = './rndmth_result/random_poseordel.csv'
# # file_path = '/home/nattomaki/vs_ws/src/moveit_tutorials/scripts_fork/ch07/rndmth_result/random_poseordel.csv'
# data_folder = './output.csv'
# # data_folder = '/home/nattomaki/vs_ws/src/moveit_tutorials/scripts_fork/ch07/output.csv'

# select_data = 10

# folder_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\data'
folder_path = './data'
# file_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\\rndmth_result\\random_poseordel.csv'
file_path = './rndmth_result/random_poseordel.csv'
# data_folder = 'C:\Python_workspace\deep-learning-from-scratch\ch07\output.csv'
data_folder = './output.csv'

select_data = 10000
# CSVファイルの読み込み
csv_data = pd.read_csv(data_folder,header=None)
csv_data = csv_data.values
csv_data  = np.delete(csv_data, 0, axis=0)
csv_data  = np.delete(csv_data, 0, axis=1)
print(csv_data.shape[0])

data_1dim = []
for i in range(csv_data.shape[0]):
    csv_data_col = csv_data[i]
    data_1dim.append(csv_data_col)

# n = math.perm(1000,2)

data_list = list(itertools.combinations(csv_data, 2))
data_list = list(itertools.combinations_with_replacement(csv_data, 2))
# same_pairs = list(product(csv_data, repeat=1))
# data_list.append(same_pairs)

# random_data = random.sample(data_list, select_data )
random_data_np = np.array(data_list)

image_pairs = []
pose_pairs = []

for i in range(random_data_np.shape[0]):
    img_pose_pair = random_data_np[i,:]
    image_pairs.append(img_pose_pair[:,0])
    pose_pairs.append(img_pose_pair[:,1:])


# 画像データと正解データのリスト
image_pairs = np.array(image_pairs)
labels = np.array(pose_pairs).astype(float)

for i in range(labels.shape[0]):
    for j in range(labels.shape[1]):
        if labels[i, j, 5] < 0:
            # print(labels[i, j, :])
            labels[i, j, 5] += 6.283185307
            # print(labels[i, j, :])

delta = labels[:,0,:]-labels[:,1,:]

delta = np.array(delta, dtype=object)

result = np.append(image_pairs, delta, axis=1)
# print(result)

# 条件に基づいて行を削除
# condition = np.abs(result[:, 2].astype(float)) > 1e-5
condition = np.logical_or(np.abs(result[:, 2].astype(float)) > 1e-5, result[:, 2].astype(float) == 0.0)
result_filtered = result[condition]
# print(result_filtered)

result_list = list(result)
random_data = random.sample(result_list, select_data )
# print(random_data)

# CSVファイルに書き込む

csv_file_path = './dataset.csv'

with open(csv_file_path, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(random_data)

# csv_file_path = './definet/dataset_full_delta.csv'
# with open(csv_file_path, 'w', newline='') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(delta)



#     # 3次元リストの各行を展開してCSVに書き込む
#     for row in eee:
#         csv_writer.writerow([element for sublist in row for element in sublist])

# csv_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\dataset.txt'
# np.savetxt(csv_path, random_data)
# with open(csv_path, 'w') as file:
#     writer = csv.writer(file)
#     writer.writerows(random_data)
# random_data.to_csv("dataset.csv", encoding="shift_jis")




# select_data = 32
# # CSVデータから2つの行をランダムに選択
# random_rows = random.sample(range(csv_data.shape[0]), select_data)

# # 選択された行を取り出す
# data = csv_data[random_rows, :]

# iamge_data = csv_data[:,0]
# # print(iamge_data)
# pose_data = csv_data[:,1:]
# pose_data = pose_data.astype(float)
# print(pose_data.dtypes)
# pose_data = pose_data.apply(pd.to_numeric, errors='coerce')

# image_pairs, labels = C(iamge_data, pose_data)
# print(len(image_pairs))

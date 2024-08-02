# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import pandas as pd
import random
from itertools import combinations, product
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from defnet import DefiNet
from common.definet_trainer import Trainer

# 画像が保存されているフォルダ
folder_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\data_try'
# CSVファイルの読み込み
file_path = 'C:\\Python_workspace\\deep-learning-from-scratch\\ch07\\rndmth_result\\random_poseordel_try.csv'  # ファイルのパスを指定してください
pose_data = pd.read_csv(file_path, header=None)
pose_data = pose_data.values


# フォルダ内の全てのpngファイルをリストアップ
image_files = [f for f in os.listdir(folder_path) if f.endswith('.png')]

# 画像のペアを作る
image_pairs = list(product(image_files, repeat=2))
print(len(image_pairs))

#poseをペアを作る+差分を計算
num_rows = pose_data.shape[0]
pose_pairs = list(product(range(num_rows), repeat=2))

delta=[]
for idx in pose_pairs:
    cul=[pose_data[idx[0]],pose_data[idx[1]]]
    delta.append(cul)

# delta=[]
# for idx in pose_pairs:
#     cul=pose_data[idx[0]]-pose_data[idx[1]]
#     delta.append(cul)

# print(delta)

# ラベルの名前取得
numbers = list(range(1, len(image_pairs)))
number_pairs = list(product(numbers, repeat=2))

# 画像データと正解データのリスト
labels = delta

# データの読み込み
x_train, x_test, t_train, t_test = train_test_split(image_pairs, labels, test_size=0.2, random_state=42)
# 処理に時間のかかる場合はデータを削減
#x_train, t_train = x_train[:5000], t_train[:5000]
#x_test, t_test = x_test[:1000], t_test[:1000]

max_epochs = 2

network = DefiNet(folder_path=folder_path, input_dim=(3,256,256),
                        conv_param = {'filter_num': 64, 'filter_size': 3, 'pad': 1, 'stride': 1},
                        hidden_size=512, output_size=7, weight_init_std=0.01, loss_alfa=1.0, loss_beta=1.0)

trainer = Trainer(network,x_train, t_train, x_test, t_test,folder_path,
                  epochs=max_epochs, mini_batch_size=5,
                  optimizer='Adam', optimizer_param={'lr': 0.001},
                  evaluate_sample_num_per_epoch=1000)
trainer.train()

# パラメータの保存
network.save_params("params.pkl")
print("Saved Network Parameters!")

# グラフの描画
markers = {'train': 'o', 'test': 's'}
x = np.arange(max_epochs)
plt.plot(x, trainer.train_acc_list, marker='o', label='train', markevery=2)
plt.plot(x, trainer.test_acc_list, marker='s', label='test', markevery=2)
plt.xlabel("epochs")
plt.ylabel("accuracy")
plt.ylim(0, 1.0)
plt.legend(loc='lower right')
plt.show()

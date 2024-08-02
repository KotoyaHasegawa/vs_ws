# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import pandas as pd
import random
import imageio
import torch
from itertools import combinations, product
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pytorch_definet import DefiNet
from pytorch_definet_trainer import Trainer


# 画像が保存されているフォルダ
# folder_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\data'
folder_path = './data'
# CSVファイルの読み込み
# file_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\\rndmth_result\\random_poseordel.csv'
file_path = './rndmth_result/random_poseordel.csv'  # ファイルのパスを指定してください

# dataset_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\dataset.csv'
dataset_path = './dataset.csv'

img_withpose_csv = pd.read_csv(dataset_path, header=None)
img_withpose_np = img_withpose_csv.values
img_withpose = img_withpose_np.reshape(img_withpose_np.shape[0], 1, 8)

image_pairs = []
pose_delta = []

for i in range(img_withpose_np.shape[0]):
    img_pose_pair = img_withpose[i,:]
    image_pairs.append(img_pose_pair[:,:2])
    pose_delta.append(img_pose_pair[:,2:])



image_pairs = np.squeeze(np.array(image_pairs))
labels = np.squeeze(np.array(pose_delta).astype(float))

# データの読み込み
x_train, x_val, t_train, t_val = train_test_split(image_pairs, labels, test_size=20) #random_state=42)
# device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
device = torch.device('cuda')
print(torch.cuda.is_available())
max_epochs = 1000

network = DefiNet(device=device,folder_path=folder_path, input_dim=(3,256,256),
                        conv_param = {'filter_num': 64, 'filter_size': 3, 'pad': 1, 'stride': 1},
                        hidden_size=512, output_size=6,  loss_alfa=1, loss_beta=1).to(device)
network = network

trainer = Trainer(device ,network,x_train, t_train, x_val, t_val,folder_path,
                  epochs=max_epochs, mini_batch_size=30,optimizer_param=0.001,
                  optimizer='Adam')

trainer.train()

# パラメータの保存
torch.save(network.state_dict(), 'definet_params.pt')
# # network.save_params("params.pkl")
print("Saved Network Parameters!")


train_loss_train_list = np.array(trainer.train_loss_train_list)
train_loss_val_list = np.array(trainer.train_loss_val_list)

# グラフの描画
markers = {'train': 'o', 'test': 's'}
x = np.arange(max_epochs)
plt.plot(x, train_loss_train_list, marker='o', label='train', markevery=1)
plt.plot(x, train_loss_val_list, marker='s', label='test', markevery=1)
plt.xlabel("epochs")
plt.ylabel("loss")
plt.ylim(0, 0.03)
plt.legend(loc='lower right')
plt.show()


# print(trainer.current)
train_acc = np.array(trainer.current)
val_acc = np.array(trainer.current_val)

# グラフの描画
markers = {'train': 'o', 'test': 's'}
x = np.arange(max_epochs)
plt.plot(x, train_acc, marker='o', label='train', markevery=1)
plt.plot(x, val_acc, marker='s', label='test', markevery=1)
plt.xlabel("epochs")
plt.ylabel("acc")
plt.ylim(0, 1)
plt.legend(loc='lower right')
plt.show()

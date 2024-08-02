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
from pytorch_vit import ViT
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
img_withpose = img_withpose_np.reshape(img_withpose_np.shape[0], 1, 9)

image_pairs = []
pose_delta = []

for i in range(img_withpose_np.shape[0]):
    img_pose_pair = img_withpose[i,:]
    image_pairs.append(img_pose_pair[:,:2])
    pose_delta.append(img_pose_pair[:,2:])


# 画像データと正解データのリスト
image_pairs = np.squeeze(np.array(image_pairs))
labels = np.squeeze(np.array(pose_delta).astype(float))

# データの読み込み
x_train, x_val, t_train, t_val = train_test_split(image_pairs, labels, test_size=10) #random_state=42)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(torch.cuda.is_available())
# device = torch.device('cuda')
max_epochs = 10

network = ViT(image_size =256, patch_size = 16, n_classes =0, dim = 1024, depth = 3, n_heads = 2, channels = 3, mlp_dim = 256)
network = network

trainer = Trainer(device ,network,x_train, t_train, x_val, t_val,folder_path,
                  epochs=max_epochs, mini_batch_size=10,optimizer_param=0.001,
                  optimizer='Adam')

trainer.train()

# パラメータの保存
torch.save(network.state_dict(), 'definet_params.pt')
# network.save_params("params.pkl")
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
plt.ylim(0, 50)
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

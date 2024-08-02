# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import pandas as pd
import random
import gc
import torch
from itertools import combinations, product
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from pytorch_definet import DefiNet
import datetime
from tqdm import tqdm


def test(net,params, x, t, mini_batch_size, device):
    
    gc.collect()
    # 設定
    net.load_state_dict(params)
    net.eval()
    train_size = x.shape[0]
    train_loss_train_list = []
    current = []

    iter_per_epoch = int(max(train_size / mini_batch_size, 1))
    numbers = list(range(0,  train_size))
    # print(numbers)

    batch=[]
    for i in range(iter_per_epoch):
        selected_numbers = numbers[i*mini_batch_size:(i+1)*mini_batch_size]
        batch.append(selected_numbers)

    acc_sum = 0.0
    loss_train = 0.0
    loss_validation = 0.0
    # bar = tqdm(total = len(batch))

    for batch_mask in tqdm(batch):
        # print(batch_mask)
        # bar.update(1)
        x_batch=[]
        t_batch=[]
        for idx in batch_mask:
            x_batchi = x[idx]
            t_batchi = t[idx]
            x_batch.append(x_batchi)
            t_batch.append(t_batchi)

        

        result_train, loss = net.forward_and_loss(x_batch ,t_batch)
        loss_avg = torch.mean(loss).to(device)
        # print(loss_avg)
        acc = net.accuracy(result_train ,t_batch, mini_batch_size)
        # print(acc)
        acc_sum += acc

        loss_train += loss_avg.item()

    train_loss_train_list.append(loss_train/iter_per_epoch)
    print("{} , Training loss{}".format(datetime.datetime.now(),loss_train/iter_per_epoch))
    print("{} , validation loss{}".format(datetime.datetime.now(),loss_validation))
    
    # evalute by validation 
    # result_val, loss_val = self.network.forward_and_loss(self.x_test ,self.t_test)
    # loss_avg_val = torch.mean(loss_val).to(self.device)
    # loss_validation = loss_avg_val.item()
    # val_acc = self.network.accuracy(result_val, self.t_test, self.x_test.shape[0])
    # val_acc_sum += val_acc

    print(acc_sum /x.shape[0])
    current.append(acc_sum /x.shape[0])


    # gc.collect()
    del x_batch
    del t_batch

    gc.collect()



# 画像が保存されているフォルダ
# folder_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\data'
folder_path = './data'
# CSVファイルの読み込み
# file_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\\rndmth_result\\random_poseordel.csv'
file_path = './rndmth_result/random_poseordel.csv'  # ファイルのパスを指定してください

# dataset_path = 'C:\Python_workspace\deep-learning-from-scratch\ch07\dataset.csv'
dataset_path = './dataset2.csv'

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



device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
net = DefiNet(device=device,folder_path=folder_path, input_dim=(3,256,256),
                        conv_param = {'filter_num': 64, 'filter_size': 3, 'pad': 1, 'stride': 1},
                        hidden_size=512, output_size=6,  loss_alfa=1, loss_beta=1).to(device)

# パラメータを取得
params = torch.load('definet_params_epoch800.pt', map_location=torch.device(device))


# 設定
test(net,params, image_pairs, labels, 1, device)
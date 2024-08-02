# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import random
import gc
import torch
import torch.optim as optim
import datetime
import gc
from tqdm import tqdm

class Trainer:
    """ニューラルネットの訓練を行うクラス
    """
    def __init__(self, device, network, x_train, t_train, x_val, t_val, folder_path,
                 epochs, mini_batch_size,optimizer_param,
                 optimizer='Adam',verbose=True):
        self.network = network
        self.verbose = verbose
        self.x_train = x_train
        self.t_train = t_train
        self.x_test = x_val
        self.t_test = t_val
        self.epochs = epochs
        self.batch_size = mini_batch_size
        self.folder_path = folder_path
        self.optimizer_param = optimizer_param
        self.device = device

        self.train_size = len(x_train)
        self.iter_per_epoch = int(max(self.train_size / mini_batch_size, 1))
        self.max_iter = int(epochs * self.iter_per_epoch)
        self.current_iter = 0
        self.current = []
        self.current_val = []

        self.train_loss_train_list = []
        self.train_loss_val_list = []
        self.train_acc_list = []
        self.test_acc_list = []

    def train_step(self):
        for epoch in range(self.epochs):
            gc.collect()
            numbers = list(range(0, self.train_size))
            random.shuffle(numbers)
            # print(numbers)

            batch=[]
            for i in range(self.iter_per_epoch):
                selected_numbers = numbers[i*self.batch_size:(i+1)*self.batch_size]
                batch.append(selected_numbers)

            print(f'epoch : {epoch+1}')
            acc_sum = 0.0
            val_acc_sum = 0.0
            loss_train = 0.0
            loss_validation = 0.0
            # bar = tqdm(total = len(batch))
    
            for batch_mask in tqdm(batch):
                # print(batch_mask)
                # bar.update(1)
                x_batch=[]
                t_batch=[]
                for idx in batch_mask:
                    x_batchi = self.x_train[idx]
                    t_batchi = self.t_train[idx]
                    x_batch.append(x_batchi)
                    t_batch.append(t_batchi)

                # print(self.network.parameters())
                # print(self.network.state_dict().keys()) #パラメータ確認
                # print("compute loss")
                result_train, loss = self.network.forward_and_loss(x_batch ,t_batch)
                loss_avg = torch.mean(loss).to(self.device)
                # print(loss_avg)
                acc = self.network.accuracy(result_train ,t_batch, self.batch_size)
                # print(acc)
                acc_sum += acc

                # params = torch.tensor(self.network.parameters(), requires_grad=True)
                optimizer = optim.Adam(self.network.parameters(), lr=self.optimizer_param)

                optimizer.zero_grad()
                loss_avg.backward()
                optimizer.step()

                loss_train += loss_avg.item()


                # self.train_loss_train_list.append(loss_train)
            # del x_batch
            # del t_batch
            # gc.collect()
                

            if epoch == 1 or epoch % 1 ==0:
            # evalute by validation 
                self.train_loss_train_list.append(loss_train/self.iter_per_epoch)

                result_val, loss_val = self.network.forward_and_loss(self.x_test ,self.t_test)
                loss_avg_val = torch.mean(loss_val).to(self.device)
                loss_validation = loss_avg_val.item()
                self.train_loss_val_list.append(loss_validation)

                val_acc = self.network.accuracy(result_val, self.t_test, self.x_test.shape[0])
                val_acc_sum += val_acc
                print("{} Epoch {}, Training loss{}".format(datetime.datetime.now(),epoch+1,loss_train/self.iter_per_epoch))
                print("{} Epoch {}, validation loss{}".format(datetime.datetime.now(),epoch+1,loss_validation))
            
            # evalute by validation 
            # result_val, loss_val = self.network.forward_and_loss(self.x_test ,self.t_test)
            # loss_avg_val = torch.mean(loss_val).to(self.device)
            # loss_validation = loss_avg_val.item()
            # val_acc = self.network.accuracy(result_val, self.t_test, self.x_test.shape[0])
            # val_acc_sum += val_acc

            print(acc_sum /self.x_train.shape[0])
            print(val_acc_sum /self.x_test.shape[0])
            self.current.append(acc_sum /self.x_train.shape[0])
            self.current_val.append(val_acc_sum /self.x_test.shape[0])

            # gc.collect()
            del x_batch
            del t_batch

            gc.collect()




    def train(self):
        # for i in range(self.max_iter):
        self.train_step()

        # val_acc = self.network.accuracy(self.x_test, self.t_test,40)
        # print('val_acc ='+ val_acc)

        # if self.verbose:
        #     print("=============== Final Test Accuracy ===============")
        #     print("test acc:" + str(test_acc))


# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import numpy as np
import cv2
from common.optimizer import *

class Trainer:
    """ニューラルネットの訓練を行うクラス
    """
    def __init__(self, network, x_train, t_train, x_test, t_test, folder_path,
                 epochs=2, mini_batch_size=5,
                 optimizer='SGD', optimizer_param={'lr':0.01},
                 evaluate_sample_num_per_epoch=None, verbose=True):
        self.network = network
        self.verbose = verbose
        self.x_train = x_train
        self.t_train = t_train
        self.x_test = x_test
        self.t_test = t_test
        self.epochs = epochs
        self.batch_size = mini_batch_size
        self.evaluate_sample_num_per_epoch = evaluate_sample_num_per_epoch
        self.folder_path = folder_path

        # optimizer
        optimizer_class_dict = {'sgd':SGD, 'momentum':Momentum, 'nesterov':Nesterov,
                                'adagrad':AdaGrad, 'rmsprop':RMSprop, 'adam':Adam}
        self.optimizer = optimizer_class_dict[optimizer.lower()](**optimizer_param)

        # separate x_dataset
        # rem_x=[]
        # for file in self.x_train:
        #     xi=[]
        #     for data in file:
        #         # 画像ファイルのパス
        #         image_path = os.path.join(self.folder_path, data)
        #         image = cv2.imread(image_path)
        #         xi.append(np.array(image))
        #     rem_x.append(xi)

        # print(len(rem_x))
        # print(np.shape(rem_x))


        # self.x_train = rem_x
        # self.train_size = len(rem_x)
        self.train_size = len(x_train)
        self.iter_per_epoch = max(self.train_size / mini_batch_size, 1)
        self.max_iter = int(epochs * self.iter_per_epoch)
        self.current_iter = 0
        self.current_epoch = 0

        self.train_loss_list = []
        self.train_acc_list = []
        self.test_acc_list = []

    def train_step(self):
        batch_mask = np.random.choice(self.train_size, self.batch_size)
        x_batch=[]
        for idx in batch_mask:
            x_batchi = self.x_train[idx]
            x_batch.append(x_batchi)

        t_batch = []
        for idx in batch_mask:
            t_batchi = self.t_train[idx]
            t_batch.append(t_batchi)

        grads = self.network.gradient(x_batch, t_batch)
        self.optimizer.update(self.network.params, grads)

        loss = self.network.loss(x_batch, t_batch)
        self.train_loss_list.append(loss)
        # if self.verbose: print("train loss:" + str(loss))

        # if self.current_iter % self.iter_per_epoch == 0:
        #     self.current_epoch += 1

        #     x_train_sample, t_train_sample = np.array(self.x_train), np.array(self.t_train)
        #     x_test_sample, t_test_sample = np.array(self.x_test), np.array(self.t_test)
        #     if not self.evaluate_sample_num_per_epoch is None:
        #         t = self.evaluate_sample_num_per_epoch
        #         x_train_sample, t_train_sample = self.x_train[:t], self.t_train[:t]
        #         x_test_sample, t_test_sample = self.x_test[:t], self.t_test[:t]

        #     train_acc = self.network.accuracy(x_train_sample, t_train_sample)
        #     test_acc = self.network.accuracy(x_test_sample, t_test_sample)
        #     self.train_acc_list.append(train_acc)
        #     self.test_acc_list.append(test_acc)

        #     if self.verbose: print("=== epoch:" + str(self.current_epoch) + ", train acc:" + str(train_acc) + ", test acc:" + str(test_acc) + " ===")
        # self.current_iter += 1

    def train(self):
        for i in range(self.max_iter):
            self.train_step()

        test_acc = self.network.accuracy(self.x_test, self.t_test)

        if self.verbose:
            print("=============== Final Test Accuracy ===============")
            print("test acc:" + str(test_acc))


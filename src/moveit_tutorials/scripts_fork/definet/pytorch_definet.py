# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import pickle
import torch
import torch.nn as nn
import imageio
import numpy as np
import scipy.stats
# import cv2
from collections import OrderedDict
from common.layers import *
from common.gradient import numerical_gradient
from backbone import Backbone


class DefiNet(nn.Module):
    def __init__(self ,device ,folder_path ,input_dim=(3, 256, 256),
                 conv_param={'filter_num':64, 'filter_size':3, 'pad':1, 'stride':1},
                 hidden_size=512, output_size=6,  loss_alfa=1.0, loss_beta=1.0,
                 init_weights: bool = True):
        filter_num = conv_param['filter_num']
        filter_size = conv_param['filter_size']
        filter_pad = conv_param['pad']
        filter_stride = conv_param['stride']
        self.input_size = input_dim[1]
        self.folder_path = folder_path
        self.device = device
        super(DefiNet, self).__init__()

        # レイヤの生成

        # 1
        self.layers = OrderedDict()
        self.norm0 = nn.BatchNorm2d(filter_size)
        self.conv1 = nn.Conv2d(input_dim[0], filter_num, filter_size, stride=filter_stride, padding=filter_pad)
        self.relu1 = nn.ReLU()
        self.norm1 = nn.BatchNorm2d(filter_num)
        self.conv2 = nn.Conv2d(filter_num, filter_num, filter_size, stride=filter_stride, padding=filter_pad)
        self.norm1 = self.norm1 
        self.relu2= nn.ReLU()
        # 2
        self.pool1 = nn.MaxPool2d(2, stride=2)
        self.conv3 = nn.Conv2d(filter_num, filter_num*2, filter_size, stride=filter_stride, padding=filter_pad)
        self.relu3 = nn.ReLU()
        self.norm2 = nn.BatchNorm2d(filter_num*2)
        self.conv4 = nn.Conv2d(filter_num*2, filter_num*2, filter_size, stride=filter_stride, padding=filter_pad)
        self.relu4 = nn.ReLU()
        self.norm2 = self.norm2
        # 3
        self.pool2 = nn.MaxPool2d(2, stride=2)
        self.conv5 = nn.Conv2d(filter_num*2, filter_num*(2**2), filter_size, stride=filter_stride, padding=filter_pad)
        self.relu5 = nn.ReLU()
        self.norm3 = nn.BatchNorm2d(filter_num*(2**2))
        self.conv6 = nn.Conv2d(filter_num*(2**2), filter_num*(2**2), filter_size, stride=filter_stride, padding=filter_pad)
        self.relu6 = nn.ReLU()
        self.norm3 = self.norm3
        self.conv7 = nn.Conv2d(filter_num*(2**2), filter_num*(2**2), filter_size,  stride=filter_stride, padding=filter_pad)
        self.relu7 = nn.ReLU()
        self.norm3 = self.norm3
        # 4
        self.pool3 = nn.MaxPool2d(2, stride=2)
        self.conv8 = nn.Conv2d(filter_num*(2**2), filter_num*(2**3), filter_size,  stride=filter_stride, padding=filter_pad)
        self.relu8 = nn.ReLU()
        self.norm4 = nn.BatchNorm2d(filter_num*(2**3))
        self.conv9 = nn.Conv2d(filter_num*(2**3), filter_num*(2**3), filter_size,  stride=filter_stride, padding=filter_pad)
        self.relu9 = nn.ReLU()
        self.norm4 = self.norm4
        self.conv10 = nn.Conv2d(filter_num*(2**3), filter_num*(2**3), filter_size,  stride=filter_stride, padding=filter_pad)
        self.relu10= nn.ReLU()
        self.norm4 = self.norm4
        # 5
        self.pool4 = nn.MaxPool2d(2, stride=2)
        self.conv11 = nn.Conv2d(filter_num*(2**3), filter_num*(2**3), filter_size,  stride=filter_stride, padding=filter_pad)
        self.relu11 = nn.ReLU()
        self.norm5 = nn.BatchNorm2d(filter_num*(2**3))
        self.conv12 = nn.Conv2d(filter_num*(2**3), filter_num*(2**3), filter_size,  stride=filter_stride, padding=filter_pad)
        self.relu12= nn.ReLU()
        self.norm5 = self.norm5
        self.conv13 = nn.Conv2d(filter_num*(2**3), filter_num*(2**3), filter_size,  stride=filter_stride, padding=filter_pad)
        self.relu13 = nn.ReLU()
        self.norm5 = self.norm5

        # self.gpool = GlobalAveragePooling2D_pytorch()
        self.gpool= nn.AdaptiveAvgPool2d(output_size=(1,1))
        self.fclayers = nn.Linear(hidden_size, output_size)
        self.loss_layer = definet_loss(loss_alfa,loss_beta,self.device)


        if init_weights:
            for m in self.modules():
                if isinstance(m, torch.nn.Conv2d):
                    #n = m.kernel_size[0] * m.kernel_size[1] * m.out_channels
                    #m.weight.data.normal_(0, np.sqrt(2. / n))
                    m.weight.detach().normal_(0, 0.06)
                    if m.bias is not None:
                        m.bias.detach().zero_()
                elif isinstance(m, torch.nn.Linear):
                    m.weight.detach().normal_(0, 0.06)
                    m.bias.detach().detach().zero_()



    def Siamise_forward(self, x):
        x_norm = (x-255/2) / 255


        out_1 = self.relu2(self.conv2(self.relu1(self.conv1(x_norm))))
        # out_1 = self.relu2(self.norm1(self.conv2(self.relu1(self.norm1(self.conv1(x_norm))))))
        out_1_pool1 = self.pool1(out_1)
        # print(out_1_pool1.device)

        out_2 = self.relu4(self.conv4(self.relu3(self.conv3(out_1_pool1))))
        # out_2 = self.relu4(self.norm2(self.conv4(self.relu3(self.norm2(self.conv3(out_1_pool1))))))
        out_2_pool2 = self.pool2(out_2)
        # print(out_2.shape)

        out_3 = self.relu7(self.conv7(self.relu6(self.conv6(self.relu5(self.conv5(out_2_pool2))))))
        # out_3 = self.relu7(self.norm3(self.conv7(self.relu6(self.norm3(self.conv6(self.relu5(self.norm3(self.conv5(out_2_pool2)))))))))
        out_3_pool3 = self.pool3(out_3)
        # print(out_3.shape)

        out_4 = self.relu10(self.conv10(self.relu9(self.conv9(self.relu8(self.conv8(out_3_pool3))))))
        # out_4 = (self.relu10(self.norm4(self.conv10(self.relu9(self.norm4(self.conv9(self.relu8(self.norm4(self.conv8(out_3_pool3))))))))))
        out_4_pool4 = self.pool4(out_4)
        # print(out_4.shape)

        out_5 = self.relu13(self.conv13(self.relu12(self.conv12(self.relu11(self.conv11(out_4_pool4))))))
        # out_5 = (self.relu13(self.norm4(self.conv13(self.relu12(self.norm4(self.conv12(self.relu11(self.norm4(self.conv11(out_4_pool4))))))))))
        # print(out_5.shape)

        return out_5

    def fc_forward(self, x):
        # max_pool = self.gpool.forward(x)
        max_pool = self.gpool(x)
        max_pool = max_pool.view(max_pool.shape[0], -1)

        out = self.fclayers(max_pool)
        # print(out.shape)

        return out



    def forward(self, x1, x2):
        x1 = self.Siamise_forward(x1)
        x2 = self.Siamise_forward(x2)

        # sub = x1/torch.max(x1) - x2/torch.max(x2)
        sub = x1 - x2

        x = self.fc_forward(sub)
        # print(x)

        return x

    def forward_and_loss(self, x ,t):
        """損失関数を求める
        引数のxは入力データ、tは教師ラベル
        """
        x=np.array(x)
        x1 = x[:,0]
        x2 = x[:,1]
        rem_x1, rem_x2 = self.process_images(x1), self.process_images(x2)

        # t_delta = []
        # for idx in t:
        #     cul=idx[0]-idx[1]
        #     t_delta.append(cul)

        t_delta = np.array(t)
        t_delta_norm = self.euler_to_normal(t_delta)
        y_norm = self.forward(rem_x1,rem_x2).to(self.device)
        # print(y.shape)
        y = self.normal_to_euler(y_norm)


        return y, self.loss_layer.forward(y_norm, t_delta_norm)


    def process_images(self, x):
        rem_x=[]
        for file in x:
            # 画像ファイルのパス
            image_path = os.path.join(self.folder_path, file)
            image = imageio.imread(image_path)
            rem_x.append(image)
        rem_x = np.array(rem_x).transpose(0, 3, 1, 2)
        rem_x = torch.from_numpy(rem_x).to(torch.float32)
        # print(torch.min(rem_x))
        rem_x = rem_x.to(self.device)

        return rem_x

    
    def euler_to_normal(self, t):
        max = np.array([[0.05, 0.02 ,0.05, 0.1745, 0.1745, 0.1745]])
        t_norm = np.zeros_like(t)
        for i in range(t.shape[1]): 
            # t_norm[:,i] =  (t[:,i] + max[:, i])/(max[:, i]+max[:, i])
            t_norm[:,i] =  t[:,i] / max[:, i]
            
        return t_norm
    
    def normal_to_euler(self, t):
        max = np.array([0.05, 0.02 ,0.05, 0.1745, 0.1745, 0.1745])
        t_ret = torch.zeros_like(t)
        for i in range(t.shape[1]): 
            # t_ret[:,i] =  t[:,i]*max[i] +t[:,i]*max[i]-max[i]
            t_ret[:,i] =  t[:,i]*max[i] 
        
        return t_ret
    
   

    def accuracy(self, x, t, batch_size):
        # if t.ndim != 1 : t = np.argmax(t, axis=1)

        acc = 0.0
        t = torch.from_numpy(np.array(t)).to('cpu')
        # x = self.normal_to_euler(x)
        error = x.to('cpu')-t

        b = torch.abs(error)
        # 0.001より小さいインデックスを削除
        # condition = torch.all(torch.abs(error) < 0.01, dim=1)
        condition = torch.all(torch.abs(error[:, :3]) < 0.003, dim=1)
        # condition = torch.all(torch.cat([torch.abs(error[:, :3]) < 0.003, torch.abs(error[:, 3:]) < 0.01], dim=1), dim=1)
        acc = torch.sum(condition).item()
        # for i in range(int(x.shape[0] / batch_size)):
        #     tx = x[i*batch_size:(i+1)*batch_size]
        #     tt = t[i*batch_size:(i+1)*batch_size]
        #     y = self.predict(tx)
        #     y = np.argmax(y, axis=1)
        #     acc += np.sum(y == tt)
        # p = x.size(0)
        return acc #/ x.size(0)



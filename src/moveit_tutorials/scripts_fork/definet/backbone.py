# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import pickle
import numpy as np
from collections import OrderedDict
from common.layers import *
from common.gradient import numerical_gradient


class Backbone:
    """単純なConvNet

    conv - relu - pool - affine - relu - affine - softmax

    Parameters
    ----------
    input_size : 入力サイズ（MNISTの場合は512）
    hidden_size_list : 隠れ層のニューロンの数のリスト（e.g. [100, 100, 100]）
    output_size : 出力サイズ（MNISTの場合は512）
    activation : 'relu' or 'sigmoid'
    weight_init_std : 重みの標準偏差を指定（e.g. 0.01）
        'relu'または'he'を指定した場合は「Heの初期値」を設定
        'sigmoid'または'xavier'を指定した場合は「Xavierの初期値」を設定
    """
    def __init__(self, input_dim=(3, 256, 256),
                 conv_param={'filter_num':64, 'filter_size':3, 'pad':1, 'stride':1},
                 hidden_size=8, output_size=256, weight_init_std=0.01):
        filter_num = conv_param['filter_num']
        filter_size = conv_param['filter_size']
        filter_pad = conv_param['pad']
        filter_stride = conv_param['stride']
        input_size = input_dim[1]
        conv_output_size = (input_size - filter_size + 2*filter_pad) / filter_stride + 1
        pool_output_size = int(filter_num * (conv_output_size/2) * (conv_output_size/2))

        # レイヤの生成
        # 1
        self.layers = OrderedDict()
        self.layers['Conv1'] = Convolution(self.params['W1'], self.params['b1'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu1'] = Relu()
        self.layers['Conv2'] = Convolution(self.params['W2'], self.params['b2'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu2'] = Relu()
        # 2
        self.layers['Pool1'] = Pooling(pool_h=2, pool_w=2, stride=2)
        self.layers['Conv3'] = Convolution(self.params['W3'], self.params['b3'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu3'] = Relu()
        self.layers['Conv4'] = Convolution(self.params['W4'], self.params['b4'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu4'] = Relu()
        # 3
        self.layers['Pool2'] = Pooling(pool_h=2, pool_w=2, stride=2)
        self.layers['Conv5'] = Convolution(self.params['W5'], self.params['b5'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu5'] = Relu()
        self.layers['Conv6'] = Convolution(self.params['W6'], self.params['b6'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu6'] = Relu()
        self.layers['Conv7'] = Convolution(self.params['W7'], self.params['b7'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu7'] = Relu()
        # 4
        self.layers['Pool3'] = Pooling(pool_h=2, pool_w=2, stride=2)
        self.layers['Conv8'] = Convolution(self.params['W8'], self.params['b8'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu8'] = Relu()
        self.layers['Conv9'] = Convolution(self.params['W9'], self.params['b9'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu9'] = Relu()
        self.layers['Conv10'] = Convolution(self.params['W10'], self.params['b10'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu10'] = Relu()
        # 5
        self.layers['Pool4'] = Pooling(pool_h=2, pool_w=2, stride=2)
        self.layers['Conv11'] = Convolution(self.params['W11'], self.params['b11'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu11'] = Relu()
        self.layers['Conv12'] = Convolution(self.params['W12'], self.params['b12'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu12'] = Relu()
        self.layers['Conv13'] = Convolution(self.params['W13'], self.params['b13'],
                                           conv_param['stride'], conv_param['pad'])
        self.layers['Relu13'] = Relu()


    def forward(self, x):
        for layer in self.layers.values():
            x = layer.forward(x)
        return x



    def backward(self, dout):
        """勾配を求める（誤差逆伝搬法）

        Parameters
        ----------
        x : 入力データ
        t : 教師ラベル

        Returns
        -------
        各層の勾配を持ったディクショナリ変数
            grads['W1']、grads['W2']、...は各層の重み
            grads['b1']、grads['b2']、...は各層のバイアス
        """
        # # forward
        # self.loss(x, t)

        # backward
        # dout = 1
        # dout = self.last_layer.backward(dout)

        layers = list(self.layers.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)

        # 設定
        grads = {}
        grads['W1'], grads['b1'] = self.layers['Conv1'].dW, self.layers['Conv1'].db
        grads['W2'], grads['b2'] = self.layers['Affine1'].dW, self.layers['Affine1'].db
        grads['W3'], grads['b3'] = self.layers['Affine2'].dW, self.layers['Affine2'].db

        return grads

    # def save_params(self, file_name="params.pkl"):
    #     params = {}
    #     for key, val in self.params.items():
    #         params[key] = val
    #     with open(file_name, 'wb') as f:
    #         pickle.dump(params, f)

    # def load_params(self, file_name="params.pkl"):
    #     with open(file_name, 'rb') as f:
    #         params = pickle.load(f)
    #     for key, val in params.items():
    #         self.params[key] = val

    #     for i, key in enumerate(['Conv1', 'Affine1', 'Affine2']):
    #         self.layers[key].W = self.params['W' + str(i+1)]
    #         self.layers[key].b = self.params['b' + str(i+1)]


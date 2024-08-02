# coding: utf-8
import sys, os
sys.path.append(os.pardir)  # 親ディレクトリのファイルをインポートするための設定
import pickle
import numpy as np
import cv2
from collections import OrderedDict
from common.layers import *
from common.gradient import numerical_gradient
from backbone import Backbone


class DefiNet:
    """単純なConvNet

    conv - relu - pool - affine - relu - affine - softmax

    Parameters
    ----------
    input_size : 入力サイズ（MNISTの場合は784）
    hidden_size_list : 隠れ層のニューロンの数のリスト（e.g. [100, 100, 100]）
    output_size : 出力サイズ（MNISTの場合は10）
    activation : 'relu' or 'sigmoid'
    weight_init_std : 重みの標準偏差を指定（e.g. 0.01）
        'relu'または'he'を指定した場合は「Heの初期値」を設定
        'sigmoid'または'xavier'を指定した場合は「Xavierの初期値」を設定
    """
    def __init__(self,folder_path ,input_dim=(3, 256, 256),
                 conv_param={'filter_num':64, 'filter_size':3, 'pad':1, 'stride':1},
                 hidden_size=512, output_size=7, weight_init_std=0.01, loss_alfa=1.0, loss_beta=1.0):
        filter_num = conv_param['filter_num']
        filter_size = conv_param['filter_size']
        filter_pad = conv_param['pad']
        filter_stride = conv_param['stride']
        input_size = input_dim[1]
        conv_output_size = (input_size - filter_size + 2*filter_pad) / filter_stride + 1
        pool_output_size = int(filter_num * (conv_output_size/2) * (conv_output_size/2))
        self.folder_path = folder_path

        # 重みの初期化
        self.params = {}
        self.params['W1'] = weight_init_std * \
                            np.random.randn(filter_num, input_dim[0], filter_size, filter_size)
        self.params['b1'] = np.zeros(filter_num)#N64C3
        self.params['W2'] = weight_init_std * \
                            np.random.randn(filter_num, filter_num, filter_size, filter_size)
        self.params['b2'] = np.zeros(filter_num)#N64C64
        self.params['W3'] = weight_init_std * \
                            np.random.randn(filter_num*2, filter_num, filter_size, filter_size)
        self.params['b3'] = np.zeros(filter_num*2)#N128C64
        self.params['W4'] = weight_init_std * \
                            np.random.randn(filter_num*2, filter_num*2, filter_size, filter_size)
        self.params['b4'] = np.zeros(filter_num*2)#N128C128
        self.params['W5'] = weight_init_std * \
                            np.random.randn(filter_num*(2**2), filter_num*2, filter_size, filter_size)
        self.params['b5'] = np.zeros(filter_num*2*2)#N256C128
        self.params['W6'] = weight_init_std * \
                            np.random.randn(filter_num*(2**2), filter_num*(2**2), filter_size, filter_size)
        self.params['b6'] = np.zeros(filter_num*2*2)#N256C256
        self.params['W7'] = weight_init_std * \
                            np.random.randn(filter_num*(2**2), filter_num*(2**2), filter_size, filter_size)
        self.params['b7'] = np.zeros(filter_num*2*2)#N256C256
        self.params['W8'] = weight_init_std * \
                            np.random.randn(filter_num*(2**3), filter_num*(2**2), filter_size, filter_size)
        self.params['b8'] = np.zeros(filter_num*(2**3))#N512C256
        self.params['W9'] = weight_init_std * \
                            np.random.randn(filter_num*(2**3), filter_num*(2**3), filter_size, filter_size)
        self.params['b9'] = np.zeros(filter_num*(2**3))#N512C512
        self.params['W10'] = weight_init_std * \
                            np.random.randn(filter_num*(2**3), filter_num*(2**3), filter_size, filter_size)
        self.params['b10'] = np.zeros(filter_num*(2**3))#N512C512

        self.params['W11'] = weight_init_std * \
                            np.random.randn(filter_num*(2**3), filter_num*(2**3), filter_size, filter_size)
        self.params['b11'] = np.zeros(filter_num*(2**3))#N512C512
        self.params['W12'] = weight_init_std * \
                            np.random.randn(filter_num*(2**3), filter_num*(2**3), filter_size, filter_size)
        self.params['b12'] = np.zeros(filter_num*(2**3))#N512C512
        self.params['W13'] = weight_init_std * \
                            np.random.randn(filter_num*(2**3), filter_num*(2**3), filter_size, filter_size)
        self.params['b13'] = np.zeros(filter_num*(2**3))#N512C512

        self.params['W14'] = weight_init_std * \
                            np.random.randn(hidden_size, output_size)
        self.params['b14'] = np.zeros(output_size)


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

        self.fclayers = OrderedDict()
        self.fclayers['Global Pooling'] = GlobalAveragePooling2D()
        self.fclayers['Fuuly connected'] = Affine(self.params['W14'], self.params['b14'])

        self.last_layer = Linear_WithLoss(loss_alfa,loss_beta)

    def predict(self, x1, x2):
        for layer in self.layers.values():
            x1 = layer.forward(x1)
            x2 = layer.forward(x2)
        x = x1 - x2
        for layer in self.fclayers.values():
            x = layer.forward(x)

        return x

    def loss(self, x ,t):
        """損失関数を求める
        引数のxは入力データ、tは教師ラベル
        """
        x=np.array(x)
        x1 = x[:,0]
        rem_x1=[]
        for file in x1:
            # 画像ファイルのパス
            image_path = os.path.join(self.folder_path, file)
            image = cv2.imread(image_path)
            rem_x1.append(image)
        # print(np.shape(rem_x1))
        rem_x1=np.array(rem_x1).transpose(0, 3, 1, 2)
        # print(np.shape(rem_x1))

        x2 = x[:,1]
        rem_x2=[]
        for file in x2:
            # 画像ファイルのパス
            image_path = os.path.join(self.folder_path, file)
            image = cv2.imread(image_path)
            rem_x2.append(image)
        rem_x2=np.array(rem_x2).transpose(0, 3, 1, 2)

        t_delta = []
        for idx in t:
            cul=idx[0]-idx[1]
            t_delta.append(cul)

        y = self.predict(rem_x1,rem_x2)
        return self.last_layer.forward(y, t_delta)



    def accuracy(self, x, t, batch_size=5):
        # if t.ndim != 1 : t = np.argmax(t, axis=1)

        # acc = 0.0
        x = np.array(x)
        for i in range(int(x.shape[0] / batch_size)):
            tx = x[i*batch_size:(i+1)*batch_size]
            tt = t[i*batch_size:(i+1)*batch_size]
            y = self.predict(tx)
            y = np.argmax(y, axis=1)
            acc += np.sum(y == tt)

        return acc / x.shape[0]

    def numerical_gradient(self, x, t):
        """勾配を求める（数値微分）

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
        loss_w = lambda w: self.loss(x, t)

        grads = {}
        for idx in (1, 2, 3):
            grads['W' + str(idx)] = numerical_gradient(loss_w, self.params['W' + str(idx)])
            grads['b' + str(idx)] = numerical_gradient(loss_w, self.params['b' + str(idx)])

        return grads

    def gradient(self, x, t):
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
        # forward
        self.loss(x, t)

        # backward
        print("start backward")
        dout = 1
        dout = self.last_layer.backward(dout)

        fclayers = list(self.fclayers.values())
        fclayers.reverse()
        for layer in fclayers:
            dout = layer.backward(dout)

        # dout1 = dout
        # dout2 = -dout

        layers = list(self.layers.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)

        # 設定
        grads = {}
        grads['W1'], grads['b1'] = self.layers['Conv1'].dW, self.layers['Conv1'].db
        grads['W2'], grads['b2'] = self.layers['Conv2'].dW, self.layers['Conv2'].db
        grads['W3'], grads['b3'] = self.layers['Conv3'].dW, self.layers['Conv3'].db
        grads['W4'], grads['b4'] = self.layers['Conv4'].dW, self.layers['Conv4'].db
        grads['W5'], grads['b5'] = self.layers['Conv5'].dW, self.layers['Conv5'].db
        grads['W6'], grads['b6'] = self.layers['Conv6'].dW, self.layers['Conv6'].db
        grads['W7'], grads['b7'] = self.layers['Conv7'].dW, self.layers['Conv7'].db
        grads['W8'], grads['b8'] = self.layers['Conv8'].dW, self.layers['Conv8'].db
        grads['W9'], grads['b9'] = self.layers['Conv9'].dW, self.layers['Conv9'].db
        grads['W10'], grads['b10'] = self.layers['Conv10'].dW, self.layers['Conv10'].db
        grads['W11'], grads['b11'] = self.layers['Conv11'].dW, self.layers['Conv11'].db
        grads['W12'], grads['b12'] = self.layers['Conv12'].dW, self.layers['Conv12'].db
        grads['W13'], grads['b13'] = self.layers['Conv13'].dW, self.layers['Conv13'].db
        grads['W14'], grads['b14'] = self.fclayers['Fuuly connected'].dW, self.fclayers['Fuuly connected'].db
        return grads

    def save_params(self, file_name="params.pkl"):
        params = {}
        for key, val in self.params.items():
            params[key] = val
        with open(file_name, 'wb') as f:
            pickle.dump(params, f)

    def load_params(self, file_name="params.pkl"):
        with open(file_name, 'rb') as f:
            params = pickle.load(f)
        for key, val in params.items():
            self.params[key] = val

        for i, key in enumerate(['Conv1', 'Affine1', 'Affine2']):
            self.layers[key].W = self.params['W' + str(i+1)]
            self.layers[key].b = self.params['b' + str(i+1)]

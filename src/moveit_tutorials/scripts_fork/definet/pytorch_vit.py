# coding: utf-8
import sys, os
sys.path.append(os.pardir)
import torch
import torch.nn as nn
import numpy as np
import imageio
import common.vis_layers as vis

from einops import repeat
from einops.layers.torch import Rearrange


class ViT(nn.Module):
    def __init__(self, image_size, patch_size, n_classes, dim, depth, n_heads, channels = 3, mlp_dim = 256):
        """ [input]
            - image_size (int) : 画像の縦の長さ（= 横の長さ）
            - patch_size (int) : パッチの縦の長さ（= 横の長さ）
            - n_classes (int) : 分類するクラスの数
            - dim (int) : 各パッチのベクトルが変換されたベクトルの長さ（参考[1] (1)式 D）
            - depth (int) : Transformer Encoder の層の深さ（参考[1] (2)式 L）
            - n_heads (int) : Multi-Head Attention の head の数
            - chahnnels (int) : 入力のチャネル数（RGBの画像なら3）
            - mlp_dim (int) : MLP の隠れ層のノード数
        """

        super().__init__()

        # Params
        n_patches = (image_size // patch_size) ** 2
        patch_dim = channels * patch_size * patch_size
        self.depth = depth

        # Layers
        self.patching = vis.Patching(patch_size = patch_size)
        self.linear_projection_of_flattened_patches = vis.LinearProjection(patch_dim = patch_dim, dim = dim)
        self.embedding = vis.Embedding(dim = dim, n_patches = n_patches)
        self.transformer_encoder = vis.TransformerEncoder(dim = dim, n_heads = n_heads, mlp_dim = mlp_dim, depth = depth)
        # self.mlp_head = vis.MLPHead(dim = dim, out_dim = n_classes)


    def trans_forward(self, img):
        """ [input]
            - img (torch.Tensor) : 画像データ
                - img.shape = torch.Size([batch_size, channels, image_height, image_width])
        """

        x = img

        # 1. パッチに分割
        # x.shape : [batch_size, channels, image_height, image_width] -> [batch_size, n_patches, channels * (patch_size ** 2)]
        x = self.patching(x)

        # 2. 各パッチをベクトルに変換
        # x.shape : [batch_size, n_patches, channels * (patch_size ** 2)] -> [batch_size, n_patches, dim]
        x = self.linear_projection_of_flattened_patches(x)

        # 3. [class] トークン付加 + 位置エンコーディング
        # x.shape : [batch_size, n_patches, dim] -> [batch_size, n_patches + 1, dim]
        x = self.embedding(x)

        # 4. Transformer Encoder
        # x.shape : No Change
        x = self.transformer_encoder(x)

        # 5. 出力の0番目のベクトルを MLP Head で処理
        # x.shape : [batch_size, n_patches + 1, dim] -> [batch_size, dim] -> [batch_size, n_classes]
        # x = x[:, 0]
        # x = self.mlp_head(x)

        return x

    def fc_forward(self, x):
        max_pool = self.gpool.forward(x)
        # max_pool = self.gpool(x)
        out = self.fclayers(max_pool)
        # print(out.shape)

        return out


    def trans_forward(self, x1, x2):
        x1 = self.trans_forward(x1)
        x2 = self.trans_forward(x2)

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
        y = self.forward(rem_x1,rem_x2)
        # print(y.shape)

        return y, self.loss_layer.forward(y, t_delta)


    def process_images(self, x):
        rem_x=[]
        for file in x:
            # 画像ファイルのパス
            image_path = os.path.join(self.folder_path, file)
            image = imageio.imread(image_path)
            rem_x.append(image)
        rem_x = np.array(rem_x).transpose(0, 3, 1, 2)
        rem_x = torch.from_numpy(rem_x).to(torch.float32)

        return rem_x



    def accuracy(self, x, t, batch_size):
        # if t.ndim != 1 : t = np.argmax(t, axis=1)

        acc = 0.0
        t = torch.from_numpy(np.array(t))
        error = x-t

        b = torch.abs(error)
        # 0.001より小さいインデックスを削除
        condition = torch.all(torch.abs(error) < 0.005, dim=1)
        acc = torch.sum(condition).item()
        # for i in range(int(x.shape[0] / batch_size)):
        #     tx = x[i*batch_size:(i+1)*batch_size]
        #     tt = t[i*batch_size:(i+1)*batch_size]
        #     y = self.predict(tx)
        #     y = np.argmax(y, axis=1)
        #     acc += np.sum(y == tt)
        # p = x.size(0)
        return acc #/ x.size(0)



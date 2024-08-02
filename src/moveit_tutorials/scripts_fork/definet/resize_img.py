import os
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from PIL import Image
from torchvision.transforms import functional as F

# def process_and_save_image(image_path, save_path):
#     # 画像を読み込む
#     image = Image.open(image_path)

#     # 画像をテンソルに変換
#     image_tensor = F.to_tensor(image).float()

#     # ガウシアンブラーを適用
#     gaussian_blur = transforms.GaussianBlur(kernel_size=(5, 5), sigma=(1.0, 1.0))
#     blurred_tensor = gaussian_blur(image_tensor)

#     # 画像をリサイズ
#     resized_tensor = F.resize(blurred_tensor, [512, 512])

#     # テンソルをPillow画像に変換
#     processed_image = F.to_pil_image(resized_tensor)

#     # 画像を保存
#     processed_image.save(save_path)

def cutting(x):
    
    # 3次元目の削除するインデックス範囲を生成
    # indices_to_remove_dim3 = list(range(0, 7)) + list(range(262, 269))

    indices_to_remove_dim3 = list(range(0, 14)) + list(range(526, 540))
    # 4次元目の削除するインデックス範囲を生成
    # indices_to_remove_dim4 = list(range(0, 112)) + list(range(367, 479))
    indices_to_remove_dim4 = list(range(0, 224)) + list(range(736, 960))

    # 3次元目と4次元目の削除しないインデックスを生成（ブールインデックスを使用）
    # dim3_keep = torch.ones(270, dtype=torch.bool)
    # dim3_keep[indices_to_remove_dim3] = False
    # dim4_keep = torch.ones(480, dtype=torch.bool)
    # dim4_keep[indices_to_remove_dim4] = False

    dim3_keep = torch.ones(540, dtype=torch.bool)
    dim3_keep[indices_to_remove_dim3] = False
    dim4_keep = torch.ones(960, dtype=torch.bool)
    dim4_keep[indices_to_remove_dim4] = False        

    # ブールインデックスを使って削除するインデックスを除外
    A_removed = x[:, :, dim3_keep, :][:, :, :, dim4_keep]

    return A_removed

def process_and_save_image(image_path, save_path):
    # 画像を読み込む
    image = Image.open(image_path)

    # 画像をテンソルに変換
    image_tensor = F.to_tensor(image).float()

    tensor_with_extra_dim = image_tensor.unsqueeze(0)

    max_pool = nn.MaxPool2d(2, 2)
    # max_pool = nn.MaxPool2d(4, 4)

    pooled_image_torch = max_pool(tensor_with_extra_dim)
    pooled_image_torch = cutting(pooled_image_torch)

    tensor_original =pooled_image_torch.squeeze(0)

    # テンソルをPillow画像に変換
    processed_image = F.to_pil_image(tensor_original)

    # 画像を保存
    processed_image.save(save_path)


# ディレクトリ内のすべての画像に対して処理を実行し、別のディレクトリに保存
def process_all_images(input_directory, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(input_directory):
        if filename.endswith(".png"):  # 画像ファイルをフィルタリング
            image_path = os.path.join(input_directory, filename)
            save_path = os.path.join(output_directory, filename)
            process_and_save_image(image_path, save_path)

# 入力と出力のディレクトリ
input_directory = './definet/bigdata'
output_directory = './definet/data'

# 画像を処理し保存
process_all_images(input_directory, output_directory)




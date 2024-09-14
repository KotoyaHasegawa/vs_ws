# import os
# import cv2

# directory = './data'
# out_directory = "./data_2value"

# if not os.path.exists(out_directory):
#     os.makedirs(out_directory)

# threshhold_value = 128

# for filename in os.listdir(directory):
#     if filename.endswith(('png')):

#         img_path = os.path.join(directory, filename)
#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

#         _, binary_img = cv2.threshold(img, threshhold_value, 255, cv2.THRESH_BINARY)

#         binary_img_path = os.path.join(out_directory, filename)
#         cv2.imwrite(binary_img_path, binary_img)


# print('2値化')



# import os
# import cv2
# import numpy as np

# # 入力ディレクトリと出力ディレクトリの設定
# input_directory = 'data'
# output_directory = './data_3value'
# threshold1 = 85  # 1つ目のしきい値
# threshold2 = 170  # 2つ目のしきい値

# # 出力ディレクトリが存在しない場合、作成する
# if not os.path.exists(output_directory):
#     os.makedirs(output_directory)

# # 入力ディレクトリ内のすべてのファイルをループ
# for filename in os.listdir(input_directory):
#     if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # 画像ファイルの拡張子をチェック
#         # 画像の読み込み
#         img_path = os.path.join(input_directory, filename)
#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

#         # 3値化
#         three_level_img = np.zeros_like(img)
#         three_level_img[img <= threshold1] = 0   # 最初の範囲のピクセルを0に設定
#         three_level_img[(img > threshold1) & (img <= threshold2)] = 127  # 中間の範囲のピクセルを127に設定
#         three_level_img[img > threshold2] = 255  # 最後の範囲のピクセルを255に設定

#         # 3値化された画像を出力ディレクトリに保存
#         three_level_img_path = os.path.join(output_directory, filename)
#         cv2.imwrite(three_level_img_path, three_level_img)

# print("すべての画像が3値化され、'output'フォルダに保存されました。")import os


# import cv2
# import numpy as np

# # 入力ディレクトリと出力ディレクトリの設定
# input_directory = 'data'
# output_directory = './data_5value'
# thresholds = [51, 102, 153, 204]  # 4つのしきい値

# # 出力ディレクトリが存在しない場合、作成する
# if not os.path.exists(output_directory):
#     os.makedirs(output_directory)

# # 入力ディレクトリ内のすべてのファイルをループ
# for filename in os.listdir(input_directory):
#     if filename.endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # 画像ファイルの拡張子をチェック
#         # 画像の読み込み
#         img_path = os.path.join(input_directory, filename)
#         img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

#         # 5値化
#         five_level_img = np.zeros_like(img)
#         five_level_img[img <= thresholds[0]] = 0   # 最初の範囲のピクセルを0に設定
#         five_level_img[(img > thresholds[0]) & (img <= thresholds[1])] = 64   # 次の範囲を64に設定
#         five_level_img[(img > thresholds[1]) & (img <= thresholds[2])] = 128  # 次の範囲を128に設定
#         five_level_img[(img > thresholds[2]) & (img <= thresholds[3])] = 192  # 次の範囲を192に設定
#         five_level_img[img > thresholds[3]] = 255  # 最後の範囲のピクセルを255に設定

#         # 5値化された画像を出力ディレクトリに保存
#         five_level_img_path = os.path.join(output_directory, filename)
#         cv2.imwrite(five_level_img_path, five_level_img)

# print("すべての画像が5値化され、'output'フォルダに保存されました。")
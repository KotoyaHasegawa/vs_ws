import os
import pandas as pd
import shutil
import csv


# 画像が保存されているフォルダ
image_folder = './data'

# CSVファイルのパス
csv_file = './rndmth_result/random_poseordel.csv'


# CSVファイルの読み込み
csv_data = pd.read_csv(csv_file, header=None)


# 画像フォルダ内の画像ファイル名のリストを取得
image_files = os.listdir(image_folder)

# 画像ファイル名を1列目に追記
# csv_data[0] = image_files
csv_data.insert(0, 'Image Files', image_files)
csv_data.to_csv("./definet/output.csv", encoding="shift_jis")
# with open(output_folder, "w") as f:
#     writer = csv.writer(f)
#     writer.writerows(data)


# # 出力先ファイルパス
# output_file = os.path.join(output_folder, 'output.csv')

# # DataFrameをCSVファイルに保存
# data.to_csv(output_file, index=False)

# print("ラベル付けが完了しました。")
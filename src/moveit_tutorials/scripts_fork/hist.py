import cv2
import numpy as np
import matplotlib.pyplot as plt

# 画像の読み込み
img = cv2.imread("data/20240430_160208_image.png", 0)
# img = cv2.imread("input_dsrim/kensyo_desired_image.png", 0)
# ヒストグラムの取得
img_hist_cv = cv2.calcHist([img], [0], None, [256], [0, 256])

# ヒストグラムの表示
plt.plot(img_hist_cv)
plt.ylim(0,100000)
plt.show()
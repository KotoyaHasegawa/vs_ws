#!/usr/bin/env python3
#coding: UTF-8

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
# import time
from time import sleep
import  numpy as np
import math
import statistics
# I_dsr_vec = np.empty((1105920, 1)) ###for UI
rsme_data = []
zncc_data = []
# nop = 1105920 ###for UI
nop = 230400 # withdraw
# nop = 72044 # input 
# nop = 115200 ###realsense
I_dsr_vec = np.empty((nop, 1))
def gen_I_dsr_vec():
    global I_dsr_vec
    I_dsr_orig = cv2.imread('./input_dsrim/kensyo_desired_image.png')
    # I_dsr_orig = cv2.imread('./data/desired_im.png')
    I_dsr_gry = cv2.cvtColor(I_dsr_orig, cv2.COLOR_BGR2GRAY)
    I_dsr_arr = np.array(I_dsr_gry, dtype='float64')
    I_dsr_vec = I_dsr_arr.reshape(-1,1)
    return I_dsr_vec 

def compute_zncc(img1, img2):
    # Ensure the images are of the same size
    if img1.shape != img2.shape:
        raise ValueError("The images must have the same dimensions")
    # Compute means
    mean1 = np.mean(img1)
    mean2 = np.mean(img2)
    # Compute zero-mean images
    img1_zero_mean = img1 - mean1
    img2_zero_mean = img2 - mean2
    # Compute numerator (sum of the product of zero-mean images)
    numerator = np.sum(img1_zero_mean * img2_zero_mean)
    # Compute denominators (product of standard deviations)
    denominator = np.sqrt(np.sum(img1_zero_mean ** 2) * np.sum(img2_zero_mean ** 2))
    # Avoid division by zero
    if denominator == 0:
        return 0
    # Compute ZNCC
    zncc = numerator / denominator
    return zncc


def process_image(msg):
    global I_dsr_vec
    global rsme_data
    global zncc_data
    bridge = CvBridge()
    orig = bridge.imgmsg_to_cv2(msg, "bgr8")
    orig = orig[ 250 : 610 ,720 : 1360 ]#withdraw
    # orig = orig[ 78 : 140 ,470 : 1632 ] #input
    gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)
    arr = np.array(gray, dtype = 'float64')
    vec = arr.reshape(-1,1)
    #画像偏差
    dI = I_dsr_vec - vec ###目標-現在
    dI2 = dI**2
    Isum = np.sum(dI2)
    rsme = math.sqrt(Isum / nop)
    # print(rsme)
    rsme_data.append(rsme)

    zncc_value = compute_zncc(I_dsr_vec , vec)
    zncc_data.append(zncc_value)
    # print(zncc_value)





    return rsme_data, zncc_data
            
def start_node():
    rospy.loginfo('rsme average node started')
    for i in range(10):
        rospy.Subscriber('/camera/color/image_raw', Image, process_image)
        # rospy.Subscriber('/camera/image_raw', Image, process_image) #for UI camera
        sleep(1)
    rsme_ave = statistics.mean(rsme_data)
    print(f"RSME: {rsme_ave}")
    rsme_var = statistics.variance(rsme_data)
    print(rsme_var)
    zncc_ave = statistics.mean(zncc_data)
    print(f"ZNCC: {zncc_ave}")
    zncc_var = statistics.variance(zncc_data)
    print(zncc_var)

if __name__ == '__main__':
    try:
        rospy.init_node('kensyo_desired_image')
        gen_I_dsr_vec()
        start_node()
    except rospy.ROSInterruptException:
        pass


# rospy.init_node('sub_one')
# image_raw = rospy.wait_for_message('/camera/color/image', Image)
# bridge = CvBridge()
# bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8')
# cv2.imwrite('./input_dsrim/kensyo_desired_image.png', bgr) ###なんかこれできない
# print('saved')



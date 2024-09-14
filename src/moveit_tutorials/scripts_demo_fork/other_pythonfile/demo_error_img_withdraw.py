#!/usr/bin/env python3
#coding: UTF-8

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# 画像撮影用
def process_image(msg):
    bridge = CvBridge()
    orig = bridge.imgmsg_to_cv2(msg, "bgr8")
    orig = orig[ 200 : 560 ,720 : 1360 ]
    gry = cv2.cvtColor(orig , cv2.COLOR_BGR2GRAY)
    # gry  = cv2.threshold(gry, 128, 255, cv2.THRESH_BINARY)#2values
    # 画像ファイルのパス
    # image_path1 = './old_data/data_new_6_input/20240119_011227_image.png'
    # image_path1 = './data/20240716_122118_image.png'
    image_path1 = './input_dsrim/kensyo_desired_image.png'
    image1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    # image1  = cv2.threshold(image1, 128, 255, cv2.THRESH_BINARY)#2values
    # 画素値の差分を計算
    difference = cv2.absdiff(image1, gry)#2values

    cv2.imshow('initial image', difference)
    if cv2.waitKey(1) & 0xff == 27:
        cv2.imwrite('./difference_image.jpg', difference)
        print ('ok')
	

 
def start_node():
	rospy.loginfo('kensyo intial image node started')
	rospy.Subscriber("/camera/color/image_raw", Image, process_image)
	# rospy.Subscriber("/camera/image_raw", Image, process_image) #for UI camerea
	rospy.spin()

if __name__ == '__main__':
	try:
		rospy.init_node('kensyo_init_image')
		start_node()
	except rospy.ROSInterruptException:
		pass
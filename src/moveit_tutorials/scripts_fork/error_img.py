#!/usr/bin/env python3
#coding: UTF-8

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

# # 画像撮影用
# def process_image(msg):
#     bridge = CvBridge()
#     orig = bridge.imgmsg_to_cv2(msg, "bgr8")
#     # orig = orig[ 250 : 610 ,720 : 1360 ] #remove
#     orig = orig[ 83 : 145 ,470 : 1632 ] #input
#     gry = cv2.cvtColor(orig , cv2.COLOR_BGR2GRAY)
#     # 画像ファイルのパス
#     # image_path1 = './old_data/data_new_6_input/20240119_011227_image.png'
#     # image_path1 = './data/20240915_175357_image.png'
#     image_path1 = './input_dsrim/kensyo_desired_image.png'
#     image1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
#     # 画素値の差分を計算
#     difference = cv2.absdiff(image1, gry)

#     cv2.imshow('initial image', difference)
#     if cv2.waitKey(1) & 0xff == 27:
#         cv2.imwrite('./difference_image.jpg', difference)
#         print ('ok')
	
# 動画撮影用
# 動画保存用の設定
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fourcc_1 = cv2.VideoWriter_fourcc(*'mp4v')
# video_writer = cv2.VideoWriter('./servo_data/difference_video.mp4', fourcc, 30.0, (1920, 1080), False)
# video_writer_1 = cv2.VideoWriter('./servo_data/outuput_video.mp4', fourcc_1, 30.0, (1920, 1080))

# #withdraw
video_writer = cv2.VideoWriter('./servo_data/difference_video.mp4', fourcc, 30.0, (640, 360), False)
video_writer_1 = cv2.VideoWriter('./servo_data/outuput_video.mp4', fourcc_1, 30.0, (640, 360))
#input
# video_writer = cv2.VideoWriter('./servo_data/difference_video.mp4', fourcc, 30.0, (1162, 62), False)
# video_writer_1 = cv2.VideoWriter('./servo_data/outuput_video.mp4', fourcc_1, 30.0, (1162, 62))
video_writer_full = cv2.VideoWriter('./servo_data/difference_full_video.mp4', fourcc, 30.0, (1920, 1080), False)
video_writer_1_full = cv2.VideoWriter('./servo_data/outuput_full_video.mp4', fourcc_1, 30.0, (1920, 1080))



def process_image(msg):
    bridge = CvBridge()
    orig_full = bridge.imgmsg_to_cv2(msg, "bgr8")
    orig = orig_full[ 250 : 610 ,720 : 1360 ]#withdrraw
    # orig = orig_full[ 100 : 162,470 : 1632 ]#input
    # orig = orig_full[ 0 : 1080 ,0 : 1920 ] #definet
    gry_full = cv2.cvtColor(orig_full, cv2.COLOR_BGR2GRAY)
    gry = cv2.cvtColor(orig , cv2.COLOR_BGR2GRAY)
    # 画像ファイルのパス
    image_path1 = './input_dsrim/kensyo_desired_image.png'
    image_path1_full = './input_dsrim/kensyo_desired_image(full).png'
    # image_path1 = './data/desired_im.png'
    image1 = cv2.imread(image_path1, cv2.IMREAD_GRAYSCALE)
    image1_full = cv2.imread(image_path1_full, cv2.IMREAD_GRAYSCALE)
	
    # 画素値の差分を計算
    difference = cv2.absdiff(image1, gry)
    difference_full = cv2.absdiff(image1_full, gry_full)
    # 差分画像を動画に書き込む
    video_writer.write(difference)
    video_writer_1.write(orig)
    video_writer_full.write(difference_full)
    video_writer_1_full.write(orig_full)


    cv2.imshow('Difference Image', difference_full)
    if cv2.waitKey(1) & 0xff == 27:
        cv2.imwrite('./difference_image.jpg', orig)
        print('Image saved and exiting...')
        video_writer.release()
        video_writer_1.release()
        video_writer_full.release()
        video_writer_1_full.release()
        rospy.signal_shutdown("ESC pressed")
 
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
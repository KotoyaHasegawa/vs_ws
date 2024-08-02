#!/usr/bin/env python3
#coding: UTF-8

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

def process_image(msg):
    bridge = CvBridge()
    orig = bridge.imgmsg_to_cv2(msg, "bgr8")
    orig = orig[ 200 : 560 ,720 : 1360 ]
    # print(orig.shape)
    # orig = bridge.imgmsg_to_cv2(msg, "mono8") ###for UI camera
    # cv2.imshow('initial image', orig)
    cv2.imwrite('./servo_data/kensyo_initial_image.png', orig)
    print("\n-----------------------------\n")
    print("\n-----------------------------\n")
    print ('init picture')
    print("\n-----------------------------\n")
    print("\n-----------------------------\n")
    rospy.signal_shutdown("Image processed and saved.")
    # cv2.waitKey(1)

    
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


# rospy.init_node('sub_one')
# image_raw = rospy.wait_for_message('/camera/color/image', Image)
# bridge = CvBridge()
# bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8')
# cv2.imwrite('./input_dsrim/kensyo_desired_image.png', bgr) ###なんかこれできない
# print('saved')

#!/usr/bin/env python3
#coding: UTF-8

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
def process_image(msg):
    bridge = CvBridge()
    orig_full = bridge.imgmsg_to_cv2(msg, "bgr8")
    # orig = orig_full [ 200 : 560 ,720 : 1360 ] #remove
    orig = orig_full [ 250 : 610 ,720 : 1360 ] #remove
    # orig = orig_full[ 83 : 145 ,470 : 1632 ] #input 
    # orig = bridge.imgmsg_to_cv2(msg, "mono8") ###for UI camera
    cv2.imshow('desired image', orig)
    # cv2.waitKey(0)
    if cv2.waitKey(1) & 0xff == 27:
        cv2.imwrite('./input_dsrim/kensyo_desired_image.png', orig)
        cv2.imwrite('./input_dsrim/kensyo_desired_image(full).png', orig_full)
        # cv2.imwrite('./practice/desired_image.png', orig)
        print ('ok')
    
def start_node():
	rospy.loginfo('kensyo desired image node started')
	rospy.Subscriber("/camera/color/image_raw", Image, process_image)
	# rospy.Subscriber("/camera/image_raw", Image, process_image) #for UI camera
	rospy.spin()

if __name__ == '__main__':
	try:
		rospy.init_node('kensyo_desired_image')
		start_node()
	except rospy.ROSInterruptException:
		pass


# rospy.init_node('sub_one')
# image_raw = rospy.wait_for_message('/camera/color/image', Image)
# bridge = CvBridge()
# bgr = bridge.imgmsg_to_cv2(image_raw, 'bgr8')
# cv2.imwrite('./input_dsrim/kensyo_desired_image.png', bgr) ###なんかこれできない
# print('saved')

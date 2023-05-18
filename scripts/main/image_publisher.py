#!/usr/bin/env python

# This python script publishes (sends) the webcam image from the robot.

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import os


def image_pub() :
    
    # initializing rosnode called 'image_pub'
	rospy.init_node('image_pub',anonymous=True)
 
 
    # opening webcam
	webcam = cv2.VideoCapture(0)
	bridge = CvBridge()
 
 
	# defining publisher on topic /webcam
	webcam_pub = rospy.Publisher('/webcam',Image,queue_size=1)
 	
	os.system('clear')
	print("Robot is now publishing it's webcam, and ready to recieve actions!")
	# while loop to send continuous frames
	while not rospy.is_shutdown() :
     
		# reading frames from webcam
		ret, frame = webcam.read()
		if not ret:
			break
		resized_frame = cv2.resize(frame,(300,225))
		flipped_frame = cv2.flip(resized_frame,0)
		# converting frame to ros image message
		msg = bridge.cv2_to_imgmsg(resized_frame, "bgr8")
  
		# publishing the above message
		webcam_pub.publish(msg)
		#rospy.loginfo("frame published.")
		
		# uncomment this section to see the sent frames
		#cv2.imshow("webcam", frame)
		#if cv2.waitKey(1) & 0xFF == ord('q'): # terminates the program if 'q' is pressed
		#	break


	# realse the webcame resource after the while loop ends
	if rospy.is_shutdown() :
		webcam.release()





if __name__ == '__main__' :
	try:
		image_pub()
	except rospy.ROSInterruptException:
		pass
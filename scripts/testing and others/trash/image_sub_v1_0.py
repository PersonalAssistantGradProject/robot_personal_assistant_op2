#!/usr/bin/env python

# This python script subscribes (receives) the webcam image from the robot.

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2



# callback function called by subscriber
def image_callback(msg) :
    
    rospy.loginfo("frame received.")
    
    # converting ros image message to frame 
    bridge = CvBridge()
    frame=bridge.imgmsg_to_cv2(msg,"bgr8")
    
    
    # flipping the received frame
    flipped_frame=cv2.flip(frame,0)
    
    
    # showing the flipped frame
    cv2.imshow("webcam", frame)
    #cv2.imwrite("op2_tmp/unknown.jpg",frame)
    cv2.waitKey(3)
    


def image_sub() :
    
    # initializing rosnode called 'image_sub'
    rospy.init_node("image_sub")
    
    # defining subscriber on topic /webcam
    rospy.Subscriber('/webcam',Image,image_callback)
    rospy.spin()



if __name__ == '__main__' :
    try :
        image_sub()
    except rospy.ROSInterruptException :
        pass
#!/usr/bin/env python

# This python script subscribes (receives) the webcam image from the robot, then applies facial detection on it, and publishes the fact that it saw a face.

import rospy
from sensor_msgs.msg import Image
from std_msgs.msg import String
from cv_bridge import CvBridge
import cv2




# loading the facial detection cascade
face_cascade = cv2.CascadeClassifier('/home/ahmad/catkin_ws/src/gptest/haarcascade_frontalface_default.xml') # you might have to change this path


pub = rospy.Publisher('/facial',String,queue_size=10)

# callback function called by subscriber
def image_callback(msg) :
    
    #rospy.loginfo("frame received.")
    
    # converting ros image message to frame 
    bridge = CvBridge()
    frame=bridge.imgmsg_to_cv2(msg,"bgr8")
    
    
    # flipping the received frame
    flipped_frame=cv2.flip(frame,0)
    
    
    # converting the flipped frame into a grayscale image
    gray_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2GRAY)
    
    
    # detecting faces from the grayscale image using the cascade
    faces = face_cascade.detectMultiScale(gray_frame, 1.1, 4)
    
    
    #drawing rectangles around the faces
    empty = True
    for (x, y, w, h) in faces:
        cv2.rectangle(flipped_frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        empty = False
        
    if not empty:
        pub.publish("face detected.")
        rospy.loginfo("face detected.")
    
    
    # showing the result
    cv2.imshow("facial detection", flipped_frame)
    cv2.waitKey(3)




def facial_detection() :
    
    # initializing rosnode called 'facial_detection'
    rospy.init_node("facial_detection")
    
    # defining subscriber on topic /webcam
    rospy.Subscriber('/webcam',Image,image_callback)
    rospy.spin()





if __name__ == '__main__' :
    try :
        facial_detection()
    except rospy.ROSInterruptException :
        pass
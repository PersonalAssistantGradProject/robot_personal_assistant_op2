#!/usr/bin/env python

# This python script subscribes (receives) the webcam image from the robot, then applies facial detection on it.

import rospy
from sensor_msgs.msg import Image 
from std_msgs.msg import Int32
from cv_bridge import CvBridge
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands




# loading the facial detection cascade
face_cascade = cv2.CascadeClassifier('/home/ahmad/catkin_ws/src/gptest/haarcascade_frontalface_default.xml') # you might have to change this path
page_num_publisher = rospy.Publisher('/robotis/action/page_num', Int32, queue_size=10)
page_num_msg = Int32()
    
    
      

# callback function called by subscriber
def image_callback(msg) :
    
    rospy.loginfo("frame received.")
    
    # converting ros image message to frame 
    bridge = CvBridge()
    frame=bridge.imgmsg_to_cv2(msg,"bgr8")
    

        
    # flipping the received frame
    flipped_frame=cv2.flip(frame,0)
    flipped_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
    results = hands.process(flipped_frame)
    flipped_frame.flags.writeable = True
    flipped_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_RGB2BGR)
    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        mp_drawing.draw_landmarks(
            flipped_frame,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    cv2.imshow('MediaPipe Hands', cv2.flip(flipped_frame, 1))
    cv2.waitKey(3)

    


def facial_detection() :
    
    # initializing rosnode called 'facial_detection'
    rospy.init_node("facial_detection")
   
    # defining subscriber on topic /webcam
    
    rospy.Subscriber('/webcam',Image,image_callback)
    rospy.spin()





if __name__ == '__main__' :
    try :
        with mp_hands.Hands(
            model_complexity=0,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
            facial_detection()
    except rospy.ROSInterruptException :
        pass
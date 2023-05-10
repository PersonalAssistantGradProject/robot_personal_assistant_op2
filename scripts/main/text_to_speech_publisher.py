#!/usr/bin/env python

import rospy
from std_msgs.msg import String
import time

def init():
    text_publisher = rospy.Publisher('/tts',String,queue_size=10)
    return text_publisher

	


def publish_text(text, text_publisher):
    
    rate = rospy.Rate(10)
    print("Robot said:", text)
    rospy.loginfo(text)
    text_publisher.publish(text)
    rate.sleep()



    while not rospy.is_shutdown():
        def callback(data):
            print("TESTTTTS")
        return 
    rospy.Subscriber('/finished_talking', String, callback)
    rospy.spin()
    #sleeptime = len(text)/12.9

    #print("Sleep time =", sleeptime)
    #time.sleep(sleeptime)
    #print("waiting finished!!!")
    #time.sleep(5)
        
    


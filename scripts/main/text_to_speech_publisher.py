#!/usr/bin/env python

import rospy
from std_msgs.msg import String


def init():
    text_publisher = rospy.Publisher('/tts',String,queue_size=10)
    return text_publisher




def publish_text(text,text_publisher):

    rate = rospy.Rate(10)
    print("Robot said:", text)
    text_publisher.publish(text)
    print("i published")
    rate.sleep()
    finished = None
    
    def callback(data):
        nonlocal finished
        finished = data.data 
    
    rospy.Subscriber('/finished_talking', String, callback)

    while not rospy.is_shutdown():
        if finished is not None:
            print("TEST5")
            return


        
    


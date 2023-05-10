#!/usr/bin/env python

import rospy
from std_msgs.msg import String


def init():
    global text_publisher
    text_publisher = rospy.Publisher('/tts',String,queue_size=10)





def publish_text(text):
    global text_publisher
    rate = rospy.Rate(10)
    print("Robot said:", text)
    text_publisher.publish(text)
    rate.sleep()
    finished = None
    
    def callback(data):
        nonlocal finished
        finished = data.data 
    
    rospy.Subscriber('/finished_talking', String, callback)

    while not rospy.is_shutdown():
        if finished is not None:
            return


        
    


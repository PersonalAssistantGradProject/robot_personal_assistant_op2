#!/usr/bin/env python

import pyttsx3
import rospy
from std_msgs.msg import String

engine = pyttsx3.init()

engine.setProperty('rate',175)



def callback(data):
    Say(data.data)


# A function to allow the robot to speech any text it's given
def Say(text):
    engine.say(text)
    engine.runAndWait()


# spin() simply keeps python from exiting until this node is stopped
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('text_sub', anonymous=True)

    rospy.Subscriber('tts', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()


# this python script will subscribe to a ROS topic that has string messages (text) and then convert it to speech.




#edit test
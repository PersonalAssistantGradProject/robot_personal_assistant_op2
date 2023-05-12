#!/usr/bin/env python




import rospy
from std_msgs.msg import Int32

def init():
    global action_publisher
    action_publisher = rospy.Publisher('/robotis/action/page_num', Int32, queue_size=10)





def publish_action(action):
    global action_publisher
    rate = rospy.Rate(10)
    print("Robot perfromed page num:", action)
    action_publisher.publish(action)
    rate.sleep()
    return

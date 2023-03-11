#!/usr/bin/env python


import rospy
from std_msgs.msg import String, Int32
import os


delay = 0
def callback(data):
    global delay

    if data.data == "face detected.":
        page = 251
    page_num_msg.data = page
    
    if delay == 0:
        page_num_publisher.publish(page_num_msg)
        rospy.loginfo("Published page_num: %s",page_num_msg.data)
        delay = 10
        rospy.sleep(2)
    else:
        delay = delay - 1
    
    
    

    
    

    
page_num_publisher = rospy.Publisher('/robotis/action/page_num', Int32, queue_size=10)
page_num_msg = Int32()



def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('facial_action', anonymous=True)

    os.system('clear')
    # inital position for the robot
    page_num_msg.data = 250
    page_num_publisher.publish(page_num_msg)
    rospy.sleep(2)
    page_num_publisher.publish(page_num_msg)
    rospy.loginfo("Published page_num: %s",page_num_msg.data)



    rospy.Subscriber('/facial', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()

#!/usr/bin/env python

# This python script publishes (sends) actions to the robot, it does that by sending a page number corresponding to the wanted action.
#
#######################
#
# page number: action
#
#   -2 : BREAK
#   -1 : STOP
# #  0 : .
#   4 : Thank you
#   15 : Sit downn
#   1 : Stand up
#   9 : Walk Ready
#   23 : Yes Go
#   27 : Oops



import rospy
from std_msgs.msg import Int32




def send_action():
    
    # initializing rosnode called 'action_sender'
    rospy.init_node('action_sender',anonymous=False)

    
    # defining publisher on topic /robotis/action/page_num
    page_num_publisher = rospy.Publisher('/robotis/action/page_num', Int32, queue_size=10)
    page_num_msg = Int32()
    
    # while loop to send continuous actions
    while not rospy.is_shutdown():
        
        page_num_msg.data = 250 # stand up action
        page_num_publisher.publish(page_num_msg)
        rospy.loginfo("Published page_num: %s",page_num_msg.data)
        rospy.sleep(7)
        
        #page_num_msg.data = 15 # sit down action
        #page_num_publisher.publish(page_num_msg)
        #rospy.loginfo("Published page_num: %s",page_num_msg.data)
        #rospy.sleep(5)
    
    
    





if __name__ == '__main__':
    try:
        send_action()
    except rospy.ROSInterruptException:
        pass
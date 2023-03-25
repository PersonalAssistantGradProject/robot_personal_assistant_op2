#!/usr/bin/env python
# license removed for brevity

# motion:
#   -2 : BREAK
#   -1 : STOP
# #  0 : .
#   4 : Thank you taken
#   15 : Sit downn taken
#   1 : Stand up taken
#   9 : Walk Ready
#   23 : Yes Go taken
#   27 : Oops taken


import rospy
from std_msgs.msg import String,Int32





def action_init () : 
    rospy.loginfo("Action initialization node started!")

    # Create a publisher to initialize the robot before starting motion.
    ini_pose_publisher = rospy.Publisher('/robotis/base/ini_pose', String, queue_size=10)
        
    # Create a publisher to enable the motion_module to be able to send motion commands.
    enable_ctrl_module_publisher = rospy.Publisher('/robotis/enable_ctrl_module', String, queue_size=10)
        
    # Create a publisher to send the index of the needed, Motion index table is defined above in this file.
    page_num_publisher = rospy.Publisher('/robotis/action/page_num', Int32, queue_size=10)


    # Defining a ROS msg of a string data type 
    ini_pose_msg = String()
    ini_pose_msg.data = "ini_pose"

    # Publishing the initialization msg to the op2_manager
    ini_pose_publisher.publish(ini_pose_msg)
    rospy.loginfo("Published ini_pose: %s",ini_pose_msg.data)
        
    # Wait for the robot to finish
    rospy.sleep(5)



    # Defining a ROS msg of a string data type 
    enable_ctrl_module_msg = String()
    enable_ctrl_module_msg.data = "action_module"

    # Publishing the initialization msg to the op2_manager
    enable_ctrl_module_publisher.publish(enable_ctrl_module_msg)
    rospy.loginfo("Published ctrl_module: %s",enable_ctrl_module_msg.data)
        
    rospy.sleep(5)
        
    

       




if __name__ == '__main__':
    try:
        rospy.init_node('action_init', anonymous=True)
        action_init()
    except rospy.ROSInterruptException:
        pass

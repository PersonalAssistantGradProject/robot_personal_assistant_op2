#!/usr/bin/env python

import rospy
from std_msgs.msg import String



words = ["darwin","darling","darlin"] + ["pain","hurt","backache"] + ["joke","funny"] + ["note"] + ["time","date"] + ["search", "google","look"]

def check_words(list_of_words):
    # subscribe to the rostopic


    rate = rospy.Rate(1) # 1Hz
    last_transcript = None
    def callback(data):
        nonlocal last_transcript
        # convert the recieved image into suitable format using CvBridge
        last_transcript = data.data



    # define subscriber on ROS topic '/webcam' with Image data 
    rospy.Subscriber('/speech_recognition_output', String, callback)

    while not rospy.is_shutdown():

        if last_transcript is not None:

            last_transcript_lower = last_transcript.lower()
            # then when you recieve a message, go and check if it has one of the words list
            for word in list_of_words:
                if word in last_transcript_lower:
                    return
        rate.sleep()

    

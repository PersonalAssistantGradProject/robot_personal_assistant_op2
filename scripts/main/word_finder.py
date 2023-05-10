#!/usr/bin/env python

import rospy
from std_msgs.msg import String



def check_words(list_of_words):
    # subscribe to the rostopic


    rate = rospy.Rate(1) # 1Hz
    transcript = None
    def callback(data):
        nonlocal transcript
        # convert the recieved image into suitable format using CvBridge
        transcript = data.data

    past_transcript = ""
    past_past_transcript = ""

    # define subscriber on ROS topic '/webcam' with Image data 
    rospy.Subscriber('/speech_recognition_output', String, callback)

    pain_type_found = ""
    pain_types = ["back","neck","leg","foot","feet","knee","arm","wrist","hand","shoulder"]
    while not rospy.is_shutdown():

        if transcript is not None:
            #print("transcript =",transcript)
            #print("past_transcript =",past_transcript)
            #print("past_past_transcript =",past_past_transcript)

            transcript_lower = transcript.lower()
            # then when you recieve a message, go and check if it has one of the words list
            for word in list_of_words:
                if word in transcript_lower:
                    if (word == "pain" or word == "hurt"):
                        print("user has pain, checking for pain type.")
                        for pain_type in pain_types:
                            if pain_type in transcript_lower + past_transcript.lower() + past_past_transcript.lower():
                                pain_type_found = pain_type
                                return word, pain_type_found
                    
                    return word, pain_type_found
            past_past_transcript = past_transcript
            past_transcript = transcript


        rate.sleep()

    

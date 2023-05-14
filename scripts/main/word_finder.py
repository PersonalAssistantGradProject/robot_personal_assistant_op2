#!/usr/bin/env python

import rospy
from std_msgs.msg import String,Int32
import text_to_speech_publisher # text_to_speech_publisher.py

def init():
    global start_publisher
    global finished_publisher
    start_publisher = rospy.Publisher('/start_recognition',String,queue_size=10)
    finished_publisher = rospy.Publisher('/finish_recognition',String,queue_size=10)



def check_words(list_of_words):

    global start_publisher
    global finished_publisher
    start_publisher.publish("start")
    rospy.loginfo("start")
    # subscribe to the rostopic

    rate = rospy.Rate(1)# 1Hz
    transcript = None
    bad_posture_time = None
    
    def callback1(data):
        nonlocal bad_posture_time
        # convert the recieved image into suitable format using CvBridge
        bad_posture_time = data.data

    if (list_of_words[0] == "darwin"):
        rospy.Subscriber('/bad_posture_time', Int32, callback1)

    count = 10

    
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
                                finished_publisher.publish("finished")
                                return word, pain_type_found
                            
                    finished_publisher.publish("finished")
                    rospy.loginfo("finished")
                    return word, pain_type_found
            past_past_transcript = past_transcript
            past_transcript = transcript

        if bad_posture_time is not None:

            if (bad_posture_time > 10):
                    print("count =",count)
                    if (count == 0):
                        advice = "I can see that you have bad posture, please fix it!"
                        text_to_speech_publisher.publish_text(advice)
                        count = (count + 1) % 20
                    else:
                        count = (count + 1) % 20

        rate.sleep()

    

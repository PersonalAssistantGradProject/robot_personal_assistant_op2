#!/usr/bin/env python

import rospy
import time
from std_msgs.msg import String,Int32
import random
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
    # subscribe to the rostopic

    rate = rospy.Rate(1)# 1Hz
    transcript = None
    

    def callback(data):
        nonlocal transcript
        # convert the recieved image into suitable format using CvBridge
        transcript = data.data

    past_transcript = ""
    past_past_transcript = ""

    # define subscriber on ROS topic '/speech_recognition_output' with tts transcript
    rospy.Subscriber('/speech_recognition_output', String, callback)

    pain_type_found = ""
    

    
    

  

    if (list_of_words[0] == "darwin"):
        

        def callback1(data):
            nonlocal bad_posture_time
            # convert the recieved image into suitable format using CvBridge
            bad_posture_time = data.data
        
        rospy.Subscriber('/bad_posture_time', Int32, callback1)


        bad_posture_time = None
        count = 10
        start_time = time.time()
        timeout = 30 # 30 seconds    

        while not rospy.is_shutdown():




            if transcript is not None:

                print("- User said:",transcript)
                transcript_lower = transcript.lower()
                for word in list_of_words:
                    if word in transcript_lower:
                        finished_publisher.publish("finished")
                        return word, pain_type_found
                transcript = None
            
            if bad_posture_time is not None:

                if (bad_posture_time > 10):
                    if (count == 0):

                        rand_text = random.randint(0, 2)
                        if (rand_text == 0):
                            advice = ("I can see your posture needs a little adjustment. Remember to ensure proper back "
                                      "support and consider changing your position regularly.")
                        elif (rand_text == 1):
                            advice = ("I couldn't help but notice your posture. It might be helpful to adjust how you sit, "
                                      "raise your shoulders, and ensure proper back support.")
                        elif (rand_text == 2):
                            advice = ("Hey, I noticed your posture needs attention. Try adjusting how you sit, raising your "
                                      "shoulders, and changing positions every 30 minutes for better alignment.")
                        text_to_speech_publisher.publish_text(advice)
                        count = (count + 1) % 20
                    else:
                        count = (count + 1) % 20

            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time >= timeout:
                word = "hey_darwin_timeout"
                return word, pain_type_found
            rate.sleep()


    elif (list_of_words[0] == "pain"):
        pain_types = ["back",
                    "neck",
                    "leg","foot","feet","knee",
                    "arm","wrist","hand",
                    "shoulder",
                    "head"]
        start_time = time.time()
        timeout = 15  # 15 seconds             
        
        while not rospy.is_shutdown():
            if transcript is not None:


                print("- User said:",transcript)
                transcript_lower = transcript.lower()
                for word in list_of_words:
                    if word in transcript_lower:
                        if (word == "pain" or word == "hurt"):
                            for pain_type in pain_types:
                                if pain_type in transcript_lower + past_transcript.lower() + past_past_transcript.lower():
                                    pain_type_found = pain_type
                                    finished_publisher.publish("finished")
                                    return word, pain_type_found
                        finished_publisher.publish("finished")
                        return word, pain_type_found
                past_past_transcript = past_transcript
                past_transcript = transcript
                transcript = None


            current_time = time.time()
            elapsed_time = current_time - start_time
            if elapsed_time >= timeout:
                word = "command_timeout"
                return word, pain_type_found
                
        
    else:

        while not rospy.is_shutdown():

            if transcript is not None:

                print("- User said:",transcript)
                transcript_lower = transcript.lower()
                for word in list_of_words:
                    if word in transcript_lower:
                        finished_publisher.publish("finished")
                        return word, pain_type_found
                transcript = None

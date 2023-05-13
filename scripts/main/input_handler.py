#!/usr/bin/env python
"""


This Python file serves as the primary module for handling user input. It 
imports and utilizes functions from other Python files to accomplish its tasks.



"""

# imported libraries
                      
import rospy
import face_recognizer # face_recognizer.py
import command_handler # command_handler.py
import text_to_speech_publisher # text_to_speech_publisher.py
import word_finder # word_finder.py
import action_sender # action_sender.py
import record_note # record_note.py
import time
import random
import datetime


# action 101 = 14s
# action 102 = 14s
# action 103 = 6s
# action 104 = 11s
# action 105 = 13s
# action 106 = 20s
# action 107 = 18s
 




if __name__ == '__main__' :

    

    # initalize ROS node 'input_handler'
    text_to_speech_publisher.init()
    action_sender.init()
    record_note.init()
    rospy.init_node('input_handler', anonymous=True)


    
    # check for authentic users
    #welcome_message = face_recognizer.security_check()
    time.sleep(5)
    action_sender.publish_action(100)
    #text_to_speech_publisher.publish_text(welcome_message)    
    #time.sleep(10)
    #exit(0)

    while True:


        print("please say \"hey darwin\"")
        list_of_words = ["darwin","darling","darlin"]
        word_finder.check_words(list_of_words)
        rand_text = random.randint(0, 4)
        if (rand_text == 0):
            text_to_speak = "Hello, how can I help you today?"
        elif (rand_text == 1):
            text_to_speak = "Hi, how can I help you?"
        elif(rand_text == 2):
            text_to_speak = "Hello, how may I assist you today?"
        elif (rand_text == 3):
            text_to_speak = "Hello, Is there anything I can do for you?"
        elif (rand_text == 4):
            text_to_speak = ""
            # get the current time
            current_time = datetime.datetime.now().time()

            # get the hour from the current time
            current_hour = current_time.hour

            # determine if it's morning, afternoon or evening
            if current_hour < 12:
                text_to_speak +="Good morning! "
            elif current_hour < 18:
                text_to_speak += "Good afternoon! "
            else:
                text_to_speak += "Good evening! "
            text_to_speak += "How may I help you today?"


        text_to_speech_publisher.publish_text(text_to_speak)  

        command_handler.command_handler()
        

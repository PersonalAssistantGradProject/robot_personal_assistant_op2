#!/usr/bin/env python
"""


This Python file serves as the primary module for handling user input. It 
imports and utilizes functions from other Python files to accomplish its tasks.



"""

# imported libraries
                      
import rospy
import random
import datetime
import os
import time
import face_recognizer # face_recognizer.py
import command_handler # command_handler.py
import text_to_speech_publisher # text_to_speech_publisher.py
import word_finder # word_finder.py
import action_sender # action_sender.py
import record_note # record_note.py

def initialize_system():

    # initalize for various functions
    text_to_speech_publisher.init()
    action_sender.init()
    record_note.init()
    word_finder.init()
    face_recognizer.init()

    # initalize ROS node 'input_handler'
    rospy.init_node('input_handler', anonymous=True)
    os.system('clear')


if __name__ == '__main__' :

    

    # initalize the system
    initialize_system()

    

    while True:
        bypass = False
        if (not bypass):
            # check for authentic users
            face_recognizer.security_check()
        else:
            time.sleep(3)
            action_sender.publish_action(100)
    
    
    
    
        while True:



            print("////////////////////////////////////////////////")
            print("----- Waiting for user to say \"hey darwin\" -----")

            list_of_words = ["darwin", "darling", "darlin", "godwin", "dad win", "daddy", "edwin", "bedouin","dad when"]
            found_word, pain_type = word_finder.check_words(list_of_words)
            if (found_word == "hey_darwin_timeout"):
                print("- User input timeout! Going back to authentication step.")
                break

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
            
            print("\n")

        # make darwin sit down but face you to detect your face
        action_sender.publish_action(108)
        time.sleep(3)
        

        

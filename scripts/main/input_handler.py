#!/usr/bin/env python
"""


This Python file serves as the primary module for handling user input. It 
imports and utilizes functions from other Python files to accomplish its tasks.



"""

# imported libraries
import speech_recognition as sr                        
import rospy                          
from std_msgs.msg import String       
import time
import os
import threading
import face_recognizer # face_recognizer.py
import command_handler # command_handler.py
import text_to_speech_publisher # text_to_speech_publisher.py
import word_finder # word_finder.py







if __name__ == '__main__' :

    
    print("started")
    # initalize ROS node 'input_handler'
    text_publisher = text_to_speech_publisher.init()
    rospy.init_node('input_handler', anonymous=True)
    
    str5 = "Hello my name is Amo! How can I help you?"
    
    text_to_speech_publisher.publish_text(str5, text_publisher)

    print("i finished talking")

    omar_image,mohammad_image,ahmad_image = face_recognizer.load_faces()
    print("faces have been loaded!")
    welcome_string = "Hello"
    number_of_auth_users = 0
    while True:
        auth_results = face_recognizer.recongize_faces(omar_image, mohammad_image, ahmad_image)

        if (auth_results[0]):
            # say hello Omar & welcome back
            welcome_string+= " Omar"
            number_of_auth_users += 1 

        if (auth_results[1]):
            # say hello Mohammad & welcome back
            if(number_of_auth_users > 0):
                welcome_string+= " and"
            welcome_string+= " Mohammad"
            number_of_auth_users +=1

        if (auth_results[2]):
            # say hello Ahmad & welcome back
            if(number_of_auth_users > 0):
                welcome_string+= " and"
            welcome_string+= " Ahmad"
            number_of_auth_users +=1


        if (number_of_auth_users > 0):
            welcome_string+= "."
            break
        else:
            print("Not authentic user. . . ")



    list_of_words = ["darwin","darling","darlin"]
    count = 0
    while True:
        word_finder.check_words(list_of_words)
        print("user said darwin",count)
        count += 1
        
    text_to_speech_publisher.publish_text(welcome_string, text_publisher)
    print(welcome_string)
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
    
    
    str5 = "Certainly, I can provide you with a long paragraph on a topic of your choice. Is there a particular subject you would like me to discuss?"
    
    text_publisher = text_to_speech_publisher.init()
    rospy.init_node('input_handler', anonymous=True)
    text_to_speech_publisher.publish_text(str5,text_publisher)

    print("i finished talking")

    welcome_message = face_recognizer.security_check()
    
    

    list_of_words = ["darwin","darling","darlin"]
    count = 0
    while True:
        word_finder.check_words(list_of_words)
        print("user said darwin",count)
        count += 1
        
    text_to_speech_publisher.publish_text(welcome_string, text_publisher)
    print(welcome_string)
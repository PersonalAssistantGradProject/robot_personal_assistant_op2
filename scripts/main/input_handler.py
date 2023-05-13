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







if __name__ == '__main__' :

    

    # initalize ROS node 'input_handler'
    text_to_speech_publisher.init()
    action_sender.init()
    record_note.init()
    rospy.init_node('input_handler', anonymous=True)


    
    # check for authentic users
    #welcome_message = face_recognizer.security_check()
    
    action_sender.publish_action(100)
    #text_to_speech_publisher.publish_text(welcome_message)    


    while True:
        print("please say \"hey darwin\"")
        list_of_words = ["darwin","darling","darlin"]
        word_finder.check_words(list_of_words)

        message = "Hello, how can i help you today?"
        text_to_speech_publisher.publish_text(message)  

        command_handler.command_handler()
        

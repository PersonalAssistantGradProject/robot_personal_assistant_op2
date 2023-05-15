#!/usr/bin/env python


"""


This Python file creates a ROS node called "text_to_speech" which subscribes
to the "/tts" ROS topic.

Whenever a string message is received on this topic, the node utilizes gTTS
to convert the text to speech.

The resulting audio is then played through the robot's speakers, giving the
impression that the robot is speaking the text.


"""


# imported libraries
from gtts import gTTS
import rospy
from std_msgs.msg import String
import os
import base64
import tempfile
import pygame



# callback function called when string data is recieved on '/tts'
def callback(data):
    # Decode the base64-encoded audio data
    audio_data = base64.b64decode(data.data)
    
    # Save the audio data to a temporary file
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(audio_data)
    temp_file.close()
    
    # Play the audio file
    pygame.mixer.music.load(temp_file.name)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pass




    global finished_talking_publisher
    finished_talking_publisher.publish("finished!")
    rospy.loginfo("finished!")
    
    # Remove the temporary file
    os.remove(temp_file.name)




# The "speak" function accepts a string parameter named 'text'.
# 
# It uses the gTTS library to convert the input text into speech.
# 
# The generated audio is saved as an mp3 file, and then played through the robot's speaker.


 


# spin() simply keeps python from exiting until this node is stopped
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    pygame.init()
    rospy.init_node('text_to_speech', anonymous=True)
    rospy.Subscriber('/tts', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    finished_talking_publisher = rospy.Publisher('/finished_talking', String, queue_size=10)
    listener()
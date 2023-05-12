#!/usr/bin/env python


"""


This Python file creates a ROS node called "text_to_speech" which subscribes
to the "/text_to_speech" ROS topic.

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
import pygame



# callback function called when string data is recieved on '/tts'
def callback(data):
    rospy.loginfo(data.data)
    speak(data.data)



# The "speak" function accepts a string parameter named 'text'.
# 
# It uses the gTTS library to convert the input text into speech.
# 
# The generated audio is saved as an mp3 file, and then played through the robot's speaker.
#

def speak(text):

    
    # create a gTTS object and specify language and voice
    # this will generate the speech we want the robot to speak
    print("generating audio")
    tts = gTTS(text=text, lang='en', tld='com', slow=False) 


    mp3_file_path = os.path.expanduser("~/op2_tmp/speech.mp3")
    # save the generated speech to an mp3 file
    print("saving mp3 file")
    tts.save(mp3_file_path)
    
    # play the mp3 file using playsound
    print("loading mp3 file")
    pygame.init()
    pygame.mixer.music.load(mp3_file_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_pos() > -1:
        pygame.time.Clock.tick(10)
    pygame.quit()
    global finished_talking_publisher
    finished_talking_publisher.publish("finished!")
    rospy.loginfo("finished!")

 


# spin() simply keeps python from exiting until this node is stopped
def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('text_to_speech', anonymous=True)
    rospy.Subscriber('/tts', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()


if __name__ == '__main__':
    finished_talking_publisher = rospy.Publisher('/finished_talking', String, queue_size=10)
    listener()
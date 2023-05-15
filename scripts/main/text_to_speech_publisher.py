#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from gtts import gTTS
import os
import base64
import tempfile


def init():
    global text_publisher
    text_publisher = rospy.Publisher('/tts',String,queue_size=10)





def publish_text(text_to_speak,wait = True):
    global text_publisher
    rate = rospy.Rate(10)
    tts = gTTS(text=text_to_speak, lang='en', tld='com', slow=False)

    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file_path = temp_file.name
    tts.save(temp_file_path)
    temp_file.close()

    # Read the audio file content as bytes
    with open(temp_file_path, 'rb') as f:
        audio_bytes = f.read()

    # Encode the audio data as base64
    audio_data = base64.b64encode(audio_bytes).decode()

    # Publish the audio data
    text_publisher.publish(audio_data)
    print("Robot said:", text_to_speak)
    # Remove the temporary audio file
    os.remove(temp_file_path)

    rate.sleep()
    finished = None
    
    def callback(data):
        nonlocal finished
        finished = data.data 
    
    rospy.Subscriber('/finished_talking', String, callback)

    while not rospy.is_shutdown():
        if (finished is not None or not wait):
            return


        
    


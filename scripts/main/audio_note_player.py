#!/usr/bin/env python

import rospy
from std_msgs.msg import String
from playsound import playsound
import os

def audio_callback(data):
    audio_data_str = data.data
    # Encode the audio data as bytes
    audio_data = audio_data_str.encode('latin-1')

    audio_file_path = os.path.expanduser("~/op2_tmp/recordings/received_note_audio.wav")

    with open(audio_file_path, 'wb') as f:
        f.write(audio_data)

    # Play the audio using the playsound library
    playsound(audio_file_path)
    global finished_talking_publisher
    finished_talking_publisher.publish("finished!")
    rospy.loginfo("finished!")


def audio_subscriber():
    rospy.init_node('audio_note_subscriber', anonymous=True)
    rospy.Subscriber('/audio_topic', String, audio_callback)
    rospy.spin()

if __name__ == '__main__':
    try:
        finished_talking_publisher = rospy.Publisher('/finished_talking', String, queue_size=10)
        audio_subscriber()
    except rospy.ROSInterruptException:
        pass

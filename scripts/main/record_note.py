#!/usr/bin/env python
import socket
import time
import audioop
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import os
import rospy
from std_msgs.msg import String
import text_to_speech_publisher # text_to_speech_publisher.py
import word_finder # word_finder.py
import random




def init():

    global audio_publisher
    audio_publisher = rospy.Publisher('/audio_topic', String, queue_size=10)
    global record_count
    record_count = 0
    directory = os.path.expanduser(f"~/op2_tmp/recordings")
    # get a list of all the files in the directory
    file_list = os.listdir(directory)
    for filename in file_list:
        file_path = os.path.join(directory, filename)
        os.remove(file_path)
    



def record():

    # Set up a socket to receive audio data
    HOST = ''  # Listen on all available interfaces
    PORT = 5000  # Use a free port number
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    data_buffer = b''
    threshold = 6000
    count = -50

    
    text_to_speak = "I'm ready to record your voice, please start talking!"
    text_to_speech_publisher.publish_text(text_to_speak, wait = False)
    time.sleep(3)
    note_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    note_socket.bind((HOST, PORT))
    note_socket.listen()
    #print(f"Listening for audio data on {HOST}:{PORT}...")
    conn, addr = note_socket.accept()
    #print(f"Connected by {addr}")

    print("\nStarted recording user's audio")
    while True:
        data = conn.recv(CHUNK)
        if not data:
            break
        data_buffer += data

        # check if user is quite

        sample = audioop.tomono(data, 2, 1, 0)  # convert stereo to mono
        energy = audioop.rms(sample, 2)  # calculate RMS energy
        #rms = np.sqrt(np.mean(np.square(np.frombuffer(data, dtype=np.int16))))
        #threshold = max(threshold * DECAY_RATE, 6 * rms)
        print(f"Energy: {energy}", end="\r")
        if energy < threshold:
            count +=1
        elif(count > 0):
            count -=10

        if (count > 250):
            break

    print("Finished recording user's audio\n")

    text_num = random.randint(0, 2)
    if (text_num == 0):
        text_to_speak = "Done! I am saving your audio at the moment!"
    elif (text_num == 1):
        text_to_speak = "All set! Saving your audio now."
    elif (text_num == 2):
        text_to_speak = "Great! I have saved your audio recording. Let me know when you want to hear it!"

    text_to_speech_publisher.publish_text(text_to_speak)


    # convert the audio data to an AudioSegment object
    audio_data = np.frombuffer(data_buffer, dtype=np.int16)
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=RATE, sample_width=audio_data.itemsize,
                                channels=CHANNELS)

 
    global record_count
    record_count +=1
    filename = os.path.expanduser(f"~/op2_tmp/recordings/recording{record_count}.mp3")
    audio_segment.export(filename, format="mp3")
    return
 
    


def playback():


    global record_count

    if (record_count == 0):
        text_num = random.randint(0, 2)
        if (text_num == 0):
            text_to_speak = "You don't have any records to playback."
        elif (text_num == 1):
            text_to_speak = "Unfortunately, there are no records for playback."
        elif (text_num == 2):
            text_to_speak = "There are currently no records that can be played back."
        text_to_speech_publisher.publish_text(text_to_speak)
        return
    

    text_num = random.randint(0, 2)
    if (text_num == 0):
        text_to_speak = f"Which recording would you like me to play? You have {record_count} recordings saved."
    elif (text_num == 1):
        text_to_speak = f"You have {record_count} recordings that I can play. Which one do you want to hear?"
    elif (text_num == 2):
        text_to_speak = f"Let me know which of your {record_count} saved recordings you would like me to play."
    text_to_speech_publisher.publish_text(text_to_speak)

    list_of_words = ["one","1","two","2","three","3","four","4","five","5","six","6","seven","7","eight","8","nine","9"]
    list_of_words = list_of_words[:2 * record_count]
    print("\nWaiting for user to say one of those:",list_of_words)
    found_word, pain_type = word_finder.check_words(list_of_words)
    print(f"recording to playback: {found_word}\n")
    
    if (found_word == "one" or found_word == "1"):
        record_num = 1
    elif (found_word == "two" or found_word == "2"):
        record_num = 2
    elif (found_word == "three" or found_word == "3"):
        record_num = 3
    elif (found_word == "four" or found_word == "4"):
        record_num = 4
    elif (found_word == "five" or found_word == "5"):
        record_num = 5
    elif (found_word == "six" or found_word == "6"):
        record_num = 6
    elif (found_word == "seven" or found_word == "7"):
        record_num = 7
    elif (found_word == "eight" or found_word == "8"):
        record_num = 8
    elif (found_word == "nine" or found_word == "9"):
        record_num = 9
    

    filename = os.path.expanduser(f"~/op2_tmp/recordings/recording{record_num}.mp3")
    text_num = random.randint(0, 2)
    if(text_num == 0):
        text_to_speak = f"Playing recording {record_num} as requested."
    elif(text_num == 1):
        text_to_speak = f"I will play recording {record_num} now!"
    elif(text_num == 2):
        text_to_speak = f"Your selected recording, number {record_num}, will play now."
    text_to_speech_publisher.publish_text(text_to_speak)

    global audio_publisher
    rate = rospy.Rate(10)
    with open(filename, 'rb') as f:
        audio_data = f.read()

    audio_data_str = audio_data.decode('latin-1')  # Decode the audio data to a string
    audio_publisher.publish(audio_data_str)
    rate.sleep()
    finished = None
    
    def callback(data):
        nonlocal finished
        finished = data.data 
    
    rospy.Subscriber('/finished_talking', String, callback)

    while not rospy.is_shutdown():
        if (finished is not None):
            return



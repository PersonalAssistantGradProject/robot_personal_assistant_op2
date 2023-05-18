#!/usr/bin/env python
import random
import socket
import audioop
import numpy as np
from pydub import AudioSegment
import os
import speech_recognition as sr
import wikipedia
import text_to_speech_publisher # text_to_speech_publisher.py
import time

def handle_wikipedia():
    time.sleep(1)

    HOST = ''  # Listen on all available interfaces
    PORT = 5000  # Use a free port number
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    data_buffer = b''

    threshold = 6000
    count = -50
    note_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    note_socket.bind((HOST, PORT))
    
    text_to_speak = "Tell me the specific topic that you would like me to address?!"
    text_to_speech_publisher.publish_text(text_to_speak,wait =False)

    time.sleep(3)
    note_socket.listen()
    print(f"Listening for audio data on {HOST}:{PORT}...")
    conn, addr = note_socket.accept()
    print(f"Connected by {addr}")
    #time.sleep(1)
    print("started recording")
    while True:
        data = conn.recv(CHUNK)
        if not data:
            break
        data_buffer += data

        # check if user is quite

        sample = audioop.tomono(data, 2, 1, 0)  # convert stereo to mono
        energy = audioop.rms(sample, 2)  # calculate RMS energy
        #print(energy)
        #rms = np.sqrt(np.mean(np.square(np.frombuffer(data, dtype=np.int16))))
        #threshold = max(threshold * DECAY_RATE, 6 * rms)
        
        if energy < threshold:
            count +=1
        elif(count > 0):
            count -=10

        if (count > 250):
            print("user has been quite for a while . exiting")
            break

    text_num = random.randint(0, 2)
    if (text_num == 0):
        text_to_speak = "Your topic is being researched at the moment. Please bear with me while I gather the necessary information."
    elif (text_num == 1):
        text_to_speak = "I'm in the process of searching for information related to the topic you provided. I'll respond as soon as I have a comprehensive answer."
    elif (text_num == 2):
        text_to_speak = "Your topic has been received and I'm in the process of researching and analyzing it. I'll provide you with a response as soon as possible."
        
    text_to_speech_publisher.publish_text(text_to_speak)
        
    # convert the audio data to an AudioSegment object
    audio_data = np.frombuffer(data_buffer, dtype=np.int16)
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=RATE, sample_width=audio_data.itemsize, channels=CHANNELS)
    filename = os.path.expanduser("~/op2_tmp/recordings/topic_recording.mp3")
    audio_segment.export(filename, format="mp3")


    sound = AudioSegment.from_mp3(filename)
    filename = os.path.expanduser("~/op2_tmp/recordings/topic_recording.wav")
    sound.export(filename, format="wav")

    # Initialize a recognizer instance
    r = sr.Recognizer()

    # Load the audio file
    audio_file = sr.AudioFile(filename)
    with audio_file as source:
        audio = r.record(source)

    # Transcribe the audio using Google's Speech Recognition API
    
    try:
        topic = r.recognize_google(audio)
    except:
        topic = ""
    
    print("topic = ", topic)
    answer = "Here's a summery about the topic you provided: "

    try:
        answer += wikipedia.summary(topic, sentences = 2)
    except:
        text_num = random.randint(0, 1)
        if (text_num == 0):
            answer = "My apologies, but I was unable to find an answer to your question."
        elif (text_num == 1):
            answer = "Unfortunately, I was unable to locate an answer to your question."
    text_to_speech_publisher.publish_text(answer)


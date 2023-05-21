#!/usr/bin/env python
import random
import socket
import audioop
import numpy as np
from pydub import AudioSegment
import os
import speech_recognition as sr
import wolframalpha
import time
import sys
import text_to_speech_publisher # text_to_speech_publisher.py


def handle_search():


    HOST = ''  # Listen on all available interfaces
    PORT = 5000  # Use a free port number
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    data_buffer = b''

    threshold = 6000
    count = -50 
    

    text_to_speak = "What would you like me to search for?"
    text_to_speech_publisher.publish_text(text_to_speak, wait = False)



    
    

    time.sleep(1.5)
    note_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    note_socket.bind((HOST, PORT))
    note_socket.listen()
    conn, addr = note_socket.accept()
    while True:
        data = conn.recv(CHUNK)
        if not data:
            break
        data_buffer += data

        # check if user is quite

        sample = audioop.tomono(data, 2, 1, 0)  # convert stereo to mono
        energy = audioop.rms(sample, 2)  # calculate RMS energy

        print(f"Energy: {energy}", end="\r")

        if energy < threshold:
            count +=1
        elif(count > 0):
            count -=10

        if (count > 250):
            break

    text_num = random.randint(0, 2)
    if (text_num == 0):
        text_to_speak = "Your question is being processed. Please wait a moment."
    elif (text_num == 1):
        text_to_speak = "I'm currently working on your question and will respond as soon as possible."
    elif (text_num == 2):
        text_to_speak = "Your question has been received and I am working on it now."
        
    text_to_speech_publisher.publish_text(text_to_speak)
        
    # convert the audio data to an AudioSegment object
    audio_data = np.frombuffer(data_buffer, dtype=np.int16)
    audio_segment = AudioSegment(audio_data.tobytes(), frame_rate=RATE, sample_width=audio_data.itemsize, channels=CHANNELS)
    filename = os.path.expanduser(f"~/op2_tmp/recordings/question_recording.mp3")
    audio_segment.export(filename, format="mp3")

    sound = AudioSegment.from_mp3(filename)
    filename = os.path.expanduser("~/op2_tmp/recordings/question_recording.wav")
    sound.export(filename, format="wav")
    # Initialize a recognizer instance
    r = sr.Recognizer()

    # Load the audio file
    audio_file = sr.AudioFile(filename)
    with audio_file as source:
        audio = r.record(source)

    # Transcribe the audio using Google's Speech Recognition API
    try:
        sys.stdout = open(os.devnull, 'w')
        question = r.recognize_google(audio)
        sys.stdout = sys.__stdout__
    except:
        question = ""
        sys.stdout = sys.__stdout__
    print(f"\nquestion = {question}\n")

    # App id obtained by the above steps
    app_id = "7KHGE6-RTHTWQXY7G"
            
    # Instance of wolf ram alpha 
    # client class
    client = wolframalpha.Client(app_id)

    # Stores the response from 
    # wolf ram alpha
    answer = "The answer for your question is: "
    try:
        result = client.query(question)
        answer += next(result.results).text



    except:
        text_num = random.randint(0, 1)
        if (text_num == 0):
            answer = "My apologies, but I was unable to find an answer to your question."
        elif (text_num == 1):
            answer = "Unfortunately, I was unable to locate an answer to your question."
    text_to_speech_publisher.publish_text(answer)




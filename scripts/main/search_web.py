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
import text_to_speech_publisher # text_to_speech_publisher.py


def handle_search():

    text_num = random.randint(0,1)
    if(text_num == 0):
        text_to_speak = "What would you like to ask?"
    elif(text_num == 1):
        text_to_speak = "Please speak out your question!"
    text_to_speech_publisher.publish_text(text_to_speak)



    HOST = ''  # Listen on all available interfaces
    PORT = 5001  # Use a free port number
    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    data_buffer = b''

    threshold = 1000
    count = 0 
    note_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    note_socket.bind((HOST, PORT))
    note_socket.listen()
    print(f"Listening for audio data on {HOST}:{PORT}...")
    conn, addr = note_socket.accept()
    print(f"Connected by {addr}")
    time.sleep(1)
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
        
        if energy < threshold:
            count +=1
        elif(count > 0):
            count -=10

        if (count > 110):
            print("user has been quite for a while . exiting")
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
        question = r.recognize_google(audio)
    except:
        question = ""
    print("question = ", question)

    # App id obtained by the above steps
    app_id = "7KHGE6-RTHTWQXY7G"
            
    # Instance of wolf ram alpha 
    # client class
    client = wolframalpha.Client(app_id)

    # Stores the response from 
    # wolf ram alpha
    result = client.query(question)

    # Includes only text from the response
    try:
        answer = next(result.results).text
        
    except:
        text_num = random.randint(0, 1)
        if (text_num == 0):
            answer = "My apologies, but I was unable to find an answer to your question."
        elif (text_num == 1):
            answer = "Unfortunately, I was unable to locate an answer to your question."
    print("answer = ", answer)
    text_to_speech_publisher.publish_text(answer)



    return


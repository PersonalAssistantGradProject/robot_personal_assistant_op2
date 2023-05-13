#!/usr/bin/env python
import socket
import time
import audioop
import numpy as np
from pydub import AudioSegment
from pydub.playback import play
import os
import text_to_speech_publisher # text_to_speech_publisher.py
import word_finder # word_finder.py





def init():


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
    PORT = 5001  # Use a free port number
    

    # say "please speak out your note" or "please start talking"
    text_to_speak = "please start talking"
    text_to_speech_publisher.publish_text(text_to_speak)

    CHANNELS = 1
    RATE = 44100
    CHUNK = 1024
    data_buffer = b''
    INITIAL_THRESHOLD = 0
    DECAY_RATE = 0.96
    threshold = INITIAL_THRESHOLD
    count = 0 
    note_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    

    note_socket.bind((HOST, PORT))
    note_socket.listen()
    print(f"Listening for audio data on {HOST}:{PORT}...")
    conn, addr = note_socket.accept()
    print(f"Connected by {addr}")

    #time.sleep(1)
    while True:
        data = conn.recv(CHUNK)
        if not data:
            break
        data_buffer += data

        # check if user is quite

        sample = audioop.tomono(data, 2, 1, 0)  # convert stereo to mono
        energy = audioop.rms(sample, 2)  # calculate RMS energy
        rms = np.sqrt(np.mean(np.square(np.frombuffer(data, dtype=np.int16))))
        threshold = max(threshold * DECAY_RATE, 6 * rms)
        if energy < threshold:
            count +=1
        elif(count > 0):
            count -=10

        if (count > 110):
            print("user has been quite for a while . exiting")
            break

    


    # say "i will save your record right now"
    text_to_speak = "Done! I am saving your audio at the moment!"
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
        text_to_speak = "You don't have any records to playback."
        text_to_speech_publisher.publish_text(text_to_speak)
        return
    
    text_to_speak = f"Which record you want me to play? you have {record_count} records saved."
    text_to_speech_publisher.publish_text(text_to_speak)
    time.sleep(1)

    list_of_words = ["one","1","two","2","three","3","four","4","five","5","six","6","seven","7","eight","8","nine","9"]
    list_of_words = list_of_words[:2* record_count]
    print(list_of_words)
    found_word, pain_type = word_finder.check_words(list_of_words)
    print("found_word =", found_word)
    
    if (found_word == "one" or found_word == "1"):
        record_num = 1
    if (found_word == "two" or found_word == "2"):
        record_num = 2
    if (found_word == "three" or found_word == "3"):
        record_num = 3
    if (found_word == "four" or found_word == "4"):
        record_num = 4
    if (found_word == "five" or found_word == "5"):
        record_num = 5
    if (found_word == "six" or found_word == "6"):
        record_num = 6
    if (found_word == "seven" or found_word == "7"):
        record_num = 7
    if (found_word == "eight" or found_word == "8"):
        record_num = 8
    if (found_word == "nine" or found_word == "9"):
        record_num = 9
    

    filename = os.path.expanduser(f"~/op2_tmp/recordings/recording{record_num}.mp3")
    text_to_speak = f"I will play recording {record_num} now."
    text_to_speech_publisher.publish_text(text_to_speak)

    audio = AudioSegment.from_file(filename, format="mp3")
    play(audio)
    return



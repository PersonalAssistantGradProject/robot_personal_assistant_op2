#!/usr/bin/env python

import socket
import pyaudio
import wave
import os
import rospy
from std_msgs.msg import Int32

# define audio settings
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 3


folder = 'audio_test' # Replace with the path to the folder you want to delete files from

# Loop through all the files in the folder and delete them
for filename in os.listdir(folder):
    file_path = os.path.join(folder, filename)
    try:
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
    except Exception as e:
        print(f"Error deleting file: {file_path}. Reason: {e}")


rospy.init_node('audio_reciever',anonymous=False)
seg_num_publisher = rospy.Publisher('/seg_num', Int32, queue_size=1)
# initialize PyAudio
audio = pyaudio.PyAudio()

# create socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set host and port of the receiver
host = '' # leave blank to accept connections from any IP address
port = 5000 # replace with the same port number used in the sender code

# bind the socket to the host and port
s.bind((host, port))

# start listening for incoming connections
s.listen(1)
print("Waiting for connection...")

# accept the incoming connection
conn, addr = s.accept()
print("Connected to", addr)

# open audio stream to record received audio
stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)
frames = []

seg_num = 0
while True:
    # receive microphone audio from the sender and record it for 3 seconds
    
    frames.clear()
    # if this is not the first segment, add the last second from the previous segment to the current frames
    if seg_num > 0:
        frames[:len(prev_frames)] = prev_frames
    
    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS * 2)):
        data = conn.recv(CHUNK)
        frames.append(data)
        # playback the audio
        #stream.write(data)

    # increment segment counter
    
    # save the recorded audio to a .wav file
    WAVE_OUTPUT_FILENAME = "audio_test/recorded_audio" + str(seg_num) +".wav"

    print(WAVE_OUTPUT_FILENAME)
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


    # publish file number

    seg_num_publisher.publish(seg_num)
    
    # save the last second of the current segment for the next segment
    prev_frames = frames[-int(RATE / CHUNK):]
    seg_num += 1
    if (seg_num > 4):
        seg_num = 0

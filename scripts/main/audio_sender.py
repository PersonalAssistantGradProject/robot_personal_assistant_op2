#!/usr/bin/env python
import pyaudio
import socket

# set the audio parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024

# initialize PyAudio
audio = pyaudio.PyAudio()

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get the IP address of the receiving PC
host = "127.0.0.2" # change to the IP address of the receiving PC
port = 5000

# connect to the receiving PC
print(f"waiting to connect to {host}")
while True:
    try:
        s.connect((host, port))
        
    except:
        continue
    break

print(f"Connected by {host}")



# start recording audio from the microphone
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# send the audio data over the network
while True:
    data = stream.read(CHUNK)
    s.sendall(data)

# stop recording and close the connection
stream.stop_stream()
stream.close()
audio.terminate()
s.close()

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
socket1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# get the IP address of the receiving PC
HOST = "192.168.1.20" # change to the IP address of the receiving PC
PORT = 5000


# connect to the receiving PC
print(f"waiting to connect to {HOST}")
while True:
    try:
        socket1.connect((HOST, PORT))
        
    except:
        continue
    break

print(f"conneted to {HOST}:{PORT}...")

# start recording audio from the microphone
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# send the audio data over the network
while True:
    data = stream.read(CHUNK)
    socket1.sendall(data)


# stop recording and close the connection
stream.stop_stream()
stream.close()
audio.terminate()
s.close()

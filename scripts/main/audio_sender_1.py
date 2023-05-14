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



# get the IP address of the receiving PC
HOST = "192.168.1.20" # change to the IP address of the receiving PC
PORT = 5001





while True:
    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # start recording audio from the microphone
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    # connect to the receiving PC
    print(f"waiting to connect to {HOST}")
    while True:
        try:
            audio_socket.connect((HOST, PORT))
                
        except:
            continue
        break

    print(f"conneted to {HOST}:{PORT}...")

    

    # send the audio data over the network
    while True:
        data = stream.read(CHUNK)
        try:
            audio_socket.sendall(data)
        except:
            break

    # cleanup
    stream.stop_stream()
    stream.close()
    #audio.terminate()
    audio_socket.close()


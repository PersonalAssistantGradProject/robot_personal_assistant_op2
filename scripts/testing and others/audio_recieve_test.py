#!/usr/bin/env python
import socket
import speech_recognition as sr
import numpy as np

HOST = ''  # listen on all network interfaces
PORT = 5000  # arbitrary non-privileged port
CHUNK = 1024  # audio chunk size
FORMAT = 'pcm'  # audio format
CHANNELS = 1  # number of audio channels
RATE = 16000  # sampling rate in Hertz
RECORD_SECONDS = 3  # length of audio recording in seconds
ENERGY_THRESHOLD = 2000  # minimum energy level to start recording

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# bind the socket to a public host, and a port
server_socket.bind((HOST, PORT))

# become a server socket
server_socket.listen(1)

# create a recognizer object
r = sr.Recognizer()

print(f"Server listening on port {PORT}")

buffer = []  # buffer to accumulate audio data
recording = False  # flag to indicate if we are currently recording

while True:
    # wait for a client to connect
    conn, addr = server_socket.accept()
    print(f"Client connected from {addr}")

    while True:
        # receive audio data from the client
        data = conn.recv(CHUNK)

        # break the loop if no more data is received
        if not data:
            break

        # create an AudioData object from the received data
        audio_data = sr.AudioData(data, RATE, CHANNELS)
        print(audio_data.sample_width)
        if audio_data.frame_data.startswith(b'\xff\xfe'):
            byteorder = 'little'
        else:
            byteorder = 'big'


        # check if the energy level is above the threshold to start recording
        audio_samples = np.frombuffer(audio_data.frame_data, dtype=np.int16)
        if len(audio_samples) > 0:
            energy = np.sqrt(np.mean(np.square(audio_samples))) * CHANNELS
        else:
            energy = 0


        if energy > ENERGY_THRESHOLD and not recording:
            print("Recording started")
            recording = True
            start_time = sr.AudioData.get_current_time()
        
        # check if we are already recording
        if recording:
            buffer.append(data)
            duration = sr.AudioData.get_current_time() - start_time
            
            # stop recording if the user is quiet for too long
            if duration > sr.AudioData.METADATA_READ_TIMEOUT:
                print("Recording stopped")
                recording = False
                
                # combine the audio data in the buffer into a single AudioData object
                audio_data = sr.AudioData(b"".join(buffer), RATE, CHANNELS)
                buffer = []
                
                # perform speech recognition
                try:
                    text = r.recognize_google(audio_data)
                    print(f"Recognized text: {text}")
                except sr.UnknownValueError:
                    print("Speech recognition could not understand audio")
                except sr.RequestError as e:
                    print(f"Could not request results from Google Speech Recognition service; {e}")
    
    # close the connection
    conn.close()

#!/usr/bin/env python
import socket
import time
import speech_recognition as sr
import threading
import rospy
from std_msgs.msg import String






def create_thread(data_buffer):
    #print(f"Thread {threading.current_thread().name} is running, data size is: {len(data_buffer)}")
    # Convert the accumulated data to an AudioData object
    audio_data = sr.AudioData(data_buffer, sample_rate=SAMPLE_RATE, sample_width=SAMPLE_WIDTH)
    # Transcribe the audio data
    try:
        transcript = r.recognize_google(audio_data)
        text_publisher.publish(transcript)
        
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")





text_publisher = rospy.Publisher('/speech_recognition_output',String,queue_size=1)
rospy.init_node('audio_reciever_speech_recognition',anonymous=True)

# Initialize the recognizer
r = sr.Recognizer()

# Set up a socket to receive audio data
HOST = ''  # Listen on all available interfaces
PORT = 5000  # Use a free port number
CHUNK = 1024  # Number of bytes to receive at a time
SAMPLE_RATE = 44100  # Sample rate of the audio data
SAMPLE_WIDTH = 2  # Sample width of the audio data
RECORD_SECONDS = 1.5  # Duration of audio to accumulate before processing
OVERLAP_SECONDS = 0.5  # Duration of overlap between consecutive audio segments


while not rospy.is_shutdown():

    
    start = None
    def callback(data):
        global start 
        #nonlocal finished
        start = data.data 

    rospy.Subscriber('/start_recognition', String, callback)
    while not rospy.is_shutdown():
        if (start is not None):
            break
    


    count = 0
    audio_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    audio_socket.bind((HOST, PORT))
    audio_socket.listen()
    print(f"Listening for audio data on {HOST}:{PORT}...")
    conn, addr = audio_socket.accept()


    with conn:
        print(f"Connected by {addr}")
        data_buffer = b''  # Initialize an empty buffer to store received data
        start_time = time.time()  # Record the start time of the recording
        end_time = start_time + RECORD_SECONDS
        overlap_buffer = None  

        finished = None
        def callback_finished(data):
            global finished 
            #nonlocal finished
            finished = data.data 

        rospy.Subscriber('/finish_recognition', String, callback_finished)

        while not rospy.is_shutdown():
            
            if (finished is not None):
                audio_socket.close()
                break
                
            # Receive audio data from the client
            data = conn.recv(CHUNK)
            if not data:
                break
            
            # Accumulate received data in the buffer
            data_buffer += data
            
            # Check if the accumulated data is greater than or equal to RECORD_SECONDS
            elapsed_time = time.time() - start_time
            
            if elapsed_time >= RECORD_SECONDS + OVERLAP_SECONDS:


                if overlap_buffer is not None:
                    data_buffer = overlap_buffer + data_buffer
                    overlap_buffer = None

                
                if (count % 3 == 0):
                    thread0 = threading.Thread(target=create_thread,args=(data_buffer,), name="Thread 0")
                    thread0.start()
                if (count % 3 == 1):
                    thread1 = threading.Thread(target=create_thread,args=(data_buffer,), name="Thread 1")
                    thread1.start()
                if (count % 3 == 2):
                    thread2 = threading.Thread(target=create_thread,args=(data_buffer,), name="Thread 2")
                    thread2.start()
                count = (count + 1) % 3

                # Update the buffer and start and end times for the next recording
                overlap_seconds = RECORD_SECONDS * 0.15  # Calculate the overlap duration
                overlap_buffer = data_buffer[-int(overlap_seconds*SAMPLE_RATE*SAMPLE_WIDTH):]
                data_buffer = data_buffer[-int((RECORD_SECONDS-overlap_seconds)*SAMPLE_RATE*SAMPLE_WIDTH):]
                start_time = end_time - overlap_seconds
                end_time += RECORD_SECONDS - overlap_seconds


    # Close the existing socket
    audio_socket.close()


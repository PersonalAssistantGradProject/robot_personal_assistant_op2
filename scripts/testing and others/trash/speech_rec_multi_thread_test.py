#!/usr/bin/env python
import time
import threading
import speech_recognition as sr
import os
import concurrent.futures
import sys

recognizer = sr.Recognizer()

def listen(message = "", to = 30):

    
    # use the recognizer to record audio from the microphone
    
    with sr.Microphone() as source:
        # adjust the recognizer for ambient noise of the source (optional)
        recognizer.adjust_for_ambient_noise(source)
        # clear the screen then print passed message
        #os.system('clear')
        print(message)
        # listen to the use for four seconds
        try:
            audio = recognizer.listen(source, timeout = to)
        except:
            print("User is quite.")
            return "."
    

    # perform speech recognition
    try:
        # use Google Web Speech API for speech recognition
        transcript = recognizer.recognize_google(audio, language='en-US')
    except sr.UnknownValueError:
        print("Unable to recognize speech for " +  message)
        return ""
    except sr.RequestError:
        print("Failed to connect to speech recognition service")
        return ""


    return transcript

output1 = " "
output2 = " "
output3 = " "
def listen_test():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        while True:

            future1 = executor.submit(listen, "test1", 0.8)
            time.sleep(0.2)
            try:
                output3 = future3.result()
                if (output3.find("Darwin") != -1 or output3.find("darling") != -1 or output3.find("Darlin") != -1):
                    print("SUCCESSFULL ----------------------------------------------------------------------------")
                    return
            except:
                print("fail")
                time.sleep(0.2)
            

            future2 = executor.submit(listen, "test2", 0.8)
            time.sleep(0.2)
            try:
                output1 = future1.result()
                if (output1.find("Darwin") != -1 or output1.find("darling") != -1 or output1.find("Darlin") != -1):
                    print("SUCCESSFULL ----------------------------------------------------------------------------")
                    return
            except:
                print("fail")
                time.sleep(0.2)


            future3 = executor.submit(listen, "test3", 0.8)
            time.sleep(0.2)
            try:
                output2 = future2.result()
                if (output2.find("Darwin") != -1 or output2.find("darling") != -1 or output2.find("Darlin") != -1):
                    print("SUCCESSFULL ----------------------------------------------------------------------------")
                    return
            except:
                print("fail")
                time.sleep(0.2)
            

            

listen_test()
print("finished!!!!!!!!!!!!!!!!")
print("Output 1:", output1)
print("Output 2:", output2)
print("Output 3:", output3)

  



'''
count = 0
while True:
    t1 = threading.Thread(target=listen, args=("test1", 1))
    t2 = threading.Thread(target=listen, args=("test2", 1))
    t1.start()
    time.sleep(1)
    t2.start()
    time.sleep(1)

    t1.join()
    t2.join()
    output1 = t1.result()
    output2 = t2.result()
    #transcript = listen("Darwin is listening to you, please speak out.",1)
    #print("User said: ", transcript)
    print("User said: ", output1)
    print("User said: ", output2)
    print(count)
    count = count+1

'''
#!/usr/bin/env python
import speech_recognition as sr
import rospy
from std_msgs.msg import Int32
import time

def speech_recognizer(words_list = []):

    
    print("started speech recognizer!")
    rospy.init_node('speech_recognizer', anonymous=True)

    rate = rospy.Rate(1) # 1Hz
    last_seg_num = None
    def callback(data):
        nonlocal last_seg_num
        last_seg_num = data
    

    
    # create a new recognizer instance
    recognizer = sr.Recognizer()
    
    found_words = []
    rospy.Subscriber('/seg_num', Int32, callback)
    while not rospy.is_shutdown():
        if last_seg_num is not None:

            WAVE_OUTPUT_FILENAME = "audio_test/recorded_audio" + str(last_seg_num.data) +".wav"
            print(WAVE_OUTPUT_FILENAME)

            try:
                with sr.AudioFile(WAVE_OUTPUT_FILENAME) as source:
                    try:
                        #recognizer.adjust_for_ambient_noise(source)
                        print("TEST55555")
                        audio_data = recognizer.listen(source)
                    except:
                        print("User is quite.")
                    
                    # perform speech recognition
                    try:
                        # use Google Web Speech API for speech recognition
                        print("TEST666")
                        transcript = recognizer.recognize_google(audio_data, language='en-US', timeout=5)
                        print("TEST777")
                    except sr.UnknownValueError:
                        print("Unable to recognize speech")
                        continue
                    except sr.RequestError:
                        print("Failed to connect to speech recognition service")
                        continue
                    except sr.WaitTimeoutError:
                        print("Speech recognition timed out")
                        continue
                    print(f"Speech recognized: {transcript}")
                    words_in_transcript = transcript.split()
                    for word in words_list():
                        if word in words_in_transcript:
                            found_words.append(word)
                    print(found_words)
                    if found_words:
                        return found_words                    
            except:
                print("file not found!")
        rate.sleep()
        #time.sleep(5)



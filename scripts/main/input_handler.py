#!/usr/bin/env python
"""


This Python file serves as the primary module for handling user input. It 
imports and utilizes functions from other Python files to accomplish its tasks.



"""

# imported libraries
import speech_recognition as sr                        
import rospy                          
from std_msgs.msg import String       
import time
import os
import threading
import face_recognizer # face_recognizer.py
import command_handler # command_handler.py
import text_to_speech_publisher # text_to_speech_publisher.py
import word_finder # word_finder.py


######################################################################################################################################
######################################################### listen to the user #########################################################


def listen(message = "", to = 30):

    
    # use the recognizer to record audio from the microphone
    
    with sr.Microphone() as source:
        # adjust the recognizer for ambient noise of the source (optional)
        recognizer.adjust_for_ambient_noise(source)
        # clear the screen then print passed message
        os.system('clear')
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
        print("Unable to recognize speech")
        return ""
    except sr.RequestError:
        print("Failed to connect to speech recognition service")
        return ""


    return transcript




######################################################################################################################################
############################################## subscribe to voice stream from the robot ##############################################



####################################################### function to publish the text to the robot

def speak_text(output_text, sleeptime):

    pub = rospy.Publisher('tts',String,queue_size=10)
    rospy.init_node('text_pub',anonymous=True)
    rate = rospy.Rate(10)
    rospy.loginfo(output_text)
    pub.publish(output_text)
    rate.sleep()
    time.sleep(sleeptime)







######################################################################################################################################
########################################################### main function ############################################################


if __name__ == '__main__' :

    
    print("started")
    # initalize ROS node 'input_handler'
    text_publisher = text_to_speech_publisher.init()
    rospy.init_node('input_handler', anonymous=True)
    
    str1 = "In addition to its economic and social benefits, education also has important personal benefits. It can improve individuals' health outcomes, as people with higher levels of education tend to have better health and access to healthcare. Education can also increase individuals' life satisfaction and overall well-being, as it provides them with opportunities for personal growth and self-fulfillment."
    str2 = "Overall, education is essential for personal, social, and economic development, and is a fundamental human right that should be accessible to all. By investing in education, we can create a brighter future for individuals and society as a whole."
    str3 = "Education is one of the most essential components of human development, as it is through education that individuals acquire knowledge, skills, and values that enable them to thrive in society. Education is not only important for personal development but also for societal and economic development. It allows individuals to gain a deeper understanding of the world around them, and provides them with the tools necessary to solve problems and make informed decisions. Education also plays a critical role in creating a more just and equitable society, as it can be used to address social inequalities and promote social mobility."
    str4 = "In the workplace, communication is critical for success. It is through communication that teams collaborate and work together to achieve common goals. Communication also enables employees to receive and provide feedback, which is essential for personal and professional growth. Good communication skills are also necessary for leadership, as effective leaders must be able to articulate their vision and goals to their team while also listening to and addressing the concerns and ideas of their team members. In addition to its interpersonal and professional benefits, communication is also important for personal growth and self-expression. Communication enables individuals to express themselves creatively, share their experiences and perspectives, and connect with others who share their interests and passions."
    str5 = "Hello my name is Amo! How can I help you?"
    
    text_to_speech_publisher.publish_text(str5, text_publisher)
    
    print("i finished talking")

    omar_image,mohammad_image,ahmad_image = face_recognizer.load_faces()
    print("faces have been loaded!")
    welcome_string = "Hello"
    number_of_auth_users = 0
    while True:
        auth_results = face_recognizer.recongize_faces(omar_image, mohammad_image, ahmad_image)

        if (auth_results[0]):
            # say hello Omar & welcome back
            welcome_string+= " Omar"
            number_of_auth_users += 1 

        if (auth_results[1]):
            # say hello Mohammad & welcome back
            if(number_of_auth_users > 0):
                welcome_string+= " and"
            welcome_string+= " Mohammad"
            number_of_auth_users +=1

        if (auth_results[2]):
            # say hello Ahmad & welcome back
            if(number_of_auth_users > 0):
                welcome_string+= " and"
            welcome_string+= " Ahmad"
            number_of_auth_users +=1


        if (number_of_auth_users > 0):
            welcome_string+= "."
            break
        else:
            print("Not authentic user. . . ")



    list_of_words = ["darwin","darling","darlin"]
    count = 0
    while True:
        word_finder.check_words(list_of_words)
        print("user said darwin",count)
        count += 1
        
    text_to_speech_publisher.publish_text(welcome_string, text_publisher)
    print(welcome_string)
        
    exit(0)
    time.sleep(100)
    
    #print("Finished!!!!!!!!!!!!!!!!!!!!!!!")
    #time.sleep(5)
    found_words = speech_recognizer.speech_recognizer(["Darwin","darling","Darlin"])
    print(found_words)
    print("Finished222222222222222222!!!!!!!!!!!!!!!!!!!!!!!")


    time.sleep(100)

    # create a recognizer object
    recognizer = sr.Recognizer()





    while True:

        # listen to the user
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
        transcript =""
        # check if user said "hey Darwin" or "hey darling"
        if (transcript.find("hey Darwin") != -1 or transcript.find("hey darling") != -1 or transcript.find("hey Darlin") != -1):

            transcript = listen("Hello, how can i help you?", 5)
            print("User said: ", transcript)
            text = command_handler.command_handler(transcript)
            print(text)
            text_to_speek = "Hello, how can i help you?" # randomize this
            #print("Darwin said: ", text_to_speek)
            
            # here publish 'text_to_speek' to the robot so that it can speak it out loud, also perform simple action if possible



        #time.sleep(5) # for testing



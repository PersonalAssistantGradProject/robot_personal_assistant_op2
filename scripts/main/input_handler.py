#!/usr/bin/env python


import speech_recognition as sr             
import random                         
import rospy                          
from std_msgs.msg import String       
from datetime import datetime
import time
import wolframalpha
import os
import pain_handler
import threading
import face_recognition
import facial_recognition
import speech_recognizer


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


####################################################### generate the required text

def handle_command(transcript):


    output_text = " "

    # handle pain
    if (transcript.find("pain") != -1 or transcript.find("hurt") != -1 or transcript.find("backache") != -1 ):
        state = 0
        if (transcript.find("neck") != -1):
            state = 2
        elif (transcript.find("back") != -1):
            state = 4 
        elif (transcript.find("leg") != -1 or transcript.find("knee") != -1 or transcript.find("foot") != -1 or transcript.find("feet") != -1):
            state = 5
        elif (transcript.find("arm") != -1 or transcript.find("wrist") != -1 or transcript.find("hand") != -1 ):
            state = 6
        elif (transcript.find("shoulder") != -1):
            state = 7
        else:
            output_text = "It would be a great idea to go see a doctor if the pain you described doesn't go away."
        if(state != 0):
            pain_handler.process_state(state)




    # tell a joke
    elif (transcript.find("joke") != -1):

        joke_num = random.randint(0, 1)
        if (joke_num == 0):
            output_text = "Why don\'t scientists trust atoms? Because they make up everything. HAHAHAHAHAHAHA" 
            #speak_text(output_text,7)

        elif (joke_num == 1):
            output_text = "What did the policeman say to his hungry stomach? Freeze. You\'re under a vest. HAHAHAHAHAHAHA"
            #speak_text(output_text,8)

        



    # take a note
    elif (transcript.find("note") != -1):


        # say: Please speak out your note!
        transcript = listen("Please speak out your note!")





        
            


        # Open file in write mode
        with open("example.txt", "w") as f:
                # Write string to file
                f.write(transcript)
                output_text = "Your note was saved as a txt file!"
                speak_text(output_text,4)



    elif (transcript.find("time") != -1 or transcript.find("date") != -1):

    
        # datetime object containing current date and time
        now = datetime.now()
        
        print("now =", now)

        # dd/mm/YY H:M:S
        
        month = now.strftime("%m")
        if (month == "01"):
            month = "January"
        elif (month == "02"):
            month = "February"
        elif (month == "03"):
            month = "March"
        elif (month == "04"):
            month = "April"
        elif (month == "05"):
            month = "May"
        elif (month == "06"):
            month = "June"
        elif (month == "07"):
            month = "July"
        elif (month == "08"):
            month = "August"
        elif (month == "09"):
            month = "September"
        elif (month == "10"):
            month = "October"
        elif (month == "11"):
            month = "November"
        elif (month == "12"):
            month = "December"


        hour = int(now.strftime("%H"))

        if (hour < 12):
            ampm = "A.M."
        elif (hour == 12):
            ampm = "P.M."
        else:
            hour = hour - 12
            ampm = "P.M."

        hour = str(hour)



        if (transcript.find("date") != -1):
            output_text = now.strftime("today's date is %d " + month + " %Y.")
            print(output_text)
            speak_text(output_text,3)

        if (transcript.find("time") != -1):
            output_text = now.strftime(" Time now is " + hour + ":%M " + ampm)
            print(output_text)
            speak_text(output_text,3)



    elif (transcript.find("search") != -1):

        print("Say your question!")
        output_text = "Please speak out your question!"
        speak_text(output_text,4)
        with sr.Microphone() as source:
            

            r.adjust_for_ambient_noise(source)
            audio_text = r.listen(source)

            # using google speech recognition
            #print("Text: "+r.recognize_google(audio_text))
            transcript = r.recognize_google(audio_text)
            print ("User said: ", transcript)
            question = transcript

            # App id obtained by the above steps
            app_id = "7KHGE6-RTHTWQXY7G"
            
            # Instance of wolf ram alpha 
            # client class
            client = wolframalpha.Client(app_id)

            # Stores the response from 
            # wolf ram alpha
            res = client.query(question)

            # Includes only text from the response
            output_text = next(res.results).text
            print(output_text)
            speak_text(output_text,5)
  

    




    # google api
    """ query = "who won world cup 2022"
    url = f"https://www.google.com/search?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    print (response)


    soup = BeautifulSoup(response.content, 'html.parser')
    print (soup)
    answer_box = soup.find('div', class_='Z0LcW')
    print(answer_box) """


    return output_text





######################################################################################################################################
########################################################### main function ############################################################


if __name__ == '__main__' :

    """ 

    omar_image = face_recognition.load_image_file("op2_tmp/omar.jpg")
    mohammad_image = face_recognition.load_image_file("op2_tmp/mohammad.jpg")
    ahmad_image = face_recognition.load_image_file("op2_tmp/ahmad.jpg")
    print("faces have been loaded!")

    while True:
        auth_results = facial_recognition.recongize_faces(omar_image, mohammad_image, ahmad_image)

        if (auth_results[0]):
            # say hello Omar & welcome back
            print("Hello Omar")
            break

        elif (auth_results[1]):
            # say hello Mohammad & welcome back
            print("Hello Mohammad")
            break

        elif (auth_results[2]):
            # say hello Ahmad & welcome back
            print("Hello Ahmad")
            break
        else:
            print("Not authentic user. . . ")

     """

        


    
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
            text = handle_command(transcript)
            print(text)
            text_to_speek = "Hello, how can i help you?" # randomize this
            #print("Darwin said: ", text_to_speek)
            
            # here publish 'text_to_speek' to the robot so that it can speak it out loud, also perform simple action if possible



        #time.sleep(5) # for testing



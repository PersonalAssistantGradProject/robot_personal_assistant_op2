#!/usr/bin/env python

import speech_recognition as sr       # PART 2
import requests                       # PART 4
from bs4 import BeautifulSoup         # PART 4
import random                         # PART 4

import rospy                          # PART 3
from std_msgs.msg import String       # PART 3
from datetime import datetime
import time
import wolframalpha
  

####################################################### PART 1 - subscribe to voice stream from the robot



####################################################### PART 2 - function to publish the text to the robot

pub = rospy.Publisher('tts',String,queue_size=10)
rospy.init_node('text_pub',anonymous=True)
rate = rospy.Rate(10)
def speak_text(output_text, sleeptime):

    rospy.loginfo(output_text)
    pub.publish(output_text)
    rate.sleep()
    time.sleep(sleeptime)


####################################################### PART 3 - generate the required text

def generate_text(user_said):


    output_text = " "


    # telling a joke
    if (user_said.find("joke") != -1):

        joke_num = random.randint(0, 1)
        if (joke_num == 0):
            output_text = "Why don\'t scientists trust atoms? Because they make up everything. HAHAHAHAHAHAHA"
            speak_text(output_text,7)

        elif (joke_num == 1):
            output_text = "What did the policeman say to his hungry stomach? Freeze. You\'re under a vest. HAHAHAHAHAHAHA"
            speak_text(output_text,8)

        



    # take a note
    elif (user_said.find("note") != -1):


        with sr.Microphone() as source:

            print("Say your note!")
            output_text = "Please speak out your note!"
            speak_text(output_text,3)

            audio_text = r.listen(source)

            # using google speech recognition
            #print("Text: "+r.recognize_google(audio_text))
            user_said = r.recognize_google(audio_text)
            print ("User said: ", user_said)
            # Open file in write mode
            with open("example.txt", "w") as f:
                # Write string to file
                f.write(user_said)
                output_text = "Your note was saved as a txt file!"
                speak_text(output_text,4)



    elif (user_said.find("time") != -1 or user_said.find("date") != -1):

    
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



        if (user_said.find("date") != -1):
            output_text = now.strftime("today's date is %d " + month + " %Y.")
            print(output_text)
            speak_text(output_text,3)

        if (user_said.find("time") != -1):
            output_text = now.strftime(" Time now is " + hour + ":%M " + ampm)
            print(output_text)
            speak_text(output_text,3)



    elif (user_said.find("search") != -1):

        print("Say your question!")
        output_text = "Please speak out your question!"
        speak_text(output_text,2)
        with sr.Microphone() as source:

            audio_text = r.listen(source)

            # using google speech recognition
            #print("Text: "+r.recognize_google(audio_text))
            user_said = r.recognize_google(audio_text)
            print ("User said: ", user_said)
            question = user_said

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



####################################################### PART 4 - speech to text


# Initialize recognizer class (for recognizing the speech)
r = sr.Recognizer()





while True:

    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:

        print("Say \"hey Darwin\"!")
        audio_text = r.listen(source)

        # using google speech recognition
        #print("Text: "+r.recognize_google(audio_text))
        user_said = r.recognize_google(audio_text)
        print ("User said: ", user_said)

        if (user_said.find("hey Darwin") != -1 or user_said.find("hey darling") != -1):


            output_text = generate_text(user_said)
            if (output_text == " "):


                print("how can i help you?") # placeholder
                with sr.Microphone() as source:

                    audio_text = r.listen(source)
                    #print("Text: "+r.recognize_google(audio_text))
                    user_said = r.recognize_google(audio_text)
                    print ("User said: ", user_said)
                    generate_text(user_said)

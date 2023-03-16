#!/usr/bin/env python

import speech_recognition as sr       # PART 2
import requests                       # PART 4
from bs4 import BeautifulSoup         # PART 4
import random                         # PART 4

import rospy                          # PART 3
from std_msgs.msg import String       # PART 3



####################################################### PART 1 - subscribe to voice stream from the robot


####################################################### PART 2 - speech to text


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

            print("how can i help you?") # placeholder
            with sr.Microphone() as source:

                audio_text = r.listen(source)
                #print("Text: "+r.recognize_google(audio_text))
                user_said = r.recognize_google(audio_text)
                print ("User said: ", user_said)
                break


####################################################### PART 3 - function to publish the text to the robot

pub = rospy.Publisher('tts',String,queue_size=10)
rospy.init_node('text_pub',anonymous=True)
rate = rospy.Rate(10)
def speak_text(output_text):

    rospy.loginfo(output_text)
    pub.publish(output_text)
    rate.sleep()

####################################################### PART 4 - generate the required text


output_text = ""


# telling a joke
if (user_said.find("joke") != -1):

    joke_num = random.randint(0, 1)
    if (joke_num == 0):
        output_text = "Why don\'t scientists trust atoms? Because they make up everything. hahahahaha"

    elif (joke_num == 1):
        output_text = "What did the policeman say to his hungry stomach? Freeze. You\'re under a vest. hahahahahaha"

speak_text(output_text)



# take a note
if (user_said.find("note") != -1):


    with sr.Microphone() as source:

        print("Say your note!")
        output_text = "Please speak out your note!"
        speak_text(output_text)

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
            speak_text(output_text)





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




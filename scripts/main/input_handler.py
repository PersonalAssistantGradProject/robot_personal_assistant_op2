#!/usr/bin/env python


import speech_recognition as sr             
import random                         
import rospy                          
from std_msgs.msg import String       
from datetime import datetime
import time
import wolframalpha
import os
  
######################################################################################################################################
######################################################### listen to the user #########################################################

def listen(message = ""):


    # create a recognizer object
    recognizer = sr.Recognizer()


    # use the recognizer to record audio from the microphone
    with sr.Microphone() as source:

        # adjust the recognizer for ambient noise of the source (optional)
        recognizer.adjust_for_ambient_noise(source)

        # clear the screen then print passed message
        os.system('clear')
        print(message)

        # listen to the use for four seconds
        try:
            audio = recognizer.listen(source, timeout = 4.0)
        except:
            print("User is quite.")
            return ""
    

    # perform speech recognition
    try:
        # use Google Web Speech API for speech recognition
        transcript = recognizer.recognize_google(audio)
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
def publish():
    pub = rospy.Publisher('tts',String,queue_size=10)
    rospy.init_node('text_pub',anonymous=True)
    rate = rospy.Rate(10)
    def speak_text(output_text, sleeptime):

        rospy.loginfo(output_text)
        pub.publish(output_text)
        rate.sleep()
        time.sleep(sleeptime)


####################################################### generate the required text

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
            r.adjust_for_ambient_noise(source)
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
        speak_text(output_text,4)
        with sr.Microphone() as source:
            

            r.adjust_for_ambient_noise(source)
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





######################################################################################################################################
########################################################### main function ############################################################


if __name__ == '__main__' :

    while True:

        # listen to the user
        transcript = listen("Darwin is listening to you, please speak out.")
        print("User said: ", transcript)
        

        # check if user said "hey Darwin" or "hey darling"
        if (transcript.find("hey Darwin") != -1 or transcript.find("hey darling") != -1):

            text_to_speek = "Hello, how can i help you?" # randomize this 
            print("Darwin said said: ", text_to_speek)
            # here publish 'text_to_speek' to the robot so that it can speak it out loud, also perform simple action if possible
        time.sleep(5) # for testing



'''
while True:

    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:

        print("Say \"hey Darwin\"!")
        r.adjust_for_ambient_noise(source)
        audio_text = r.listen(source)

        # using google speech recognition
        #print("Text: "+r.recognize_google(audio_text))
        user_said = r.recognize_google(audio_text)
        print ("User said: ", user_said)

        if (user_said.find("hey Darwin") != -1 or user_said.find("hey darling") != -1):


            output_text = generate_text(user_said)
            if (output_text == " "):

                
                print("how can i help you?") # placeholder
                speak_text("how can i help you?",3)
                with sr.Microphone() as source:
                    
                    r.adjust_for_ambient_noise(source)
                    audio_text = r.listen(source)
                    #print("Text: "+r.recognize_google(audio_text))

                    user_said = r.recognize_google(audio_text)
                    print ("User said: ", user_said)
                    generate_text(user_said)
'''
#!/usr/bin/env python


# imported libraries
import speech_recognition as sr             
import random                                    
from datetime import datetime
import wolframalpha
import time
import pain_handler # pain_handler.py
import word_finder # word_finder.py
import text_to_speech_publisher # text_to_speech_publisher.py
import record_note # record_note.py


def handle_pain(pain_type):

    state = 0
    if (pain_type == "neck"):
        state = 2
    elif (pain_type == "back"):
        state = 4
    elif (pain_type == "leg" or pain_type == "knee" or pain_type == "foot" or pain_type == "feet"):
        state = 5
    elif (pain_type == "arm" or pain_type == "wrist" or pain_type == "arm"):
        state = 6
    elif (pain_type == "shoulder"):
        state = 7
    else:
        output_text = "I'm sorry to hear about the pain you're experiencing. . . "
            
        output_text += "I would strongly recommend seeking medical attention if the symptoms persist. . . "
            
        output_text += "A visit to a doctor may help determine the cause of the pain and lead to proper treatment. . ."
        text_to_speech_publisher.publish_text(output_text)
    if (state != 0):
        pain_handler.process_state(state)

    return    


def handle_joke():

    # choose random number
    joke_number = random.randint(0, 6)

    if (joke_number == 0):
        joke =  "How do you open a banana? With a mon-key. hahaha."

    elif (joke_number == 1):
        joke =  "What do you call a bee that can't make up its mind? A Maybe. hahaha."
    
    elif (joke_number == 2):
        joke =  "Why did the bicycle fall over? Because it was two tired! hahaha."
    
    elif (joke_number == 3):
        joke =  "Why did the computer get cold? Because it left its Windows open! hahaha."

    elif (joke_number == 4):
        joke =  "Knock knock. Who's there? Olive. Olive who? Olive YOU!"

    elif (joke_number == 5):
        joke =  "Patient said: Doctor, I have a pain in my eye whenever I drink tea. " \
                "Doctor replied: Take the spoon out of the mug before you drink."
        
    elif (joke_number == 6):
        joke =  "The professor looked at the students and told them that you are the lamps of the future. " \
                "The student looked at his colleague who found him in the seventh sleep, and the student" \
                "said: Professor, the lamp next to me has burned out."
    
    # send the joke to the robot to say it
    text_to_speech_publisher.publish_text(joke)
    return
    
def handle_record_note(found_word):

    if (found_word == "play"):
        record_note.playback()
    else:
        record_note.record()
    return

    








def command_handler():

    
    # global list of words
    list_of_words =   ["pain","hurt","backache"] \
                    + ["joke","funny"] \
                    + ["play","note","record"] \
                    + ["time","date"] \
                    + ["search", "google","look"]

    
    found_word, pain_type = word_finder.check_words(list_of_words)

    print("found_word =", found_word)
    print ("pain_type =", pain_type)



    # handle pain
    if (found_word == "pain" or found_word == "hurt" or found_word == "backache"):
        handle_pain(pain_type)
        return




    # handle joke
    elif (found_word == "joke" or found_word == "funny"):
        handle_joke()
        return
        



    # take a note/record
    elif (found_word == "note" or found_word == "record" or found_word == "play"):
        handle_record_note(found_word)
        return

    print("got stuck")
    return


    
    '''
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


    return output_text'''

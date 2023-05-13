#!/usr/bin/env python


# imported libraries
import speech_recognition as sr             
import random                                    
from datetime import datetime

import time
import pain_handler # pain_handler.py
import word_finder # word_finder.py
import text_to_speech_publisher # text_to_speech_publisher.py
import record_note # record_note.py
import search_web # search_web.py
import search_wikipedia # search_wikipedia,py


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
        joke =  "How do you open a banana? With a mon-key. hahahaha."

    elif (joke_number == 1):
        joke =  "What do you call a bee that can't make up its mind? A Maybe. hahahaha."
    
    elif (joke_number == 2):
        joke =  "Why did the bicycle fall over? Because it was two tired! hahahaha."
    
    elif (joke_number == 3):
        joke =  "Why did the computer get cold? Because it left its Windows open! hahahaha."

    elif (joke_number == 4):
        joke =  "Knock knock. Who's there? Olive. Olive who? Olive YOU!"

    elif (joke_number == 5):
        joke =  "Patient said: Doctor, I have a pain in my eye whenever I drink tea. " \
                "Doctor replied: Take the spoon out of the mug before you drink. hahahaha."
        
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


def handle_introduce(found_word):
    if (found_word == "what can you do"):
        text_to_speak = "I am a personal assistant designed to accompany you while you work or study at your desk. \
                        I offer a wide range of services, including web searching, voice note taking, and playback, as well \
                        as time and date information. If you are experiencing any discomfort or pain in your back, shoulders, \
                        arms, legs, or neck, I can provide you with medical advice. Additionally, I can provide you with \
                        summaries of various topics from Wikipedia, tell you a joke if you need a mood boost, and provide \
                        you with current weather information."
        text_to_speech_publisher.publish_text(text_to_speak)
    else:
        text_to_speak = "Hello, my name is Darwin OP2, but you can call me Darwin. I am a fully autonomous humanoid robot \
                        designed to be your personal assistant while you work or study at your desk. I provide a wide range \
                        of services such as web searching, voice note taking, and playback, as well as time and date information. \
                        In case you experience discomfort or pain in your back, shoulders, arms, legs, or neck, \
                        I can offer you medical advice. Moreover, I can provide you with summaries of various topics from Wikipedia, \
                        crack a joke to cheer you up, and keep you updated on the current weather."
        text_to_speech_publisher.publish_text(text_to_speak)
    return


def handle_time_date(found_word):

    now = datetime.now()
    if (found_word == "time"):

        hour = int(now.strftime("%H"))

        if (hour < 12):
            ampm = "A.M."
        elif (hour == 12):
            ampm = "P.M."
        else:
            hour = hour - 12
            ampm = "P.M."

        hour = str(hour)
        text_to_speak = now.strftime(" Time now is " + hour + ":%M " + ampm)

    else:

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

        text_to_speak = now.strftime("today's date is %d " + month + " %Y.")
    text_to_speech_publisher.publish_text(text_to_speak)
    return






def command_handler():

    
    # global list of words
    list_of_words =   ["pain","hurt","backache"] \
                    + ["joke","funny"] \
                    + ["play","note","record"] \
                    + ["time","date"] \
                    + ["search", "google"] \
                    + ["what can you do", "who are you", "introduce"] \
                    + ["wikipedia"]

    
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


    elif (found_word == "what can you do" or  found_word == "who are you" or found_word =="introduce"):
        handle_introduce(found_word)
        return
    

    elif (found_word == "date" or  found_word == "time"):
        handle_time_date(found_word)
        return


    elif (found_word == "search" or  found_word == "google"):
        search_web.handle_search()
        return
    

    elif (found_word == "wikipedia"):
        search_wikipedia.handle_wikipedia()
        return


    print("got stuck")
    return
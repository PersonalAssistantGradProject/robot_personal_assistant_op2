#!/usr/bin/env python


# imported libraries           
import random
import time                     
from datetime import datetime
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
    elif (pain_type == "back" or pain_type == "backache"):
        state = 4
    elif (pain_type == "leg" or pain_type == "knee" or pain_type == "foot" or pain_type == "feet"):
        state = 5
    elif (pain_type == "arm" or pain_type == "wrist" or pain_type == "arm"):
        state = 6
    elif (pain_type == "shoulder"):
        state = 7
    elif (pain_type == "head" or pain_type == "headache"):
        output_text= ("I'm sorry to hear that. Maybe you could rest in a quiet place. "
                      "Find a calm and comfortable environment where you can lie down "
                      "and relax. Dimming the lights or closing the curtains can help "
                      "create a soothing atmosphere.")
        
        text_to_speech_publisher.publish_text(output_text)

    else:

        output_text = ("I'm sorry to hear about your pain. If the symptoms continue, "
                       "it's best to see a doctor. They can identify the cause of the "
                       "pain and provide appropriate treatment.")
        
        text_to_speech_publisher.publish_text(output_text)

        
    if (state != 0):
        pain_handler.process_state(state)

    return    


def handle_joke():

    # choose random number
    joke_number = random.randint(0, 6)

    if (joke_number == 0):
        joke = "How do you open a banana? With a mon-key. Hahahaha."

    elif (joke_number == 1):
        joke = "What do you call a bee that can't make up its mind? A Maybe. Hahahaha."
    
    elif (joke_number == 2):
        joke = "Why did the bicycle fall over? Because it was two tired. Hahahaha."
    
    elif (joke_number == 3):
        joke = "Why did the computer get cold? Because it left its Windows open. Hahahaha."

    elif (joke_number == 4):
        joke = "Knock knock. Who's there? Olive. Olive who? Olive YOU!"

    elif (joke_number == 5):
        joke = ("Patient said: Doctor, I have a pain in my eye whenever I drink tea. "
                "Doctor replied: Take the spoon out of the mug before you drink. Hahahaha.")
        
    elif (joke_number == 6):
        joke = ("The professor looked at the students and told them that you are the lamps of the future. "
                "The student looked at his colleague who found him in the seventh sleep, and the student "
                "said: Professor, the lamp next to me has burned out. Hahahaha.")
    
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
        paragraph = ["I am a personal assistant designed to accompany you while you work or study at your desk.",
                     "I offer a wide range of services, including web searching, voice note taking, and playback, as well as time and date information.",
                     "I will also keep track of your posture and make sure to alert you when you need to change it.",
                     "If you are experiencing any discomfort or pain in your back, shoulders, arms, legs, or neck, I can provide you with medical advice.",
                     "Additionally, I can provide you with summaries of various topics from Wikipedia, tell you a joke if you need a mood boost, and provide you with current weather information."]
        
        for sentence in paragraph:
            text_to_speech_publisher.publish_text(sentence, wait = False)
        time.sleep(40)
        
    else:
        paragraph = ["Hello, I'm Darwin, your personal assistant.",
                     "I provide various services like web searching, voice note taking, and time/date information.",
                     "I also keep track of your posture to ensure your comfort, and will alert you when it needs adjustment.",
                     "If you experience discomfort or pain in your back, shoulders, arms, legs, or neck, I can offer you medical advice.",
                     "Additionally, I can provide Wikipedia summaries, tell jokes, and keep you updated on the weather."]
        for sentence in paragraph:
            text_to_speech_publisher.publish_text(sentence, wait = False)
        time.sleep(31)
    
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

        text_to_speak = now.strftime("Today's date is %d " + month + " %Y.")
    text_to_speech_publisher.publish_text(text_to_speak)
    return



def command_handler():

    
    # global list of words
    list_of_words =   ["pain","hurt","backache","headache"] \
                    + ["joke","funny"] \
                    + ["play","note","record"] \
                    + ["time","date"] \
                    + ["wikipedia"] \
                    + ["search", "google"] \
                    + ["what can you do", "who are you", "introduce"]

    
    while True:
        print("\n----- Waiting for user to give command -----")
        found_word, pain_type = word_finder.check_words(list_of_words)
        print("\ncommand found:", found_word)
        if (pain_type != ""):
            print ("pain type:", pain_type)
        print("")



        # handle pain
        if (found_word == "pain" or found_word == "hurt" or found_word == "backache" or found_word == "headache"):
            if (found_word == "backache"):
                pain_type = found_word
            elif (found_word == "headache"):
                pain_type = found_word
            handle_pain(pain_type)


        # handle joke
        elif (found_word == "joke" or found_word == "funny"):
            handle_joke()
            

        # take a note/record
        elif (found_word == "note" or found_word == "record" or found_word == "play"):
            handle_record_note(found_word)


        elif (found_word == "what can you do" or  found_word == "who are you" or found_word =="introduce"):
            handle_introduce(found_word)
        

        elif (found_word == "date" or  found_word == "time"):
            handle_time_date(found_word)


        elif (found_word == "wikipedia"):
            search_wikipedia.handle_wikipedia()
        

        elif (found_word == "search" or  found_word == "google"):
            search_web.handle_search() 

        elif (found_word == "command_timeout"):
            break

        else:
            print("ERROR IN COMMAND HANDLING!!!!!!!!!!!! COMMAND NOT FOUND!!!")
        

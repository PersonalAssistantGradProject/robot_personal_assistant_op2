#!/usr/bin/env python


# imported libraries
import speech_recognition as sr             
import random                                    
from datetime import datetime
import wolframalpha
import pain_handler # pain_handler.py



def command_handler(transcript):


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

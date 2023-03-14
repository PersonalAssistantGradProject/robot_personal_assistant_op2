import speech_recognition as sr       # PART 2
import requests                       # PART 3
from bs4 import BeautifulSoup         # PART 3





####################################################### PART 1 - subscribe to voice stream from the robot


####################################################### PART 2 - speech to text


# Initialize recognizer class (for recognizing the speech)
""" r = sr.Recognizer()


while True:

    # Reading Microphone as source
    # listening the speech and store in audio_text variable
    with sr.Microphone() as source:

        print("Say \"hey Darwin\"!")
        audio_text = r.listen(source)

        # using google speech recognition
        #print("Text: "+r.recognize_google(audio_text))
        text = r.recognize_google(audio_text)
        print ("User said: ", text)

        if (text.find("hey Darwin") != -1 or text.find("hey darling") != -1):

            print("how can i help you?") # placeholder
            with sr.Microphone() as source:

                audio_text = r.listen(source)
                #print("Text: "+r.recognize_google(audio_text))
                text = r.recognize_google(audio_text)
                print ("User said: ", text)
                break """




####################################################### PART 3 - generate the required text



query = "who won world cup 2022"
url = f"https://www.google.com/search?q={query}"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
response = requests.get(url, headers=headers)
print (response)


soup = BeautifulSoup(response.content, 'html.parser')
print (soup)
answer_box = soup.find('div', class_='Z0LcW')
print(answer_box)

####################################################### PART 4 - publish the text to the robot
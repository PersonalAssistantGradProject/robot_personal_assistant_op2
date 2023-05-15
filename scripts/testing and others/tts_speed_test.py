#!/usr/bin/env python

# imported libraries
from gtts import gTTS
import pygame
import time
from io import BytesIO







def speak_1(text):

    
    print("generating audio")
    tts = gTTS(text=text, lang='en', tld='com', slow=False) 
    pygame.init()
    start_time = time.time()

    print("saving mp3 file")
    tts.save("test_speech.mp3")
    


    print("loading mp3 file")
    
    pygame.mixer.music.load("test_speech.mp3")
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds")
    pygame.mixer.music.play()
    while pygame.mixer.music.get_pos() > -1:
        pygame.time.Clock().tick(10)
    pygame.quit()


def speak_2(text):

    
    print("generating audio")
    tts = gTTS(text=text, lang='en', tld='com', slow=False) 
    pygame.mixer.init()
    start_time = time.time()

    print("saving mp3 file")
    audio = BytesIO()
    tts.write_to_fp(audio)
    audio.seek(0)
    sound = pygame.mixer.Sound(audio)
    end_time = time.time()
    total_time = end_time - start_time
    print(f"Total time taken: {total_time} seconds")


    sound.play()
    while pygame.mixer.get_busy():
        pass
    pygame.mixer.quit()




    


    
    
    


text_to_speak = "The night was cold and dark, with a thin layer of fog obscuring the streetlights. John walked briskly down the sidewalk, his hands buried deep in his coat pockets. He had just left a party at his friend's apartment, and he was feeling a little drunk and disoriented. As he approached the corner of the street, he heard a low growl coming from the alleyway to his left. He stopped in his tracks and looked over, but he couldn't see anything in the darkness. Suddenly, a pair of glowing"





speak_2(text_to_speak)
speak_1(text_to_speak)



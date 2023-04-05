import speech_recognition as sr

# Initialize recognizer
r = sr.Recognizer()

# Use microphone as source
with sr.Microphone() as source:
    print("Speak now...")
    # Adjust ambient noise for better recognition
    r.adjust_for_ambient_noise(source)
    # Listen for audio
    audio = r.listen(source)

try:
    # Transcribe audio using Google Speech Recognition
    text = r.recognize_google(audio)
    print("You said:", text)
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))

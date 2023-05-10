'''
import pyttsx3

# Create TTS engine
engine = pyttsx3.init()

# Set voice properties for robotic voice
engine.setProperty('rate', 150)  # Adjust speech rate (words per minute)
engine.setProperty('volume', 0.5)  # Adjust volume (0.0 to 1.0)
engine.setProperty('pitch', 50)

# Text to be converted to speech
text = "Hello, this is a robotic voice example using pyttsx3 in Python!"

# Generate speech
engine.say(text)
engine.runAndWait()



import subprocess

# Text to be converted to speech
text = "Hello, this is an example of adjusting the speed and pitch of the voice using espeak in Python!"

# Set desired speed (words per minute)
speed = 140  # Example: setting speed to 150 WPM

# Set desired pitch (0 to 99)
pitch = 50  # Example: setting pitch to 50, which represents a lower pitch

# Set desired voice variant or voice file path
voice = "ko"  # Example: setting voice to "en-us", which represents the US English accent

# Use espeak command with desired speed and pitch
subprocess.call(['espeak', '-v', voice, '-s', str(speed), '-p', str(pitch), text])




import subprocess

# Text to be converted to speech
text = "Hello, this is a robotic voice example using espeak in Python!"

# Set voice properties for robotic voice
voice = "en+f5"  # Specify voice and variant (en: English, f5: robotic voice variant)
rate = 150  # Adjust speech rate (words per minute)
pitch = 30
# Construct espeak command
espeak_cmd = ["espeak", "-v", voice,'-p', str(pitch), "-s", str(rate), text]

# Call espeak command using subprocess
subprocess.run(espeak_cmd)
'''



import subprocess

# Text to be converted to speech
text = "Darwin"

# Set desired pitch (0 to 99)
pitch = 50  # Example: setting pitch to 50, which represents a lower pitch

# Set desired speed (words per minute)
speed = 150  # Example: setting speed to 150 WPM

# Set path to voice file with altered pitch and speed
voice_file = "/home/ahmad/Introduction.mp3"  # Example: path to altered voice file

# Use espeak command with altered voice file
subprocess.call(['espeak', '-f', voice_file, '-p', str(pitch), '-s', str(speed), text])

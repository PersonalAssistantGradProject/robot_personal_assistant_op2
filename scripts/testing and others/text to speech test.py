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
text = "Hello, this is an example of adjusting the pitch of the voice using espeak in Python!"

# Set desired pitch level (0 to 99)
pitch = 0  # Example: setting pitch to 50, which represents a lower pitch

# Use espeak command with desired pitch
subprocess.call(['espeak', '-p', str(pitch), text])
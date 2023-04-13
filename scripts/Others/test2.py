from google.cloud import speech_v1
from google.cloud.speech_v1 import enums
import pyaudio
import io

# Define audio recording parameters
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Initialize PyAudio
audio = pyaudio.PyAudio()

# Start audio stream from microphone
stream = audio.open(format=FORMAT, channels=CHANNELS,
                    rate=RATE, input=True,
                    frames_per_buffer=CHUNK)

# Initialize Google Cloud client
client = speech_v1.SpeechClient()

# Configure audio input
audio_generator = stream.read(CHUNK)
audio_input = []
while audio_generator:
    audio_input.append(audio_generator)
    audio_generator = stream.read(CHUNK)

stream.stop_stream()
stream.close()
audio.terminate()

audio_content = b''.join(audio_input)

audio = speech_v1.RecognitionAudio(content=audio_content)
config = speech_v1.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=RATE,
    language_code='en-US')

# Perform transcription
response = client.recognize(config=config, audio=audio)
transcript = ''
for result in response.results:
    transcript += result.alternatives[0].transcript

print("Transcribed text:", transcript)

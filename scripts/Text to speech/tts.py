import pyttsx3


engine = pyttsx3.init()



# A function to allow the robot to speech any text it's given
def Say(text):
    engine.say(text)
    engine.runAndWait()



# this python script will subscribe to a ROS topic that has string messages (text) and then convert it to speech.



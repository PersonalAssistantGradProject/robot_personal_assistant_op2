#!/usr/bin/env python

"""

This Python file uses the "face_recognition" library to implement face 
recognition functionality. It defines a function named "recognize_faces"
which can accept three face images as parameters, although this value
can be changed.

The script first loads these three images using the"load_faces" function.

The "recognize_faces" function subscribers to the webcam of the robot. 
Whenever a new image is received ,the function processes it using the
"face_recognition" library to determine if any of the authorized users
are recognized.

The authentication results are returned as a tuple of three values, one for
each input face.

"""


# imported libraries
import face_recognition
import cv2
import rospy
import time
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import os
import random
import text_to_speech_publisher
import action_sender


# The "load_faces" function loads the images of the faces of the three
# authorized users (Omar, Mohammad, Ahmad) using the "load_image_file"
# function from the "face_recognition" library.
#
# The loaded face images are returned so that they can be used in the
# "recognize_faces" function.
#
# It is worth noting that the face images used can be changed if needed.
#
def init():

    omar_image_path = os.path.expanduser("~/op2_tmp/omar.jpg") # path to Omar face image, change if needed.
    omar_image = face_recognition.load_image_file(omar_image_path) 
    mohammad_image_path = os.path.expanduser("~/op2_tmp/mohammad.jpg") # path to Mohammad face image, change if needed.
    mohammad_image = face_recognition.load_image_file(mohammad_image_path) 
    ahmad_image_path = os.path.expanduser("~/op2_tmp/ahmad.jpg") # path to Ahmad face image, change if needed.
    ahmad_image = face_recognition.load_image_file(ahmad_image_path) 

    global omar_face_encoding
    global mohammad_face_encoding
    global ahmad_face_encoding
    omar_face_encoding = face_recognition.face_encodings(omar_image)[0]
    mohammad_face_encoding = face_recognition.face_encodings(mohammad_image)[0]
    ahmad_face_encoding = face_recognition.face_encodings(ahmad_image)[0]




# The "recognize_faces" function accepts three face images as parameters,
# which are the faces of the authorized users.
#
# It initializes a ROS node named "face_recognizer" using the "rospy"
# library and subscribes to the "/webcam" topic.
#
# When called, the function processes the most recent image published by
# the robot using the "face_recognition" library to determine if any of
# the authorized users are recognized.
#
# The authentication results are returned as a tuple of three values,
# one for each input face.
#
# Note that the faces of the authorized users can be easily modified.
#
# The function is invoked in an infinite loop by "input_handler.py"
# until one of the authorized users is successfully recognized.
#

def recongize_faces():

    global omar_face_encoding
    global mohammad_face_encoding
    global ahmad_face_encoding
    

    # CvBridge to convert the recieved image into suitable format
    bridge = CvBridge()
    rate = rospy.Rate(1) # 1Hz
    last_image = None

    # callback function called when an image is recieved on '/webcam'
    def callback(data):
        nonlocal last_image
        # convert the recieved image into suitable format using CvBridge
        last_image = bridge.imgmsg_to_cv2(data, "bgr8")

    # define subscriber on ROS topic '/webcam' with Image data 
    rospy.Subscriber('/webcam', Image, callback)

    unknown_image_path = os.path.expanduser("~/op2_tmp/unknown.jpg")

    # perform face recognition on the recieved image
    while not rospy.is_shutdown():

        if last_image is not None:

            
            # save the image to the path 'op2_tmp/unknown.jpg'
            cv2.imwrite(unknown_image_path, last_image)

            # load the image using 'load_image_file' 
            unknown_image = face_recognition.load_image_file(unknown_image_path)

            # Get the face encodings for each face in each face image
            # Since there could be more than one face in each image, it returns a list of encodings.
            # But since I know each image only has one face, I only care about the first encoding in each image, so I grab index 0.
            try:
                unknown_face_encoding = face_recognition.face_encodings(unknown_image)
            except IndexError:
                return [False, False, False]

            known_faces = [
                omar_face_encoding,
                mohammad_face_encoding,
                ahmad_face_encoding
            ]
            auth_results = [False, False, False]
            for face in unknown_face_encoding:
                # results is an array of True/False telling if the unknown face matched anyone in the known_faces array
                face_results = face_recognition.compare_faces(known_faces, face, tolerance=0.4)
                auth_results = [x or y for x, y in zip(auth_results, face_results)]
            
            
            return auth_results
            
        rate.sleep()



def security_check():

    print("----- Started authentication step using face recognition -----")
    text_num = random.randint(0, 1)
    if (text_num == 0):
        welcome_message = "Hello"
    elif (text_num == 1):
        welcome_message = "Welcome"
    
    
    number_of_auth_users = 0
    while True:
        auth_results = recongize_faces()

        if (auth_results[0]):
            welcome_message+= " Omar"
            number_of_auth_users += 1 

        if (auth_results[1]):
            if(number_of_auth_users > 0):
                welcome_message+= " and"
            welcome_message+= " Mohammad"
            number_of_auth_users +=1

        if (auth_results[2]):
            if(number_of_auth_users > 0):
                welcome_message+= " and"
            welcome_message+= " Ahmad"
            number_of_auth_users +=1

        if (number_of_auth_users > 0):
            random_number = random.random()
            if (random_number < 0.25):
                welcome_message+= ". Its good to see you again"
            welcome_message+= "."
            
            # welcome the user by standing up (action 100: inital position), and speak out welcome message
            action_sender.publish_action(100)
            text_to_speech_publisher.publish_text(welcome_message, wait = False)
            return
        else:
            print("- No authentic users found!")
    
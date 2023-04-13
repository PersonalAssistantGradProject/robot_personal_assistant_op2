#!/usr/bin/env python

# This python script subscribes (receives) the webcam image from the robot, then applies facial detection on it.


import cv2
import mediapipe as mp
print("test")
cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

while True:
    success, image = cap.read()
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(imageRGB)
    
 # checking whether a hand is detected
    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: # working with each hand
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)   
                #if (id == 8):
                cv2.circle(image, (cx, cy), 25, (0, 0, 255), cv2.FILLED)
            for id, lm in enumerate(handLms.landmark):
                h, w, c = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)   
                #if (id == 8):
                cv2.circle(image, (cx, cy), 25, (0, 0, 255), cv2.FILLED)
            #mpDraw.draw_landmarks(image, handLms, mpHands.HAND_CONNECTIONS)
    image = cv2.flip(image,1)
    cv2.imshow("Output", image)
    cv2.waitKey(1)
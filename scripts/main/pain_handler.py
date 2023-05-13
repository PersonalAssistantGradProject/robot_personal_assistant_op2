#!/usr/bin/env python
"""


This Python file contains a function named "process_state" which is
invoked by "input_handler.py". The purpose of this function is to
receive the user's state as input, and then instruct the robot to
execute the appropriate actions based on the state provided.


"""



import numpy as np
import rospkg
import os
from std_msgs.msg import Int32
import rospy
import random
import time
import text_to_speech_publisher # text_to_speech_publisher.py
import action_sender # action_sender.py
import word_finder # word_finder.py

# Function to print state number and name (used for testing)
def print_state(state):

    if(state == 0):
        print("State 0: no pain")
    elif(state == 1):
        print("State 1: neck pain + bad posture")
    elif(state == 2):
        print("State 2: neck pain")
    elif(state == 3):
        print("State 3: back pain + bad posture")
    elif(state == 4):
        print("State 4: back pain")
    elif(state == 5):
        print("State 5: leg pain")
    elif(state == 6):
        print("State 6: arm pain")
    else:
        print("State 7: shoulder pain")


# Function to print action number and name (used for testing)
def print_action(action):

    if(action == 0):
        print("Action 0 performed: neck_1")
    elif(action == 1):
        print("Action 1 performed: neck_2")
    elif(action == 2):
        print("Action 2 performed: arm_1")
    elif(action == 3):
        print("Action 3 performed: back_1")
    elif(action == 4):
        print("Action 4 performed: leg_1")
    elif(action == 5):
        print("Action 5 performed: back_2")
    elif(action == 6):
        print("Action 6 performed: arm_2")
    elif(action == 7):
        print("Action 7 performed: walk")
    elif(action == 8):
        print("Action 8 performed: extend knee")
    elif(action == 9):
        print("Action 9 performed: extend palm")
    elif(action == 10):
        print("Action 10 performed: side bending")
    else:
        print("Action 11: see a doctor")


# action 101 = 14s
# action 102 = 14s
# action 103 = 6s
# action 104 = 11s
# action 105 = 13s
# action 106 = 20s
# action 107 = 18s
def perform_action(action):
    
    advice = ""
    if random.random() < 0.50:
        text_num = random.randint(0,1)
        if(text_num == 0):
            advice = "hmmmmmmmmmmmmmmmmmmmmmmmm. "
        elif(text_num == 1):
            advice = "Let me think. Hmmmmmm. "
    if (action == 0):
        
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "Try to move your neck to the right, then move it to the left like this. Do it ten times."
        elif(text_num == 1):
            advice += "Here's an exercise for your neck. Tilt your head to the right, then to the left, like this. Do it ten times."
        elif(text_num == 2):
            advice += "Let's do a neck stretch. Rotate your head to the right, then to the left, like this. Repeat this motion ten times."
        text_to_speech_publisher.publish_text(advice,False)
        # send action 101
        time.sleep(2)
        action_sender.publish_action(101)
        time.sleep(14)

    elif (action == 1):
        
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "This neck exercise is quick and easy. Just move your neck up and down like this, five times."
        elif(text_num == 1):
            advice += "To stretch your neck muscles, try moving your head up and down like this, five times. It's a simple exercise."
        elif(text_num == 2):
            advice += "Could you please move your neck up and down like this five times?"
        text_to_speech_publisher.publish_text(advice,False)
        # send action 102
        time.sleep(2)
        action_sender.publish_action(102)
        time.sleep(14)
    elif (action == 2):
        
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "Let's do a simple arm stretch. Raise your arms like a fork, and hold it for ten seconds. It'll help relieve tension."
        elif(text_num == 1):
            advice += "This arm exercise is quick and effective. Raise your arms like a fork, like this, and hold it for ten seconds."
        elif(text_num == 2):
            advice += "Try raising your arms like a fork like this. Hold it for ten seconds."
        
        text_to_speech_publisher.publish_text(advice,False)
        # send action 103
        time.sleep(2)
        action_sender.publish_action(103)
        time.sleep(6)
        
    elif (action == 3):
        
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "Let's try a standing lower back stretch. Look at me and follow along."
        elif(text_num == 1):
            advice += "This standing lower back stretch is quick and effective. Watch me and try it yourself."
        elif(text_num == 2):
            advice += "You can do a standing lower back stretch. Look at me how I am doing it."
        text_to_speech_publisher.publish_text(advice,False)
        # send action 104
        time.sleep(2)
        action_sender.publish_action(104)
        time.sleep(11)
    elif (action == 4):
        
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "Let's try a balance exercise. Stand on one leg, lift your other leg behind you, and hold it with your arm for five seconds."
        elif(text_num == 1):
            advice += "Can you try this simple standing balance exercise with me? Lift one leg behind you and hold it with your arm for five seconds, while standing on one leg."
        elif(text_num == 2):
            advice += "Try to stand on one leg, raise your other leg to the back, then use your arm to hold your extended leg for five seconds. "
        
        text_to_speech_publisher.publish_text(advice,False)
        # send action 105
        time.sleep(2)
        action_sender.publish_action(105)
        time.sleep(13)
    elif (action == 5):
        
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "Let's try a balance exercise. Stand on one leg, lift your other leg behind you, and hold it with your arm for five seconds."
        elif(text_num == 1):
            advice += "Can you try this simple standing balance exercise with me? Lift one leg behind you and hold it with your arm for five seconds, while standing on one leg."
        elif(text_num == 2):
            advice +="Try to make your elbows 90 angle, then pull your arms to the back. Do it 10 times."
        
        text_to_speech_publisher.publish_text(advice,False)
        # send action 106
        time.sleep(2)
        action_sender.publish_action(106)
        time.sleep(20)

    elif (action == 6):
        
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "Can you do this arm exercise with me? Make a 90-degree angle with your elbows, then extend your arms out to the sides. Repeat ten times."
        elif(text_num == 1):
            advice += "Can you try this arm workout? Make a right angle with your elbows, then stretch your arms out to the sides. Repeat ten times."
        elif(text_num == 2):
            advice +="For this exercise, raise your elbows to shoulder height and then extend your arms out to the sides. Repeat ten times."
      
        text_to_speech_publisher.publish_text(advice,False)
        # send action 107
        time.sleep(2)
        action_sender.publish_action(107)
        time.sleep(18)


    elif (action == 7):
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "You could try and walk around for a few minutes. This could help reduce your pain"
        elif(text_num == 1):
            advice += "Maybe walking around for a few minutes could help reduce your discomfort. Would you like to try it?"
        elif(text_num == 2):
            advice +="For this exercise, raise your elbows to shoulder height and then extend your arms out to the sides. Repeat ten times."
       
        text_to_speech_publisher.publish_text(advice)


    elif (action == 8):
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "Make sure your knee is fully extended and has a slight bend of more than ninty degrees."
        elif(text_num == 1):
            advice += "Check that your knee is extended and has a comfortable bend wider than ninty degrees."
        elif(text_num == 2):
             advice += "Please make sure that your knee is well extended. It should have an angle a little wider than ninty degrees."
       
        text_to_speech_publisher.publish_text(advice)


    elif (action == 9):
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "Would you like to try extending your other arm downwards for a few seconds? It could potentially reduce your discomfort."
        elif(text_num == 1):
            advice += "You could try using your opposite arm to extend downwards for a few seconds. It might help reduce your discomfort."
        elif(text_num == 2):
             advice += "Using your other arm. Extend your arm downwards for a few seconds. This could reduce your pain."
        
        text_to_speech_publisher.publish_text(advice)


    elif (action == 10):
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "Side bend your head to the left and right, holding each position for a few seconds. Do this three times on each side."
        elif(text_num == 1):
            advice += "Would you like to try side bending your head to the left and right? Repeat the movement three times on each side."
        elif(text_num == 2):
            advice += "Try to side bend your head to the left and right. Do it 3 times for each side."
        
        text_to_speech_publisher.publish_text(advice)


    elif (action == 11):
        # say this
        text_num = random.randint(0,2)
        if(text_num == 0):
            advice += "If your pain continues, it may be worth considering consulting a doctor. I'm sorry that my suggestion didn't help."
        elif(text_num == 1):
            advice += "If the pain persists, it might be a good idea to see a doctor. I apologize that my suggestion didn't provide relief."
        elif(text_num == 2):
            advice = "I'm sorry that my advice wasn't helpful. It might be worth considering seeing a medical professional if your pain continues."
        
        text_to_speech_publisher.publish_text(advice)




    

        
def process_state(state):
    

    # load Q-table from "scripts/main/q_learning/q_table.npy"
    rospack = rospkg.RosPack()
    package_path = rospack.get_path('robot_personal_assistant_op2')
    q_table_path = os.path.join(package_path, 'scripts/main/q_learning/q_table.npy')
    q_table = np.load(q_table_path)

    # print updated Q-table
    np.set_printoptions(precision=3)
    print("\n\n----- Finalized Q-table -----\n")
    print(q_table)
    #state = random.randint(1,7)
    bad_posture_time = None
    '''
    def callback(data):
        nonlocal bad_posture_time
        # convert the recieved image into suitable format using CvBridge
        bad_posture_time = data.data

    if (state == 2 or state == 4):
        rospy.Subscriber('/bad_posture_time', Int32, callback)
        while not rospy.is_shutdown():
            if bad_posture_time is not None:
                if (bad_posture_time > 0):
                    state -=1
                    break
                else:
                    break
    '''
    print_state(state)



    while True:

        action = np.argmax(q_table[state,:])
        # perform the action

        print_action(action)
        perform_action(action)
        if (action == 11):
            break
  
  

        time.sleep(2)
        text_num = random.randint(0,2)
        if(text_num == 0):
            text_to_speak = "Are you satisfied?"
        elif(text_num == 1):
            text_to_speak = "Have you noticed any changes in your pain level?"
        elif(text_num == 2):
            text_to_speak = "Did your pain go away?"
        text_to_speech_publisher.publish_text(text_to_speak)
        
        list_of_words = ["yes","no"]
        found_word, pain_type = word_finder.check_words(list_of_words)
        
        if (found_word == "yes"):
            text_num = random.randint(0,1)
            if(text_num == 0):
                text_to_speak = "That's wonderful to hear!"
            elif(text_num == 1):
                text_to_speak ="I am really happy to hear that!"
            text_to_speech_publisher.publish_text(text_to_speak)
            break
        else:
            q_table[state,action] = 0
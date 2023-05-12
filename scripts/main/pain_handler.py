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
import text_to_speech_publisher # text_to_speech_publisher.py
import action_sender # action_sender.py

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

def perform_action(action):
    advice = ""
    if random.random() < 0.50:
        advice = "hmmmmmmmmmmmmmmmmmmmmmmmm. "
    if (action == 0):
        # send action 101
        action_sender.publish_action(101)
        # say this
        advice += "Try to move your neck to the left then to the right like this. Do it 10 times."
        text_to_speech_publisher.publish_text(advice)

    elif (action == 1):
        # send action 102
        action_sender.publish_action(102)
        # say this
        advice += "Try to move your neck to the up and down like this. . . Do it 5 times."
        text_to_speech_publisher.publish_text(advice)
    elif (action == 2):
        # send action 103
        action_sender.publish_action(103)
        # say this
        advice += "Try raising your arms like a fork like this. . . Hold it for 10 seconds."
        text_to_speech_publisher.publish_text(advice)
        
    elif (action == 3):
        # send action 104
        action_sender.publish_action(104)
        # say this
        advice += "You can do a standing lower back stretch. . . Look at me how I am doing it."
        text_to_speech_publisher.publish_text(advice)

    elif (action == 4):
        # send action 105
        action_sender.publish_action(105)
        # say this
        advice += "Try to stand on one leg, raise your other leg to the back, then use your arm to hold your extended leg for 5 seconds. "
        text_to_speech_publisher.publish_text(advice)
    elif (action == 5):
        # send action 106
        action_sender.publish_action(106)
        # say this
        advice += "Try to make your elbows 90 angle, then pull your arms to the back. . . Do it 10 times."
        text_to_speech_publisher.publish_text(advice)
    elif (action == 6):
        # send action 107
        action_sender.publish_action(107)
        # say this
        advice += "Try to make your elbows 90 angle, then extend your arms to the sides. . . Do it 10 times."
        text_to_speech_publisher.publish_text(advice)


    elif (action == 7):
        # say this
        advice += "You could try and walk around for a few minutes. . . This could help reduce your pain"
        text_to_speech_publisher.publish_text(advice)


    elif (action == 8):
        # say this
        advice += "Please make sure that your knee is well extended. . . It should have an angle a little wider than 90 degrees."
        text_to_speech_publisher.publish_text(advice)


    elif (action == 9):
        # say this
        advice += "Using your other arm. . . Extend your arm downwards for a few seconds. . . This could reduce your pain."
        text_to_speech_publisher.publish_text(advice)


    elif (action == 10):
        # say this
        advice += "Try to side bend your head to the left and right. . . Do it 3 times for each side."
        text_to_speech_publisher.publish_text(advice)


    elif (action == 11):
        # say this
        advice = "I'm sorry my advice didn't help. . . If your pain continues, it's a good idea to see a doctor."
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
        
    print_state(state)



    while True:

        action = np.argmax(q_table[state,:])
        # perform the action

        print_action(action)
        perform_action(action)
        if (action == 11):
            break
        # ask user if satisfied, if yes, go to state 0 and exit the program
        satisfied = input("are you satisfied?")
        if (satisfied == "yes"):
            break
        else:
            q_table[state,action] = 0
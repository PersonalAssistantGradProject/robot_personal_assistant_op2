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
    print_state(state)

    while True:

        action = np.argmax(q_table[state,:])
        # perform the action

        print_action(action)
        if (action == 11):
            break
        # ask user if satisfied, if yes, go to state 0 and exit the program
        satisfied = input("are you satisfied?")
        if (satisfied == "yes"):
            break
        else:
            q_table[state,action] = 0
#!/usr/bin/env python

"""
This Python file implements a reinforcement learning algorithm known as Q-learning to train
an agent to provide optimal recommendations for specific pain types. The output of the
program is a Q-table, which serves as a trained model.

This Q-table is later utilized by another Python file, which makes use of the trained model
to select the most suitable advice for a given scenario.


The Q-table consists of 8 states (rows) and 12 actions (columns):

- States:
State 0: no pain
State 1: neck pain + bad posture
State 2: neck pain
State 3: back pain + bad posture
State 4: back pain
State 5: leg pain
State 6: arm pain
State 7: shoulder pain


- Actions:
Action 0: neck_1
Action 1: neck_2
Action 2: arm_1
Action 3: back_1
Action 4: leg_1
Action 5: back_2
Action 6: arm_2
Action 7: walk
Action 8: extend knee
Action 9: extend palm
Action 10: side bending
Action 11: see a doctor


"""


# included libraries
import numpy as np
import gym
from gym import spaces
import random


# The "training_agent" function serves to train the Q-learning agent by simulating human
# responses to all action recommendations provided by the agent.
# The simulation employs a simplified approach that mainly uses chances and randomization.
def training_agent(state,action):

    # State 1: neck pain + bad posture
    if (state == 1):
        if action in (0,1,10):
            if random.random() < 0.95:
                return "yes"
        if (action == 7): 
            if random.random() < 0.55:
                return "yes"
        if (action == 11): 
            if random.random() < 0.15:
                return "yes"
    
    # State 2: neck pain
    elif (state == 2):
        if action in (0,1,10):
            if random.random() < 0.95:
                return "yes"
        if (action == 11): 
            if random.random() < 0.15:
                return "yes"

    # State 3: back pain + bad posture 
    elif (state == 3):
        if (action == 3):
            if random.random() < 0.95:
                return "yes"
        if (action == 5):
            if random.random() < 0.75:
                return "yes"
        if (action == 2):
            if random.random() < 0.65:
                return "yes"
        if (action == 7):
            if random.random() < 0.55:
                return "yes"
        if (action == 11): 
            if random.random() < 0.15:
                return "yes"
    
    # State 4: back pain        
    elif (state == 4):
        if (action == 3):
            if random.random() < 0.95:
                return "yes"
        if (action == 2):
            if random.random() < 0.65:
                return "yes"   
        if (action == 5):
            if random.random() < 0.75:
                return "yes"
        if (action == 11): 
            if random.random() < 0.15:
                return "yes"
        
    # State 5: leg pain       
    elif (state == 5):
        if action in (4,7):
            if random.random() < 0.95:
                return "yes"
        if (action == 3):
            if random.random() < 0.65:
                return "yes"
        if (action == 8):
            if random.random() < 0.85:
                return "yes"
        if (action == 11): 
            if random.random() < 0.15:
                return "yes"

    # State 6: arm pain       
    elif (state == 6):
        if action in (2,6,9):
            if random.random() < 0.95:
                return "yes"
        if (action == 5):
            if random.random() < 0.65:
                return "yes"
        if (action == 11): 
            if random.random() < 0.15:
                return "yes"

    # State 7: shoulder pain    
    else:
        if action in (5,10):
            if random.random() < 0.95:
                return "yes"
        if (action == 2):
            if random.random() < 0.75:
                return "yes"
        if (action == 6):
            if random.random() < 0.65:
                return "yes"
        if (action == 11): 
            if random.random() < 0.15:
                return "yes"
    

    # return "no" if no chance were successful
    return "no"
    


# The "CustomEnv" class defines a customized environment for our Q-learning algorithm, 
# specifically with 8 states and 12 actions. These specifications determine the size
# of our Q-table. Additionally, the class features customized reset and step functions.
class CustomEnv(gym.Env):

    def __init__(self):
        self.action_space = spaces.Discrete(12) # 12 actions: 0-11
        self.observation_space = spaces.Discrete(8) # 8 states: 0-7
        self.state = 0 # initial state


    def reset(self):
        self.state = random.randint(1,7) # reset to random state from 1 to 7
        return self.state


    def step(self, action):
        
        # the "training_agent" simulation function evaluates step taken by
        # the agent and determines whether the user is satisfied with the
        # action taken in a given state or not.
        satisfied = training_agent(state,action)
        if (satisfied == "yes"):
            # go to state 0, give a reward of 1, and mark the episode as done.
            self.state = 0
            reward = 1
            done = True
        else:
            # give no reward, and continue to the next step of the episode.
            reward = 0
            done = False


        return self.state, reward, done



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







# create a "CustomEnv" object
env = CustomEnv()


# construct Q-table
action_space_size = env.action_space.n
state_space_size = env.observation_space.n
q_table = np.zeros((state_space_size, action_space_size))
print("\n\n----- Initialized Q-table -----\n")
print(q_table)


# initialize parameters
num_episodes=100000
max_steps_per_episode= 12  # Max number of steps per episode before it terminates
learning_rate=0.1          # Learning rate (alpha)
discount_rate=0.05         # Discount rate (gamma)


# epsilon-greedy algorithm parameters
exploration_rate=1             # Exploration rate (epsilon)
max_exploration_rate=1         # Max epsilon
min_exploration_rate=0.01      # Min epsilon
exploration_decay_rate=0.00008 # Rate of epsilon decay

 

# Q-learning Algorithm
for episode in range (num_episodes):

    # Reset Env to random state from 1-7
    state=env.reset()
    done=False

    # In order to prevent the agent from repeating the same action within the
    # same episode, we have declared the unused_actions list and copy_of_q_table.
    # This ensures that each of the maximum 12 steps per episode will have a unique action.
    unused_actions = list(range(12))
    copy_of_q_table = q_table.copy()

    # print functions used for testing.
    #print ("\n\n---------- Episode number =",episode,"----------")
    #print_state(state)

    for step in range (max_steps_per_episode):
        
        # To select an action for the current step, we begin by generating a random 
        # number between 0 and 1. If this number exceeds the  value of epsilon we adopt 
        # an exploitation strategy and select the action with the highest Q value for 
        # the current state. However,  if the randomized number falls within the range 
        # of epsilon, we follow an exploration strategy and select a completely random action.

        exploration_rate_threshold = random.uniform(0,1)
        if exploration_rate_threshold > exploration_rate:
            # Exploit: choose action based on Q-table values.
            action = np.argmax(copy_of_q_table[state,:])
        else:
            # Explore: choose a random action.
            action = random.choice(unused_actions)


        # Make sure that the action does not get repeated in the same episode.
        copy_of_q_table[state, action] = -1
        unused_actions.remove(action)
        
        


        # Take the action and observe the outcome state and reward.
        new_state, reward, done = env.step(action)

        # print functions used for testing.
        #print(" ")
        #print_action(action)
        #print("reward =", reward)


        # update Q-table for Q(s,a)
        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]1
        # qtable[new_state,:] : all the actions we can take from new state.
        q_table[state,action]=q_table[state,action] * (1-learning_rate) + \
            learning_rate *(reward+ discount_rate*np.max(q_table[new_state,:]))
        
        # update state
        state = new_state

        # finish episode if it was marked as done
        if done==True:
            break

    # Exploration rate decay after every episode
    exploration_rate= min_exploration_rate + \
                      (max_exploration_rate-min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
    

    # print functions used for testing.
    #print("\n\nepisode ", episode," finished!")
    #print("exploration_rate =",exploration_rate)
    #print("\n\n *************Q-table ***************\n")
    #print(q_table)



# print updated Q-table
np.set_printoptions(precision=3)
print("\n\n----- Finalized Q-table -----\n")
print(q_table)
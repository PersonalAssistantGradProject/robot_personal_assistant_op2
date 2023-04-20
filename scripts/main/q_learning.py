#!/usr/bin/env python

import numpy as np
import gym
from gym import spaces
import random


def training_agent(state,action):
    if (state == 1):
        if action in (0,1,10):
            if random.random() < 0.95:
                return "yes"
        if (action == 7): 
            if random.random() < 0.55:
                return "yes"
            
    elif (state == 2):
        if action in (0,1,10):
            if random.random() < 0.95:
                return "yes"
        if (action == 11): 
            if random.random() < 0.15:
                return "yes"
            
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
            
    elif (state == 6):
        if action in (2,6,9):
            if random.random() < 0.95:
                return "yes"
        if (action == 5):
            if random.random() < 0.65:
                return "yes"
        
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
    
    return "no"
    




class CustomEnv(gym.Env):

    def __init__(self):
        self.action_space = spaces.Discrete(12) # 12 actions: 0-11
        self.observation_space = spaces.Discrete(8) # 8 states: 0-7
        self.state = 0 # initial state


    def reset(self):
        self.state = random.randint(1,7) # reset to random state from 1 to 7
        return self.state


    def step(self, action):
        '''
        if action == 0:

        elif action == 1:



        elif action == 2:
            
            
        elif action == 3:


        elif action == 4:


        elif action == 5:


        elif action == 6:


        elif action == 7:


        elif action == 8:


        elif action == 9:


        elif action == 10:

        else:
        '''
        #satisfied = input("Are you satisfied with what i recommeneded?")
        satisfied = training_agent(state,action)
        if (satisfied == "yes"):
            # go to state 0, and give reward, and done = True
            self.state = 0
            reward = 1
            done = True
        else:
            reward = 0
            done = False


        return self.state, reward, done


# function to print state number and name (every episode)
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


# function to print action number and name (every step)
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





env = CustomEnv()



#Construct Q-table
action_space_size= env.action_space.n
state_space_size= env.observation_space.n
q_table= np.zeros ((state_space_size, action_space_size))
print(q_table)


#Initialize Parameters
num_episodes=100000
max_steps_per_episode= 12  # Max number of steps per episode before it terminates
learning_rate=0.1         # Learning rate (alpha)
discount_rate=0.05       # Discount rate (gamma)


#epsilon-greedy algorithm
exploration_rate=1           # epsilon= exploration rate
max_exploration_rate=1       # Max epsilon
min_exploration_rate=0.01    # Min epsilon
exploration_decay_rate=0.00008 # rate of epsilon decay

 

#Q learning Algorithm
for episode in range (num_episodes):
    #print ("\n\n---------- Episode number =",episode,"----------")
    # Reset Env to random state from 1-7
    state=env.reset()
    #print_state(state)
    done=False
    unused_actions = list(range(12))
    copy_of_q_table = q_table.copy()

    for step in range (max_steps_per_episode):
        
        # Choose an action a in the current world state (s)
        ## First we randomize a number
        ## If this number > greater than epsilon
        #            --> exploitation (taking the biggest Q value for this state)
        # Else doing a random choice --> exploration
        exploration_rate_threshold= random.uniform(0,1)
        if exploration_rate_threshold > exploration_rate:
            # exploit (get action based on q_table values)
            action = np.argmax(copy_of_q_table[state,:])
        else:
            # explore (get random action)
            action = random.choice(unused_actions)


        # make sure that the action does not get repeated in the same episode
        copy_of_q_table[state, action] = -1
        unused_actions.remove(action)
        
        #print(" ")
        #print_action(action)

        # Take the action (a) and observe the outcome state(s') and reward (r)
        new_state, reward, done = env.step(action)
        #print("reward =", reward)
        #update Q-table for Q(s,a)

        # Update Q(s,a):= Q(s,a) + lr [R(s,a) + gamma * max Q(s',a') - Q(s,a)]1
        # qtable[new_state,:] : all the actions we can take from new state
        q_table[state,action]=q_table[state,action] * (1-learning_rate) + \
            learning_rate *(reward+ discount_rate*np.max(q_table[new_state,:]))

        state = new_state
        if done==True:
            break
    # Exploration rate decay
    exploration_rate= min_exploration_rate + \
                      (max_exploration_rate-min_exploration_rate) * np.exp(-exploration_decay_rate*episode)
    
    #print("\n\nepisode ", episode," finished!")
    #print("exploration_rate =",exploration_rate)
    #print("\n\n *************Q-table ***************\n")
    #print(q_table)


np.set_printoptions(precision=3)
#print update Q-table
print("\n\n *************Q-table ***************\n")
print(q_table)

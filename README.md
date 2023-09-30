# Building an Interactive and Intelligent system Using Darwin OP2 Humanoid Robot
---
# Introduction

This project focused on utilizing the Darwin OP2 robot to create an immersive and interactive personal assistant system that relies on audio and visual data. It includes Reinforcement learning-based medical advice, Face recognition, Speech recognition, Text-tospeech conversion, Web scraping.


##### Objectives:
- Personal assistant for individuals who stay on their desks for long periods of time.
- Help alleviate desk-ergonomics related pains, such as neck and back pain, using both physical and verbal advice.
- Support various productivity-boosting tasks like online searches and capturing voice notes.

##### Implementation:
- Hardware: Darwin OP2 Humanoid Robot, PC for computing the output.
- Software: Linux, Python, Robot Operating System (ROS), OpenCV, gTTS.

##### Processing Steps:
1. Darwin captures user’s data using its built-in microphone and webcam. Then the usre data is sent to a processing computer.
2. The processing computer computes the suitable output for the given user data and status. Then sends this output back to Darwin.
3. Darwin provides the user with the output using verbal and phyiscal channels.


##### Outcome:
Darwin functions as a robotic personal assistant, using the power of reinforcement learning to provide medical advice. Additionally, it possesses the capability to fetch web-based information, record and replay your voice, issue alerts when your posture is suboptimal, and provide you with the current time, date, and even a touch of humor.

Check out the [Demo Video].

For more information about this project, please refer to its [documentation].

---
# Team Members
##### Students:

- **Omar Barham** - Computer Engineering - ombarham@gmail.com
- **Mohammad Khader** - Computer Engineering -  mohammedkhader864@gmail.com
- **Ahmad Al-Najjar** -  - ahmadimnajjar@gmail.com

##### Advisors:

- **Dr. Khalil Yousef** - Associate Professor of Computer Engineering - khalil@hu.edu.jo
- **Prof. Bassam Jamil** - Computer Engineering Professor - bassam@hu.edu.jo

Please feel free to contact any of the members via email.

---
# Requirements

##### PC Side:
- Ubuntu 20.04 LTS (Focal Fossa)
- ROS Noetic Ninjemys
- Python 3.8.10
- For python libraries, please check requirements_pc.txt

##### Darwin Side:
- Linux Mint 17.3 "Rosa"
- ROS Indigo Igloo
- Python 2.7.6
- For python libraries, please check requirements_darwin.txt

##### Other Requirements:
- Stable internet connection with fast internetwork communication (aka external router).

Please note that the above versions are the one we used and are 100% working, other versions may or may not cause problems while running the project.

---
# Running the Project

##### Part 1:
1. Start Darwin and the PC.
2. Darwin will then open a wifi network called "ROBOTIS-OP2_SHARE", you should connect to it using the PC.
3. Using [UltraVNC], connect to Darwin's GUI (Darwin will have an IP of 10.42.0.1).
4. Connect Darwin to a monitor using its mini HDMI output. Since we're connected to the GUI using UltraVNC, now we can choose to display only the secondary monitor that we just connected.
5. Plug in a mouse and a keyboard into darwin.


After completing part 1, you will have full access to Darwin without relying on a VNC connection.
##### Part 2:
1. Connect both Darwin and the PC to the same router.
2. Open a new terminal on Darwin side.
3. Use ```ifconfig``` to find the IP address of Darwin.
4. use the command ```cd``` to make sure you're in the home directory.
5. use the command ```gedit ~/.baschrc```, and make sure you have the following lines in it:
    ```sh
    export ROS_MASTER_URI=http://"ROBOT_IP":11311
    export ROS_HOSTNAME="ROBOT_IP"
    ```
6. Open a new terminal on PC side.
7. Use ```ifconfig``` to find the IP address of the PC.
8. use the command ```cd``` to make sure you're in the home directory.
9. use the command ```gedit ~/.baschrc```, and make sure you have the following lines in it:
    ```sh
    export ROS_MASTER_URI=http://"ROBOT_IP":11311
    export ROS_HOSTNAME="PC_IP"
    ```
10. Close the terminals on both Darwin and PC.

##### Part 3:
Do the following steps for both sides (Darwin and PC):
1. Go into your ROS workspace, we'll assume it' s named "catkin_ws", use the command ```cd catkin_ws\src\```
2. Make sure you have the latest version of this repository, use the command ```git clone https://github.com/PersonalAssistantGradProject/robot_personal_assistant_op2```
3. Make sure that all files are excutable within the repository's folder.

##### Part 4:
1. On Darwin side, change the IP address in the file "audio_sender.py" to the IP address of the PC.
2. On Darwin side, use the command ```roslaunch robot_personal_assistant_op2 robot.launch```, wait for Darwin to stand up and sit down. After a minute or so, a statement will be printed on the terminal saying that Darwin is ready.
3. On the PC side, use the command ```roslaunch robot_personal_assistant_op2 laptop.launch```, wait a few seconds and the system should be ready to use.

---
# Other Notes
The purpose of documenting this project is to help people who would work on the same project in the future. by documenting all of our steps, we hope to give them the information they need to continue working on this project. It is also our intent to inspire people who would work on similar projects, all of our code is open source with most parts of it being documented. We believe that going through our codes and documentations could influence those who have intersts in such projects.

##### Open-Source Code used in this project:
- [Body Posture Detection]

##### Other Useful Links:
- [ROS Wiki]
- [ROBOTIS Darwin OP2 e-Manual]

---
# Future Work
Future plans for this project incude:
1. Adding more medical advice.
2. Using Deep Q-Learning (DQN) instead of Q-Learning.
3. Task scheduling and organization.
4. Adding more custom actions and body language.
5. Robot to medical facility communication.
6. Enhance system security.
7. Exploring design alternatives.
8. Overall optimization and bug-fixing.

[//]: #
   [Demo Video]: <https://youtu.be/yJ2NVAMxFx4>
   [documentation]: <https://github.com/PersonalAssistantGradProject/robot_personal_assistant_op2/blob/main/Project%20Documentation.pdf>
   [Body Posture Detection]: <https://learnopencv.com/building-a-body-posture-analysis-system-using-mediapipe/>
   [ROS Wiki]: <https://wiki.ros.org/>
   [ROBOTIS Darwin OP2 e-Manual]: <https://emanual.robotis.com/docs/en/platform/op2/getting_started/>
   [UltraVNC]: <https://uvnc.com/>
   

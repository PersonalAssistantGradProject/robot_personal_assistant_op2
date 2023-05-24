#!/bin/bash
cd
cd catkin_ws/src/robot_personal_assistant_op2/scripts/main/
python image_publisher.py
python3.9 audio_sender.py &
python3.9 audio_note_player.py &
python3.9 text_to_speech_subscriber.py &
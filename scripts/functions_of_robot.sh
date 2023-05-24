#!/usr/bin/bash

roscd robot_personal_assistant_op2/
cd scripts/main/
python3.9 audio_sender.py
python3.9 audio_note_player.py
python3.9 text_to_speech_subscriber.py
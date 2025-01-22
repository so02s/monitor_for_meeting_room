#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/user/.Xauthority

source /home/monitor/monitor_for_meeting_room/.venv/bin/activate
pip install -r /home/monitor/monitor_for_meeting_room/requirements.txt
deactivate

# НЕ ЗАБЫТЬ - ПРИ ЗАПУСКЕ СКРИПТА ДОЛЖНЫ БЫТЬ ПРАВА SUDO
sudo /home/monitor/monitor_for_meeting_room/.venv/bin/python3 /home/monitor/monitor_for_meeting_room/main.py
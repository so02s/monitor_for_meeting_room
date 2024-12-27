#!/bin/bash

export DISPLAY=:0
export XAUTHORITY=/home/user/.Xauthority
#xhost +local:

sudo .venv/bin/python3 main.py
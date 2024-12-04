#!/bin/bash

export DISPLAY=:0
xhost +local:

sudo .venv/bin/python3 main.py
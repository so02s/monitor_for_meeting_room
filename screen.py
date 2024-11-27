import os
import time

os.environ['DISPLAY'] = ':0'

def turn_off_screen():
    os.system("xset dpms force off")

def turn_on_screen():
    os.system("xset dpms force on")

# Example usage
turn_off_screen()
time.sleep(5)  # Wait for 5 seconds before turning the screen back on
turn_on_screen()
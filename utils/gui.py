import os
import time
import subprocess
from pug4py.pug import Pug

# Генерирование веб страничек

# TODO открывание страничек после генерации
async def change_image(occupied: dict, schedule, room_name: str) -> None:
    pug = Pug("pug")
    if occupied:
        rendered_html = pug.render("./pug/occupied.pug", occupied=occupied, room_name=room_name)
    else:
        rendered_html = pug.render("./pug/nobody.pug", schedule=schedule, room_name=room_name)
    with open("./pug/index.html", "w") as f:
        f.write(rendered_html)

async def static_image() -> None:
    pug = Pug("pug")
    rendered_html = pug.render("./pug/static.pug")
    
    with open("./pug/index.html", "w") as f:
        f.write(rendered_html)


# Работа с дисплеем

os.environ['DISPLAY'] = ':0'

def turn_off_screen():
    os.system("xset dpms force off")

def turn_on_screen():
    os.system("xset dpms force on")


def set_brightness(brightness):
    try:
        subprocess.run(['xrandr', '--output', 'HDMI-1', '--brightness', str(brightness)], check=True)
    except subprocess.CalledProcessError as e:
        pass

def turn_on_hdmi(duration=1, steps = 50):
    for i in range(steps + 1):
        brightness = 1 - (i / steps)
        set_brightness(brightness)
        time.sleep(duration / steps)

def turn_off_hdmi(duration=5, steps = 100):
    for i in range(steps + 1):
        brightness = i / steps
        set_brightness(brightness)
        time.sleep(duration / steps)
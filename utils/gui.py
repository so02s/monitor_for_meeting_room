import os
import time
import subprocess
from datetime import datetime
import webbrowser

from jinja2 import Template
from pathlib import Path

# Генерирование веб страничек

async def change_image(occupied: dict, schedule, path: Path):
    # определение стиля
    mode = "light" if datetime.now().hour < 12 else "dark"
    occup = "occupied" if occupied else "free"
    dist_path = path / mode / occup

    # Рендер html странички
    tmp = Template(open(dist_path / "index.html").read())
    html = tmp.render(slots=schedule)

    # запись в файл
    with open(dist_path / "temp.html", "w") as f:
        f.write(html)

    # открытие странички
    # TODO до этого нужно закрывать прошлую
    # webbrowser.register('vivaldi', None, webbrowser.BackgroundBrowser('/usr/bin/vivaldi'))
    # webbrowser.get('vivaldi').open(dist_path.as_posix() + "/temp.html")
    webbrowser.open(dist_path.as_posix() + "/temp.html")

async def static_image(path: Path):
    # определение стиля
    mode = "light" if datetime.now().hour < 12 else "dark"
    dist_path = path / mode / "error"

    # рендер
    tmp = Template(open(dist_path / "index.html").read())
    html = tmp.render()

    # запись в файл
    with open(dist_path / "temp.html", "w") as f:
        f.write(html)
    
    webbrowser.open(dist_path.as_posix() + "/temp.html")
    

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
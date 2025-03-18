import os
import time
import subprocess
from datetime import datetime, timedelta
import webbrowser
import pyautogui

from jinja2 import Template
from pathlib import Path

# Генерирование веб страничек

async def change_image(occupied: dict, schedule: list, path: Path):
    # определение стиля
    mode = "light" if not datetime.now().hour < 12 else "dark"
    occup = "occupied" if occupied else "free"
    dist_path = path / mode / occup

    now = datetime.now()
    time_str = now.strftime("%H:%M")

    schedule = [
        record for record in schedule 
        if not record['end_time'] <= time_str
    ]

    tmp = Template(open(dist_path / "index.html").read())

    if occupied:
        for i in range(len(schedule)):
            if i == 0:
                if datetime.strptime(schedule[i]['start_time'], "%H:%M") > datetime.strptime(time_str, "%H:%M"):
                    free_slot = f"{time_str} - {schedule[i]['start_time']}"
                    break
            else:
                if datetime.strptime(schedule[i]['start_time'], "%H:%M") > datetime.strptime(schedule[i-1]['end_time'], "%H:%M"):
                    free_slot = f"{schedule[i-1]['end_time']} - {schedule[i]['start_time']}"
                    break
        else:
            free_slot = f"{schedule[-1]['end_time']} - {datetime.strptime(schedule[-1]['end_time'], '%H:%M') + timedelta(hours=1):%H:%M}"

        html = tmp.render(occupied=occupied, free=free_slot)
    else:
        schedule = schedule[:3]
        html = tmp.render(slots=schedule)

    # запись в файл
    with open(dist_path / "temp.html", "w") as f:
        f.write(html)

    # открытие странички
    # pyautogui.hotkey('ctrl', 'w')
    falcon_path = '/usr/bin/falkon'
    subprocess.run([falcon_path, '--no-sandbox', "10.23.43.2"]) # dist_path.as_posix() + "/temp.html"])
    # webbrowser.register('falkon', None, webbrowser.BackgroundBrowser('/usr/bin/falkon'))
    # webbrowser.get('falkon').open(dist_path.as_posix() + "/temp.html")
    # webbrowser.open(dist_path.as_posix() + "/temp.html")



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
    
    # pyautogui.hotkey('ctrl', 'w')
    # webbrowser.open(dist_path.as_posix() + "/temp.html")
    falcon_path = '/usr/bin/falkon'
    subprocess.run([falcon_path, '--no-sandbox', "10.23.43.2"]) 


# Работа с дисплеем

os.environ['DISPLAY'] = ':0'

# def turn_off_screen():
#     os.system("xset dpms force off")

# def turn_on_screen():
#     os.system("xset dpms force on")


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

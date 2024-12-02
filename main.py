import time
import board
import subprocess
import threading
import neopixel
import threading
from radar import radar, extract_distances

'''
Что должен делать?

1. Когда поблизости никого нет - зажигать красный/зеленый в зависимости от того, занята ли переговорка или нет
2. Когда есть кто-то - показывать:
    - Если занята - то кем и до скольки
    - Если свободна - то когда ближайшая запись

'''

# Проверка радаром значений постоянная - маленькое расстояние - на 1 мин включается дисплей

# Проверка расписания на день конкретной переговорки - раз в сутки? Чаще? Надо поговорить

# export DISPLAY=:0
# xrandr --output HDMI-1 --brightness 1
# xrandr --output HDMI-1 --brightness 0



# =============================== Радар ===================================

def set_brightness(brightness):
    try:
        subprocess.run(['xrandr', '--output', 'HDMI-1', '--brightness', str(brightness)], check=True)
    except subprocess.CalledProcessError as e:
        pass

def turn_on_hdmi(duration=2):
    steps = 100
    for i in range(steps + 1):
        brightness = 1 - (i / steps)
        set_brightness(brightness)
        time.sleep(duration / steps)

def turn_off_hdmi(duration=5):
    steps = 100
    for i in range(steps + 1):
        brightness = i / steps
        set_brightness(brightness)
        time.sleep(duration / steps)

class DisplayTimer:
    def __init__(self):
        self.timer = None
        self.active = False

    def start(self):
        if not self.active:
            self.active = True
            self.timer = threading.Timer(60, self.turn_off)
            self.timer.start()
            turn_on_hdmi()

    def reset(self):
        if self.active:
            self.timer.cancel()
            self.timer = threading.Timer(60, self.turn_off)
            self.timer.start()

    def turn_off(self):
        self.active = False
        turn_off_hdmi()
        
        
radar.start()
display_timer = DisplayTimer()

try:
    while True:
        distance = extract_distances(radar.get_data())
        if distance[0] < 120 or distance[1] < 120:
            display_timer.start()
            display_timer.reset()
        else:
            if display_timer.active:
                display_timer.turn_off()  # Отключаем дисплей, если человек ушел
except KeyboardInterrupt:
    if display_timer.active:
        display_timer.turn_off()  # Убедитесь, что дисплей отключен при выходе
        radar.stop()















# Ниже - проверка разного функционала устройства


# # Настройки
# LED_COUNT = 4
# LED_PIN = board.D12
# # Создание объекта для управления светодиодами
# pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT)

# # Функция для установки цвета
# def set_color(color):
#     pixels.fill(color)

# while(True):
#     distance = extract_distances(radar.get_data())
#     print(*distance)
#     if distance[0] < 120 or distance[1] < 120:
#         set_color((0, 255, 0))
#         # time.sleep(5)
#     else:
#         set_color((255, 0, 0))
#     time.sleep(0.05)

# # Основной цикл
# try:
#     while True:
#         set_color((255, 0, 0))  # Красный
#         time.sleep(1)
#         set_color((0, 255, 0))  # Зеленый
#         time.sleep(1)
#         set_color((0, 0, 255))  # Синий
#         time.sleep(1)
#         set_color((255, 255, 255))  # Белый
#         time.sleep(1)
#         set_color((0, 0, 0))  # Выключить
#         time.sleep(1)

# except KeyboardInterrupt:
#     # Выключить светодиоды при завершении программы
#     pixels.fill((0, 0, 0))
import asyncio
import threading
import logging

import board
import neopixel

import LD2410
import time

# import os
# import subprocess

'''
Что должен делать?

1. Когда поблизости никого нет - зажигать красный/зеленый в зависимости от того, занята ли переговорка или нет
2. Когда есть кто-то - показывать:
    - Если занята - то кем и до скольки
    - Если свободна - то когда ближайшая запись

'''

# =============================== Обновление расписания ===================================

# Функция для установки цвета
def set_color(color):
    pixels.fill(color)


async def check_schedule():
    '''
        Функция, отвечающая за расписание, подсветку индикатора и отображаемую картинку
    '''
    
    # Настройки светодиодов
    LED_COUNT = 4
    LED_PIN = board.D12
    # Создание объекта для управления светодиодами
    pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT)
    
    
    while True:
        # тыкнуть бота на JSON
        # изменить занятость (красный/зеленый индикатор)
        # изменить картинку для вывода на экран
        await asyncio.sleep(3)  # 15 минут = 15 * 60


# =============================== Подсветка монитора ===================================

class ResettableTimer:
    def __init__(self, time, function, args=None, kwargs=None):
        self._time = time
        self._function = function
        self._args = args if args is not None else []
        self._kwargs = kwargs if kwargs is not None else {}
        self._timer = None
        self._running = False

    def _set(self):
        self._timer = threading.Timer(
            self._time,
            self._function,
            self._args,
            self._kwargs)

    def start(self):
        if not self._running:
            self._running = True
            self._set()  # Создаем новый таймер
            self._timer.start()

    def cancel(self):
        self._running = False
        if self._timer is not None:
            self._timer.cancel()

    def reset(self, start=False):
        self.cancel()  # Останавливаем текущий таймер
        self._set()    # Создаем новый таймер

        if self._running or start:
            self.start()  # Запускаем новый таймер


def turn_on_hdmi(duration=1, steps = 50):
    global on
    on = True
    print("Turn on")
    # for i in range(steps + 1):
    #     brightness = 1 - (i / steps)
    #     set_brightness(brightness)
    #     time.sleep(duration / steps)

def turn_off_hdmi(duration=5, steps = 100):
    global on
    on = False
    print("Turn off")
    # for i in range(steps + 1):
    #     brightness = i / steps
    #     set_brightness(brightness)
    #     time.sleep(duration / steps)

def get_data(data):
    """
    Извлекает расстояния до движущейся и статической цели из данных LD2410.

    :param data: Список, возвращаемый функцией get_data_frame()
    :return: Кортеж с расстоянием до движущейся и статической цели
    """
    data = data[0]
    
    if len(data) < 6:
        raise ValueError("Недостаточно данных для извлечения расстояний.")

    movement_distance = data[1]

    return movement_distance


def set_brightness(brightness):
    try:
        subprocess.run(['xrandr', '--output', 'HDMI-1', '--brightness', str(brightness)], check=True)
    except subprocess.CalledProcessError as e:
        pass


async def check_radar():
    '''
        Функция, отвечающая за радар
    '''
    # инициализация + отключение DEBUG
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger('LD2410')
    logger.setLevel(logging.WARNING)
    logging.getLogger().setLevel(logging.WARNING)
    
    radar = LD2410.LD2410(port="/dev/ttyAMA0")
    radar.start()
    
    global on
    on = False
    
    timer = ResettableTimer(15, turn_off_hdmi)
    
    while True:
        data = get_data(radar.get_data())
        
        if data <= 120:
            if not on:
                turn_on_hdmi()
                timer.start()
            else:
                print("reset")
                timer.reset()
        
        await asyncio.sleep(0.5)


# =========================== Основный цикл =========================== 

async def main():
    schedule_task = asyncio.create_task(check_schedule())
    radar_task = asyncio.create_task(check_radar())

    await asyncio.gather(schedule_task, radar_task)

if __name__ == "__main__":
    asyncio.run(main())
















# def is_human_near(radar: Radar) -> bool:
#     distance = radar.get_data()
#     return distance[0] < 120 or distance[1] < 120

# radar = Radar()
# display_timer = DisplayTimer()

# Тут отдельный поток для проверки радара 

# try:
#     while True:
#         distance = radar.get_data()
#         if distance[0] < 120 or distance[1] < 120:
#             display_timer.start()
#             display_timer.reset()
#         else:
#             if display_timer.active:
#                 display_timer.turn_off()  # Отключаем дисплей, если человек ушел
# except KeyboardInterrupt:
#     if display_timer.active:
#         display_timer.turn_off()  # Убедитесь, что дисплей отключен при выходе
#         radar.stop()


# ===================== Расписание для переговорки =================


# Ниже - проверка разного функционала устройства




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



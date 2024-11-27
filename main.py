import time
import board
import neopixel
from radar import radar, extract_distances

# Настройки
LED_COUNT = 4
LED_PIN = board.D12
# Создание объекта для управления светодиодами
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT)

radar.start()

# Функция для установки цвета
def set_color(color):
    pixels.fill(color)

while(True):
    distance = extract_distances(radar.get_data())
    print(*distance)
    if distance[0] < 120 or distance[1] < 120:
        set_color((0, 255, 0))
        # time.sleep(5)
    else:
        set_color((255, 0, 0))
    time.sleep(0.05)

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
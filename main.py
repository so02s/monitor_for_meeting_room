import asyncio
import logging
import pathlib
from decouple import config

# import board
# import neopixel

import LD2410

from utils.request import fetch_data, fetch_data_test
from utils.json import parse_schedule
# from utils.pixel import change_color
from utils.gui import change_image, static_image, turn_off_hdmi, turn_on_hdmi
from utils.timer import ResettableTimer

'''
Что должен делать?

1. Когда поблизости никого нет - зажигать красный/зеленый в зависимости от того, занята ли переговорка или нет
2. Когда есть кто-то - показывать:
    - Если занята - то кем и до скольки
    - Если свободна - то когда ближайшая запись

'''


async def check_schedule():
    '''
        Функция, отвечающая за расписание, подсветку индикатора и отображаемую картинку
    '''
    url = config('URL')
    room = config('ROOM_NUMBER')

    base_dir = pathlib.Path('./sources') / config("DISPL")
    # room_name = config('ROOM_NAME')

    # LED_COUNT = 4
    # LED_PIN = board.D12
    # pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT)
    
    while True:
        try:
            response = await fetch_data_test(url, room)
        except:
            response = None

        if not response:
            await static_image(base_dir)
        else:
            try:
                occupied, schedule = parse_schedule(response)

                # await change_color(occupied, pixels)
                await change_image(occupied, schedule, base_dir)
            except:
                await static_image(base_dir)

        await asyncio.sleep(30) # 15 минут = 15 * 60 = 900

async def check_radar():
    '''
        Функция, отвечающая за радар и подсветку монитора
    '''

    # Инициализация радара и таймера
    logging.basicConfig(level=logging.WARNING)
    logger = logging.getLogger('LD2410')
    logger.setLevel(logging.WARNING)
    logging.getLogger().setLevel(logging.WARNING)

    radar = LD2410.LD2410(port="/dev/ttyAMA0")
    radar.start()
    
    timer = ResettableTimer(60, turn_off_hdmi, turn_on_hdmi)
    
    # Бесконечный цикл проверки радара
    while True:
        data = radar.get_data()
        
        if data <= 120:
            if not timer.is_running:
                timer.start()
            else:
                timer.reset()
        
        await asyncio.sleep(0.5)



async def main():
    schedule_task = asyncio.create_task(check_schedule())
    # radar_task = asyncio.create_task(check_radar())


    await asyncio.gather(
        schedule_task,
        # radar_task
    )

if __name__ == "__main__":
    asyncio.run(main())
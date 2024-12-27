# TODO просто не нужно. удалить после тестирования



import LD2410
import time
import logging

class Radar:
    def __init__(self):
        # Необходимо для отключения DEBUG
        logging.basicConfig(level=logging.WARNING)
        logger = logging.getLogger('LD2410')
        logger.setLevel(logging.WARNING)
        logging.getLogger().setLevel(logging.WARNING)
        
        self.radar = LD2410.LD2410(port="/dev/ttyAMA0")
        self.radar.start()
    
    def get_data(self):
        """
        Извлекает расстояния до движущейся и статической цели из данных LD2410.

        :param data: Список, возвращаемый функцией get_data_frame()
        :return: Кортеж с расстоянием до движущейся и статической цели
        """
        data = self.radar.get_data_frame()
        
        if len(data) < 6:
            raise ValueError("Недостаточно данных для извлечения расстояний.")

        movement_distance = data[1]
        static_distance = data[3]

        return movement_distance, static_distance

    def stop(self):
        self.radar.stop()




# Код на проверку на всякий случай. Следующая строка - команда для оболочки, чтобы очистить порт
# lsof /dev/ttyAMA0

# fw_version = radar.read_firmware_version()
# print(f"Firmware version: {fw_version}")

# # Запуск опроса радара
# radar.start()

# try:
#     while True:
#         data = radar.get_data()
#         if data:
#             print(f"Detected data: {data}")
#         time.sleep(1)  # Интервал опроса
# except KeyboardInterrupt:
#     print("Stopping radar polling...")
# finally:
#     radar.stop()

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

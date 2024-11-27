from  LD2410  import *
import time

radar = LD2410(port="/dev/ttyAMA0") # Replace <port> with your serial port. e.g "COM3" or "/dev/ttyS0" etc. 

radar.disable_engineering_mode()

def extract_distances(data):
    """
    Извлекает расстояния до движущейся и статической цели из данных LD2410.

    :param data: Список, возвращаемый функцией get_data_frame()
    :return: Кортеж с расстоянием до движущейся и статической цели
    """
    data = data[0]
    
    if len(data) < 6:
        raise ValueError("Недостаточно данных для извлечения расстояний.")

    movement_distance = data[1]
    static_distance = data[3]

    return movement_distance, static_distance
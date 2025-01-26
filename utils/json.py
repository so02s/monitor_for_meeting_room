import json
from datetime import datetime

def parse_schedule(response: str):
    try:
        data = json.loads(response)
    except json.JSONDecodeError:
        raise ValueError("Ошибка: Неверный формат JSON.")

    if not all(key in data for key in ["room", "date", "records"]):
        raise KeyError("Ошибка: Отсутствуют необходимые ключи в JSON (room, date, records).")

    records = data["records"]

    if not isinstance(records, list):
        raise TypeError("Ошибка: 'records' должен быть списком.")

    current_time = datetime.now().strftime("%H:%M")
    occupied = None
    
    # проверка занятости и форматирование
    for record in records:
        if not isinstance(record, dict):
            raise TypeError("Ошибка: Каждый элемент в 'records' должен быть словарем.")
        if "name" not in record or "time" not in record:
            raise KeyError("Ошибка: Каждый элемент в 'records' должен содержать ключи 'name' и 'time'.")

        time_range = record["time"].split('-')

        if len(time_range) != 2:
            raise ValueError(f"Ошибка: Неверный формат времени для записи {record}. Ожидается 'HH:MM-HH:MM'.")
        
        start_time, end_time = time_range
        
        try:
            f_start_dt = datetime.strptime(start_time, "%H:%M").strftime("%H:%M")
            f_end_dt = datetime.strptime(end_time, "%H:%M").strftime("%H:%M")
        except ValueError:
            raise ValueError(f"Ошибка: Неверный формат времени для записи {record}. Ожидается 'HH:MM'.")
        
        # Форматирование записей
        record["time"] = f"{f_start_dt}-{f_end_dt}"

        if not occupied and start_time <= current_time <= end_time:
            occupied = record
            
    records.sort(key=lambda x: x['time'])

    return occupied, records
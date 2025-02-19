import json
from datetime import datetime
from decouple import config

def valid_records(json_text: str) -> bool:
    """
    Проверяет response

    Args:
        json_text (str): JSON-текст для проверки.

    Returns:
        Валиден ли ответ
    """

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as e:
        print(f"Ошибка парсинга JSON: {e}")
        return False

    if not all(key in data for key in ["room", "date", "records"]):
        print("Недостаточно данных в JSON-тексте")
        return False
    
    today = datetime.today().strftime("%Y-%m-%d")
    if data["date"] != today:
        print("Дата в JSON-тексте не соответствует сегодняшней дате")
        return False

    # if data["room"] != config["ROOM_NUMBER"]:
    #     print("Номер комнаты в JSON-тексте не соответствует конфигурации")
    #     return False

    # if not isinstance(records, list):
    #     print("Ошибка: 'records' должен быть списком.")
    #     return False
    
    # TODO возможно, необходимо проверить отдельные записи

    return True


def parse_schedule(response: str):
    
    data = json.loads(response)
    records = data["records"]

    current_time = datetime.now().strftime("%H:%M")
    occupied = None
    
    for record in records:
        if not occupied and record["start_time"] <= current_time <= record["end_time"]:
            occupied = record
            
    records.sort(key=lambda x: x['start_time'])

    return occupied, records
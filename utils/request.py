import aiohttp, random
from datetime import datetime
from typing import Any, Dict, List

# TODO поменять на эту
async def fetch_data(url: str, room: str) -> Any:
    today_date = datetime.now().strftime("%Y-%m-%d")

    load = {
        "room": room,
        "date": today_date
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=load) as response:
                response.raise_for_status()
                data = await response.json()
                return data
    except:
        # TODO добавление в логи
        print ("Error")
        return None


# для тестирования
async def fetch_data_test(url: str, room: str) -> Dict[str, Any]:
    # return None
        # {
        #     "room": "1",
        #     "date": "2024-12-16",
        #     "records": []
        # },
        # {
        #     "room": "1",
        #     "date": "2024-12-16",
        #     "records": [
        #         {"name": "alice", "time": "14:00-15:00"}
        #     ]
        # },
        # {
        #     "room": "1",
        #     "date": "2024-12-16",
        #     "records": [
        #         {"name": "bob", "time": "8:00-9:00"},
        #         {"name": "charlie", "time": "12:00-13:00"},
        #         {"name": "dave", "time": "15:00-16:00"}
        #     ]
        # },
        # {
        #     "room": "1",
        #     "date": "2024-12-16",
        #     "records": [
        #         {"name": "invalid_user", "time": "not_a_time"}
        #     ]
        # },
        # {
        #     "room": "1",
        #     "date": "2024-12-16",
        #     "records": [
        #         {"time": "9:00-10:00"}  # Отсутствует поле "name"
        #     ]
        # },
        # None

    return '''
{
    "room": "1",
    "date": "2025-01-24",
    "records": [
        {"name": "sorencoa", "time": "9:00-10:00"},
        {"name": "john_doe", "time": "10:00-11:00"},
        {"name": "jane_smith", "time": "11:00-12:00"}
    ]
}
'''
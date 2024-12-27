# monitor_for_meeting_room
Скрипт и системные утилиты для мониторов переговорок на Raspberry Pi 3 B+

## Запуск

1. Создать окружение venv 
    - ```python3 -m venv <путь/до/окружения>```
2. Активировать окружение
    - ```source <путь/до/окружения>/bin/activate```
3. Скачать необходимые пакеты
    - ```pip install -r requirements.txt```
4. Настроить Raspberry!!!
    - ```sudo nano /boot/filmware/config.txt```
    - Добавить:
    - ```dtoverlay=disable-bt``` (отключение bluetooth) -> для работы /dev/ttyAMA0
    - Для круглого монитора:
    ```
    hdmi_group=2
    hdmi_mode=87
    hdmi_pixel_freq_limit=356000000
    hdmi_timings=1080 0 68 32 100 1080 0 12 4 16 0 0 0 60 0 85500000 0
    ```
    - ```sudo apt install libraspberrypi-bin``` -утилита для управления дисплеем
5. Выйти из окружения ```deactivate```
6. Дописать .env
    - Какая по номеру комната
7. Запустить скрипт ```sudo <путь/до/окружения>/bin/python3 main.py``` (сейчас скрипт работает только под правами рута)


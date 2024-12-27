import threading

# TODO добавить логи
class ResettableTimer:
    '''
    Класс, реализующий таймер.
    Может быть сброшен и запущен несколько раз снова.
    '''

    def __init__(self, interval, function_off, function_on):
        self.interval = interval
        self.function = function_off
        self.function_on = function_on
        self.timer = None
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.function_on()
            self.is_running = True
            self.timer = threading.Timer(self.interval, self._timeout)
            self.timer.start()
            # print(f"Таймер запущен на {self.interval} секунд.")

    def reset(self):
        if self.timer is not None:
            self.timer.cancel()
            self.is_running = False
            # print("Таймер сброшен.")
        self.start()

    def _timeout(self):
        self.is_running = False
        self.function_off()
        # print("Время вышло!")
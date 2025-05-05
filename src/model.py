import math
import random

from PyQt6.QtCore import QTime


class Model:
    def __init__(self):
        self._time = QTime.currentTime()

    def get_time(self) -> QTime:
        return self._time

    def get_round_time(self, mins_precision: int = 5):
        return self._round_down(self._time, mins_precision)

    def _round_down(self, time: QTime, mins_precision: int = 5):
        minute = math.floor(time.minute() / mins_precision) * mins_precision
        return QTime(time.hour(), minute)

    def set_time(self, time: QTime) -> None:
        self._time = time

    def generate_random_time(self, mins_precision: int = 5) -> QTime:
        hour = random.randint(1, 12)
        minute = round(random.randint(0, 59))
        time = QTime(hour, minute)
        return self._round_down(time, mins_precision)

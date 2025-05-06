from dataclasses import dataclass
import math
import random

from PyQt6.QtCore import QTime


class Model:
    def __init__(self):
        self._time = QTime.currentTime()
        self.settings = Settings()

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


@dataclass
class NumberSetting:
    value: int


@dataclass
class CheckBoxSetting:
    checked: bool


class Settings:
    def __init__(self):
        self.show_minute_marks = CheckBoxSetting(True)
        self.show_hour_marks = CheckBoxSetting(True)
        self.hours_text_interval = NumberSetting(1)
        self.minutes_text_interval = NumberSetting(5)
        self.round_minutes_to_nearest = NumberSetting(5)

import sys
import math
import random

from PyQt6.QtCore import Qt, QTime, QPoint
from PyQt6.QtGui import QColor, QFont, QPainter, QPolygon
from PyQt6.QtWidgets import (
    QApplication,
    QLabel,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class AnalogClock(QWidget):
    def __init__(self, time: QTime, parent=None):
        super().__init__(parent)
        self._time = time
        self._set_colors()

    def set_time(self, time: QTime):
        self._time = time

    def _set_colors(self):
        self._hour_numbers_color = QColor("red")
        self._hour_hand_color = QColor("red")

        self._minute_numbers_color = QColor("teal")
        self._minute_hand_color = QColor("teal")

    def paintEvent(self, event):
        side = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        self.draw_hour_marks(painter)
        self.draw_minute_marks(painter)

        self.draw_hour_numbers(painter)
        self.draw_minute_numbers(painter)

        self.draw_hour_hand(painter, self._time)
        self.draw_minute_hand(painter, self._time)

    def draw_hour_marks(self, painter: QPainter) -> None:
        for i in range(12):
            painter.drawLine(70, 0, 80, 0)
            painter.rotate(30)

    def draw_minute_marks(self, painter: QPainter) -> None:
        for i in range(60):
            if i % 5 != 0:
                painter.drawLine(77, 0, 80, 0)
            painter.rotate(6)

    def draw_hour_numbers(self, painter: QPainter) -> None:
        painter.setPen(self._hour_numbers_color)
        font = painter.font()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        circle_diameter = 60

        for i in range(1, 13):
            angle = math.radians(-30 * i)
            x = circle_diameter * -math.sin(angle)
            y = circle_diameter * -math.cos(angle)
            painter.drawText(int(x - 5), int(y + 5), str(i))

    def draw_minute_numbers(self, painter: QPainter) -> None:
        painter.setPen(self._minute_numbers_color)
        font = painter.font()
        font.setPointSize(6)
        font.setBold(True)
        painter.setFont(font)
        circle_diameter = 90

        for i in range(1, 61):
            if i % 5 == 0:
                angle = math.radians(-6 * i)
                x = circle_diameter * -math.sin(angle)
                y = circle_diameter * -math.cos(angle)
                x_offset = -5
                y_offset = 2.5
                if i == 60:
                    i = 0
                painter.drawText(int(x + x_offset), int(y + y_offset), str(i))

    def draw_hour_hand(self, painter: QPainter, time: QTime) -> None:
        self.hour_hand = QPolygon([
            QPoint(5, 8),
            QPoint(-5, 8),
            QPoint(0, -35)
        ])
        painter.setBrush(self._hour_hand_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.save()
        hour_angle = 30 * (time.hour() % 12 + time.minute() / 60.0)
        painter.rotate(hour_angle)
        painter.drawConvexPolygon(self.hour_hand)
        painter.restore()

    def draw_minute_hand(self, painter: QPainter, time: QTime) -> None:
        self.minute_hand = QPolygon([
            QPoint(3, 8),
            QPoint(-3, 8),
            QPoint(0, -55)
        ])
        painter.setBrush(self._minute_hand_color)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.save()
        minute_angle = 6 * (time.minute() + time.second() / 60.0)
        painter.rotate(minute_angle)
        painter.drawConvexPolygon(self.minute_hand)
        painter.restore()


class DigitalClock(QLabel):
    def __init__(self, time: QTime, parent=None):
        super().__init__(parent)
        self._time = time

        font = QFont()
        font.setPointSize(64)
        font.setBold(True)
        self.setFont(font)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._set_text()

    def set_time(self, time: QTime):
        self._time = time
        self._set_text()

    def _set_text(self):
        # TODO: use proper formatting and assign color

        hours = self._text_style(self._time.toString("hh"), "red")
        minutes = self._text_style(self._time.toString("mm"), "teal")

        self.setText(f"{hours}:{minutes}")

    def _text_style(self, text: str, color: str) -> str:
        return (
            f'<span style="color: {color};">{text}</span>'
        )


class Model:
    def __init__(self):
        self._time = QTime.currentTime()

    def get_time(self) -> QTime:
        return self._time

    def get_round_time(self, mins_precision: int = 5):
        minute = round(self._time.minute() / mins_precision) * mins_precision
        return QTime(self._time.hour(), minute)

    def set_time(self, time: QTime) -> None:
        self._time = time

    def generate_random_time(self, mins_precision: int = 5) -> QTime:
        hour = random.randint(1, 12)
        minute = round(random.randint(0, 59) / mins_precision) * mins_precision
        return QTime(hour, minute)


class View(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Analog Clock")
        self.resize(600, 900)
        self.setStyleSheet(
            """
            QPushButton {
                font-size: 32px;
                font: bold;
            }
            """
        )

        layout = QVBoxLayout(self)
        initial_time = QTime()

        self._analog_clock = AnalogClock(initial_time, self)
        layout.addWidget(self._analog_clock)

        self.time_generator_button = QPushButton("New Time", self)
        layout.addWidget(self.time_generator_button)

        self.show_digital_button = QPushButton("Show Digital", self)
        layout.addWidget(self.show_digital_button)

        self._digital_clock = DigitalClock(initial_time, self)
        self._digital_clock.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self._digital_clock.hide()
        layout.addWidget(self._digital_clock)

    def update_analog_clock(self, time: QTime):
        self._analog_clock.set_time(time)
        self._analog_clock.update()

    def update_digital_clock(self, time: QTime):
        self._digital_clock.set_time(time)
        self._digital_clock.update()

    def show_digital_clock(self):
        self._digital_clock.show()

    def hide_digital_clock(self):
        self._digital_clock.hide()


class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
        self._time = model.get_round_time()

        self._view.time_generator_button.clicked.connect(self.update_time)
        self._view.show_digital_button.clicked.connect(self.show_digital_clock)

        self.update_view()

    def update_time(self) -> None:
        self._time = self._model.generate_random_time()
        self.update_view()
        self._view.hide_digital_clock()

    def show_digital_clock(self) -> None:
        self._view.show_digital_clock()

    def update_view(self) -> None:
        self._view.update_analog_clock(self._time)
        self._view.update_digital_clock(self._time)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = Model()
    view = View()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec())

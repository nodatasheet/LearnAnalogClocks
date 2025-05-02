import random
import sys
import math
from PyQt5.QtCore import Qt, QTime, QPoint, pyqtSignal
from PyQt5.QtGui import QFont, QPainter, QColor, QPolygon
from PyQt5.QtWidgets import QApplication, QPushButton, QSizePolicy, QWidget, QVBoxLayout, QLabel


class AnalogClockWidget(QWidget):
    def __init__(self, time: QTime, parent=None):
        super().__init__(parent)

        self.time = time

        # Define the shapes of the hour, minute, and second hands
        self.hour_hand: QPolygon = QPolygon([
            QPoint(5, 8),
            QPoint(-5, 8),
            QPoint(0, -35)
        ])
        self.minute_hand: QPolygon = QPolygon([
            QPoint(3, 8),
            QPoint(-3, 8),
            QPoint(0, -55)
        ])
        self.second_hand: QPolygon = QPolygon([
            QPoint(1, 8),
            QPoint(-1, 8),
            QPoint(0, -80)
        ])

        self.hour_hand_color: QColor = QColor("red")
        self.minute_hand_color: QColor = QColor("cyan")
        self.seconds_hand_color: QColor = QColor("white")

        self.hour_text_color: QColor = QColor("red")
        self.minute_text_color: QColor = QColor("cyan")

    def paintEvent(self, event):
        side = min(self.width(), self.height())

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        self.draw_hour_marks(painter)
        self.draw_minute_marks(painter)

        self.draw_hour_numbers(painter)
        self.draw_minute_numbers(painter)

        self.draw_hour_hand(painter, self.time)
        self.draw_minute_hand(painter, self.time)

    def draw_hour_marks(self, painter: QPainter) -> None:
        painter.setPen(QColor("white"))
        for i in range(12):
            painter.drawLine(70, 0, 80, 0)
            painter.rotate(30)

    def draw_minute_marks(self, painter: QPainter) -> None:
        painter.setPen(QColor("white"))
        for i in range(60):
            if i % 5 != 0:
                painter.drawLine(77, 0, 80, 0)
            painter.rotate(6)

    def draw_hour_numbers(self, painter: QPainter) -> None:
        painter.setPen(self.hour_text_color)
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        circle_diameter = 60

        for i in range(1, 13):
            angle = math.radians(-30 * i)
            x = circle_diameter * -math.sin(angle)
            y = circle_diameter * -math.cos(angle)
            painter.drawText(int(x - 5), int(y + 5), str(i))

    def draw_minute_numbers(self, painter: QPainter) -> None:
        painter.setPen(self.minute_text_color)
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
        painter.setBrush(self.hour_hand_color)
        painter.setPen(Qt.NoPen)
        painter.save()
        hour_angle = 30 * (time.hour() % 12 + time.minute() / 60.0)
        painter.rotate(hour_angle)
        painter.drawConvexPolygon(self.hour_hand)
        painter.restore()

    def draw_minute_hand(self, painter: QPainter, time: QTime) -> None:
        painter.setBrush(self.minute_hand_color)
        painter.setPen(Qt.NoPen)
        painter.save()
        minute_angle = 6 * (time.minute() + time.second() / 60.0)
        painter.rotate(minute_angle)
        painter.drawConvexPolygon(self.minute_hand)
        painter.restore()


class DigitalClockWidget(QLabel):
    def __init__(self, time: QTime, parent=None):
        super().__init__(parent)
        self.time = time

        font = QFont()
        font.setPointSize(64)
        font.setBold(True)
        self.setFont(font)

        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.format_text_style()

    def format_text_style(self):
        hours = self._text_style(
            self.time.toString("hh"),
            "red"
        )
        minutes = self._text_style(
            self.time.toString("mm"),
            "cyan"
        )
        separator = self._text_style(":", "white")
        self.setText(f"{hours}{separator}{minutes}")

    def _text_style(self, text: str, color: str) -> str:
        return (
            f'<span style="color: {color};">{text}</span>'
        )


class TimeGenerator(QWidget):
    """A widget with a button to generate a random time."""
    generated = pyqtSignal(QTime)  # Signal to emit the new time

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the "New Time" button
        self.button = QPushButton("New Time", self)
        self.button.setStyleSheet(
            "font-size: 32px; color: white; background-color: gray;"
        )
        self.button.clicked.connect(self.generate_random_time)

        # Layout for the button
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

    def generate_random_time(self):
        """Generate a random time and emit it."""
        hour = random.randint(0, 9)
        minute = random.choice(range(0, 59, 5))
        new_time = QTime(hour, minute)
        self.generated.emit(new_time)


class ShowDigitalButton(QWidget):
    """A widget with a button to show the digital clock."""
    signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)

        # Create the "Show Digital Time" button
        self.button = QPushButton("Show Digital Time", self)
        self.button.setStyleSheet(
            "font-size: 32px; color: white; background-color: gray;"
        )
        self.button.clicked.connect(self.emit_signal)

        # Layout for the button
        layout = QVBoxLayout(self)
        layout.addWidget(self.button)

    def emit_signal(self):
        """Emit the signal and disable the button."""
        self.signal.emit()


class Clock(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Analog Clock")
        self.resize(600, 900)
        self.setStyleSheet("background-color: black;")

        self.time = QTime().currentTime()

        layout = QVBoxLayout(self)

        self.analog_clock = AnalogClockWidget(self.time, self)
        layout.addWidget(self.analog_clock)

        self.time_generator = TimeGenerator(self)
        self.time_generator.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.time_generator.generated.connect(self.update_time)
        layout.addWidget(self.time_generator)

        self.show_digital_button = ShowDigitalButton(self)
        self.show_digital_button.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.show_digital_button.signal.connect(self.show_digital_time)
        layout.addWidget(self.show_digital_button)

        self.digital_clock = DigitalClockWidget(self.time, self)
        self.digital_clock.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )
        self.digital_clock.hide()
        layout.addWidget(self.digital_clock)

    def update_time(self, new_time: QTime):
        """Update the clocks with the new time."""
        self.digital_clock.hide()

        self.analog_clock.time = new_time
        self.analog_clock.update()

        self.digital_clock.time = new_time
        self.digital_clock.format_text_style()

    def show_digital_time(self):
        """Unhide the digital clock."""
        self.digital_clock.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clock = Clock()
    clock.show()
    sys.exit(app.exec_())

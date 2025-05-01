import sys
import math
from PyQt5.QtCore import Qt, QTime, QPoint
from PyQt5.QtGui import QPainter, QColor, QPolygon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel


class AnalogClockWidget(QWidget):
    def __init__(self, manual_time: QTime, parent=None):
        super().__init__(parent)
        self.manual_time = manual_time

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

        time = self.manual_time

        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.translate(self.width() / 2, self.height() / 2)
        painter.scale(side / 200.0, side / 200.0)

        self.draw_hour_marks(painter)
        self.draw_hour_numbers(painter)
        self.draw_minute_numbers(painter)

        self.draw_hour_hand(painter, time)
        self.draw_minute_hand(painter, time)

    def draw_hour_marks(self, painter: QPainter) -> None:
        painter.setPen(QColor("white"))
        for i in range(12):
            painter.drawLine(75, 0, 80, 0)
            painter.rotate(30)

    def draw_hour_numbers(self, painter: QPainter) -> None:
        painter.setPen(self.hour_text_color)
        font = painter.font()
        font.setPointSize(10)
        painter.setFont(font)
        circle_diameter = 60

        for i in range(1, 13):
            angle = math.radians(30 * i)
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
                angle = math.radians(6 * i)
                x = circle_diameter * -math.sin(angle)
                y = circle_diameter * -math.cos(angle)
                x_offset = -5
                y_offset = 2.5
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
    def __init__(self, manual_time: QTime, parent=None):
        super().__init__(parent)
        self.manual_time = manual_time
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet("font-size: 64px;")  # Set font size
        self.update_text()

    def update_text(self):
        styled_hours = self._text_style(
            self.manual_time.toString("hh"),
            "red"
        )
        styled_minutes = self._text_style(
            self.manual_time.toString("mm"),
            "cyan"
        )
        separator = self._text_style(":", "white")
        self.setText(f"{styled_hours}{separator}{styled_minutes}")

    def _text_style(self, text: str, color: str) -> str:
        return (
            f'<span style="color: {color}; font-weight: bold;">{text}</span>'
        )


class Clock(QWidget):
    def __init__(self, manual_time: QTime) -> None:
        super().__init__()
        self.setWindowTitle("Analog Clock")
        self.resize(500, 550)
        self.setStyleSheet("background-color: black;")

        self.manual_time = manual_time

        # Layout to stack analog and digital clocks
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        # Analog clock widget
        self.analog_clock_widget = AnalogClockWidget(self.manual_time, self)
        layout.addWidget(self.analog_clock_widget)

        # Digital clock widget
        self.digital_clock_widget = DigitalClockWidget(self.manual_time, self)
        layout.addWidget(self.digital_clock_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    time = QTime(3, 45)  # Set the manual time here
    clock = Clock(time)
    clock.show()
    sys.exit(app.exec_())

import math

from PyQt6.QtCore import Qt, QTime, QPoint
from PyQt6.QtGui import QColor, QIntValidator, QPainter, QPolygon
from PyQt6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDialog,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QWidget):
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

        initial_time = QTime()
        layout = QVBoxLayout(self)

        top_layout = QHBoxLayout()
        top_layout.addStretch()
        self.settings_button = QPushButton("Settings", self)
        self.settings_button.setFixedWidth(90)
        self.settings_button.setStyleSheet("font-size: 18px;")
        top_layout.addWidget(self.settings_button)
        layout.addLayout(top_layout)

        self._analog_clock = AnalogClock(initial_time, self)
        layout.addWidget(self._analog_clock)

        self.time_input = TimeInput(self)
        layout.addWidget(self.time_input)

        self.show_digital_button = QPushButton("Show Digital", self)
        layout.addWidget(self.show_digital_button)

        self._digital_clock = DigitalClock(initial_time, self)
        layout.addWidget(self._digital_clock)
        self.hide_digital_clock()

        self.time_generator_button = QPushButton("New Time", self)
        layout.addWidget(self.time_generator_button)

    def update_analog_clock(self, time: QTime):
        self._analog_clock.set_time(time)
        self._analog_clock.update()

    def update_digital_clock(self, time: QTime):
        self._digital_clock.set_time(time)
        self._digital_clock.update()

    def show_digital_clock(self):
        self._digital_clock.show_clock()

    def hide_digital_clock(self):
        self._digital_clock.hide_clock()


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


class DigitalClock(QStackedWidget):
    def __init__(self, time: QTime, parent=None):
        super().__init__(parent)
        self._time = time
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self._digital_clock = QLabel(self)
        self._digital_clock.setStyleSheet("font-size: 64px; font: bold;")
        self._digital_clock.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._empty_widget = QWidget(self)
        self.addWidget(self._digital_clock)
        self.addWidget(self._empty_widget)

        self._set_text()

    def set_time(self, time: QTime):
        self._time = time
        self._set_text()

    def _set_text(self):
        hour_number = self._time.hour() % 12

        if hour_number == 0:
            hour_number = 12

        hours = self._text_style(str(hour_number).zfill(2), "red")
        minutes = self._text_style(self._time.toString("mm"), "teal")

        self._digital_clock.setText(f"{hours}:{minutes}")

    def _text_style(self, text: str, color: str) -> str:
        return (
            f'<span style="color: {color};">{text}</span>'
        )

    def show_clock(self):
        self.setCurrentWidget(self._digital_clock)

    def hide_clock(self):
        self.setCurrentWidget(self._empty_widget)


class TimeInput(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        layout = QHBoxLayout(self)
        self.setStyleSheet(
            """
            QLineEdit {
                font-size: 32px;
                font: bold;
            }
            """
        )
        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed
        )

        self._hours = QLineEdit(self)
        self._hours.setMaxLength(2)
        self._hours.setValidator(QIntValidator(0, 23, self))
        self._hours.setPlaceholderText("HH")
        layout.addWidget(self._hours)

        self._minutes = QLineEdit(self)
        self._minutes.setMaxLength(2)
        self._minutes.setValidator(QIntValidator(0, 59, self))
        self._minutes.setPlaceholderText("MM")
        layout.addWidget(self._minutes)

        self.check_button = QPushButton("Check", self)
        self.check_button.setFixedWidth(200)
        layout.addWidget(self.check_button)

    def hours(self):
        self._hours.setStyleSheet("")
        return self._hours.text()

    def minutes(self):
        self._minutes.setStyleSheet("")
        return self._minutes.text()

    def set_hours_wrong(self):
        self._hours.setStyleSheet("background-color: red;")

    def set_minutes_wrong(self):
        self._minutes.setStyleSheet("background-color: red;")

    def set_hours_correct(self):
        self._hours.setStyleSheet("background-color: green;")

    def set_minutes_correct(self):
        self._minutes.setStyleSheet("background-color: green;")

    def reset(self):
        self._hours.clear()
        self._minutes.clear()
        self._hours.setStyleSheet("")
        self._minutes.setStyleSheet("")

    def hours_return_pressed(self):
        return self._hours.returnPressed

    def minutes_return_pressed(self):
        return self._minutes.returnPressed


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.resize(400, 300)
        self.setStyleSheet(
            """
            QPushButton {
                font-size: 18px;
                font: bold;
            }
            QCheckBox, QComboBox {
                font-size: 16px;
            }
            QLabel, QComboBox {
                font-size: 16px;
            }
            """
        )

        main_layout = QVBoxLayout(self)

        visual_group = QGroupBox("Visual", self)
        visual_layout = QVBoxLayout(visual_group)

        self._minute_marks_checkbox = QCheckBox("Show minute marks", self)
        self._hour_marks_checkbox = QCheckBox("Show hour marks", self)

        visual_layout.addWidget(self._minute_marks_checkbox)
        visual_layout.addWidget(self._hour_marks_checkbox)

        self._hour_text_dropdown = self._add_dropdown(
            label="Show hours text",
            items=["None", "Every 1-hr", "Every 3-hr", "Every 6-hr"],
            parent=visual_layout
        )

        self._minute_text_dropdown = self._add_dropdown(
            label="Show minutes text",
            items=["None", "Every 5-min", "Every 15-min", "Every 30-min"],
            parent=visual_layout
        )

        main_layout.addWidget(visual_group)

        behavior_group = QGroupBox("Behavior", self)
        behavior_layout = QVBoxLayout(behavior_group)

        self._round_minutes_dropdown = self._add_dropdown(
            label="Round-up selected minutes: ",
            items=["1", "5", "15", "30"],
            parent=behavior_layout
        )

        main_layout.addWidget(behavior_group)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        main_layout.addWidget(close_button)

    def _add_dropdown(self,
                      label: str,
                      items: list,
                      parent: QVBoxLayout) -> QComboBox:

        layout = QHBoxLayout()
        label = QLabel(label, self)
        dropdown = QComboBox(self)
        dropdown.addItems(items)

        layout.addWidget(label)
        layout.addWidget(dropdown)
        parent.addLayout(layout)

        return dropdown

from view import MainWindow, SettingsWindow
from model import Model


class Controller:
    def __init__(self, model: Model, main_window: MainWindow):
        self._model = model
        self._main_window = main_window
        self._time = model.get_round_time()
        self._bind_main_window_buttons()
        self._update_analog_clock_settings()
        self._update_clocks()

    def show_main_window(self):
        self._main_window.show()

    def _bind_main_window_buttons(self):
        main = self._main_window
        main.time_generator_button.clicked.connect(self._update_time)
        main.show_digital_button.clicked.connect(self._show_digital)
        main.time_input.check_button.clicked.connect(self._check_input)
        main.time_input.hours_return_pressed().connect(self._check_input)
        main.time_input.minutes_return_pressed().connect(self._check_input)
        main.settings_button.clicked.connect(self._open_settings)

    def _open_settings(self):
        self._settings_window = SettingsWindow(self._main_window)
        settings = self._model.settings

        self._settings_window.hour_marks_checkbox.setChecked(
            settings.show_hour_marks.checked
        )

        self._settings_window.minute_marks_checkbox.setChecked(
            settings.show_minute_marks.checked
        )

        self._settings_window.set_current_value(
            self._settings_window.minute_text_dropdown,
            settings.minutes_text_interval.value
        )

        self._settings_window.set_current_value(
            self._settings_window.hour_text_dropdown,
            settings.hours_text_interval.value
        )

        self._settings_window.set_current_value(
            self._settings_window.round_minutes_dropdown,
            settings.round_minutes_to_nearest.value
        )

        self._settings_window.set_button.clicked.connect(self._save_settings)
        self._settings_window.exec()

    def _save_settings(self):
        settings = self._model.settings
        window = self._settings_window

        settings.show_minute_marks.checked = \
            window.minute_marks_checkbox.isChecked()

        settings.show_hour_marks.checked = \
            window.hour_marks_checkbox.isChecked()

        settings.minutes_text_interval.value = \
            window.get_item(window.minute_text_dropdown).value

        settings.hours_text_interval.value = \
            window.get_item(window.hour_text_dropdown).value

        settings.round_minutes_to_nearest.value = \
            window.get_item(window.round_minutes_dropdown).value

        self._update_analog_clock_settings()
        window.close()

    def _update_analog_clock_settings(self):
        model_settings = self._model.settings
        analog_settings = self._main_window.get_analog_settings()

        analog_settings.minutes_text_interval = \
            model_settings.minutes_text_interval.value

        analog_settings.hours_text_interval = \
            model_settings.hours_text_interval.value

        analog_settings.show_minute_marks = \
            model_settings.show_minute_marks.checked

        analog_settings.show_hour_marks = \
            model_settings.show_hour_marks.checked

        self._main_window.update_analog_clock_settings(analog_settings)

    def _update_time(self):
        self._time = self._model.generate_random_time()
        self._update_clocks()
        self._main_window.hide_digital_clock()
        self._main_window.time_input.reset()

    def _show_digital(self):
        self._main_window.show_digital_clock()

    def _update_clocks(self):
        self._main_window.update_analog_clock_time(self._time)
        self._main_window.update_digital_clock_time(self._time)

    def _check_input(self):
        time_input = self._main_window.time_input
        actual_hours = self._time.hour() % 12

        if actual_hours == 0:
            actual_hours = 12

        if self._is_same(time_input.hours(), actual_hours):
            time_input.set_hours_correct()

        else:
            time_input.set_hours_wrong()

        if self._is_same(time_input.minutes(), self._time.minute()):
            time_input.set_minutes_correct()

        else:
            time_input.set_minutes_wrong()

    def _is_same(self, input_value: str, actual: int) -> bool:
        if input_value.isnumeric():
            if actual == int(input_value):
                return True

        return False

from view import View
from model import Model


class Controller:
    def __init__(self, model: Model, view: View):
        self._model = model
        self._view = view
        self._time = model.get_round_time()

        view.time_generator_button.clicked.connect(self.update_time)
        view.show_digital_button.clicked.connect(self.show_digital_clock)
        view.time_input.check_button.clicked.connect(self.check_input)
        view.time_input.hours_return_pressed().connect(self.check_input)
        view.time_input.minutes_return_pressed().connect(self.check_input)

        self.update_view()

    def update_time(self):
        self._time = self._model.generate_random_time()
        self.update_view()
        self._view.hide_digital_clock()
        self._view.time_input.reset()

    def show_digital_clock(self):
        self._view.show_digital_clock()

    def update_view(self):
        self._view.update_analog_clock(self._time)
        self._view.update_digital_clock(self._time)

    def check_input(self):
        time_input = self._view.time_input
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

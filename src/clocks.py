import sys

from view import MainWindow
from model import Model
from controller import Controller

from PyQt6.QtWidgets import QApplication

if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = Model()
    view = MainWindow()
    controller = Controller(model, view)
    view.show()
    sys.exit(app.exec())

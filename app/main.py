import os
import sys

import qdarkstyle
from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.uic import loadUi

from ApplicationFacade import ApplicationFacade


class WeatherApp(QDialog):
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

    def __init__(self):
        super(WeatherApp, self).__init__()
        ui_path = os.path.join(self.ROOT_DIR, 'weather-app.ui')
        loadUi(ui_path, self)
        self.__facade: ApplicationFacade = ApplicationFacade()
        self.searchButton.clicked.connect(lambda: self.__facade.get_gui_data(self))  # Search button callback


if __name__ == "__main__":
    app = QApplication(sys.argv)

    stylesheet = qdarkstyle.load_stylesheet_pyqt5()
    app.setStyleSheet(stylesheet)

    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())


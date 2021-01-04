import json

from DataManager import DataManager


class ApplicationFacade:
    def __init__(self):
        self.__data_manager: DataManager = DataManager()

    def get_gui_data(self, gui) -> dict:
        data = self.__data_manager.get_info(gui.searchTextEdit.toPlainText().capitalize())
        print(json.dumps(data, indent=2))

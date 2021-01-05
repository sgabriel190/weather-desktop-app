import time
from concurrent import futures

from PyQt5.QtWidgets import QLabel, QErrorMessage

from DataHelper import FormatDataHelper
from DataManager import DataManager


class ApplicationFacade:
    def __init__(self, gui):
        self.__gui = gui
        self.__data_manager: DataManager = DataManager()
        self.__fresh_opened = True

    def __set_ui(self, value: bool) -> None:
        """
        This method sets visible all the widgets.
        :param value: A bool value which sets the widgets visible or not.
        """
        self.__fresh_opened = not value
        self.__gui.scrollAreaNextHoursWeather.setVisible(value)
        self.__gui.groupBoxWeatherNext3Days.setVisible(value)
        self.__gui.groupBoxGeneralInfo.setVisible(value)
        self.__gui.frameCurrentInfo.setVisible(value)

    def __set_current_data(self, data: dict) -> None:
        """
        This method sets the labels for the current weather
        :param data: A dictionary containing all the data for current time.
        """
        self.__gui.labelCity.setText(data["city"])
        self.__gui.labelCurrentTemperature.setText(FormatDataHelper.format_temp(data["current"]["temp"]))
        self.__gui.labelCurrentAdditionalInfo.setText("{}: {}".format(data["current"]["weather"][0]["main"],
                                                                      data["current"]["weather"][0]["description"]))
        self.__gui.labelCurrentAdditionalInfo_2.setPixmap(FormatDataHelper.get_image(data["current"]["weather"][0]["icon"]))

    def __set_next_hours(self, data: list) -> None:
        """
        This method sets data for the next hours widgets.
        :param data: A dictionary containing the data for the next hours.
        """
        tmp_time = "labelTimeHourTemp"
        tmp_temp = "labelTemperatureHourTemp"
        tmp_img = "labelImageHourTemp"

        icons_url = list(map(lambda x: x["icon"], data))
        results = FormatDataHelper.get_images(icons_url)

        for index, item in enumerate(data):
            # Search for the labels to be changed
            label_img = self.__gui.findChild(QLabel, tmp_img+str(index+1))
            label_time = self.__gui.findChild(QLabel, tmp_time+str(index+1))
            label_temp = self.__gui.findChild(QLabel, tmp_temp+str(index+1))

            # Update the labels
            label_time.setText(str(item["time"].split("~")[0].strip()))
            label_temp.setText(str(FormatDataHelper.format_temp(item["temperature"])))
            label_img.setPixmap(results[index])

    def __set_next_days_data(self, data: list) -> None:
        """
        This method sets data for the next days widgets.
        :param data: A list with data for the next 3 days.
        """
        tmp_day = "labelDayName"
        tmp_img = "labelImageDay"
        tmp_min_temp = "labelMinTempDay"
        tmp_max_temp = "labelMaxTempDay"
        icons_url = list(map(lambda x: x["icon"], data))
        results = FormatDataHelper.get_images(icons_url)
        for index, item in enumerate(data):
            # Search for the labels to be changed
            label_day = self.__gui.findChild(QLabel, tmp_day+str(index+1))
            label_img = self.__gui.findChild(QLabel, tmp_img+str(index+1))
            label_min_temp = self.__gui.findChild(QLabel, tmp_min_temp+str(index+1))
            label_max_temp = self.__gui.findChild(QLabel, tmp_max_temp+str(index+1))

            # Update the labels
            label_day.setText(str(item["time"].split("~")[1].strip()))
            label_img.setPixmap(results[index])
            label_min_temp.setText("Min: {}".format(FormatDataHelper.format_temp(item["min_temp"])))
            label_max_temp.setText("Max: {}".format(FormatDataHelper.format_temp(item["max_temp"])))

    def __set_general_information(self, data: dict) -> None:
        """
        This method sets the data for the general widget
        :param data: A dictionary containing for the current day.
        """
        label_names = {
            "humidity": "labelHumidityValue",
            "pressure": "labelPressureValue",
            "wind_speed": "labelWindSpeedValue",
            "visibility": "labelVisibilityValue",
            "feels_like": "labelFeelsLikeValue",
            "clouds": "labelCloudinessValue"
        }

        for key in label_names.keys():
            label = self.__gui.findChild(QLabel, label_names[key])
            value = data[key]
            label.setText(str(value))

    def __set_gui_data(self, data: dict) -> None:
        """
        This method sets data for a search.
        :param data: A dictionary containing all the data for the search.
        """
        start = time.time()
        with futures.ThreadPoolExecutor(max_workers=10) as e:
            e.submit(lambda: self.__set_next_days_data(data["daily"]))
            e.submit(lambda: self.__set_next_hours(data["hourly"]))
            e.submit(lambda: self.__set_current_data(data))
            e.submit(lambda: self.__set_general_information(data["current"]))
        print("[ApplicationFacade] - set data {}".format(time.time() - start))

    def get_gui_data(self) -> None:
        """
        This is the main method of the class. It serves as the callback function of the gui search button.
        """
        try:
            if self.__fresh_opened is True:
                self.__set_ui(True)
            data = self.__data_manager.get_info(self.__gui.searchTextEdit.toPlainText().capitalize())
            start = time.time()
            self.__set_gui_data(data)
            print("[ApplicationFacade] - render {}".format(time.time() - start))
        except Exception as e:
            self.__set_ui(False)
            print("[ApplicationFacade] - __set_gui_data error: {}".format(e))
            dialog = QErrorMessage()
            dialog.showMessage(str(e))
            dialog.exec_()

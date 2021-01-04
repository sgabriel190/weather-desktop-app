from PyQt5.QtWidgets import QLabel

from DataManager import DataManager
from FormatDataHelper import FormatDataHelper


class ApplicationFacade:
    def __init__(self, gui):
        self.__gui = gui
        self.__data_manager: DataManager = DataManager()
        self.__fresh_opened = True

    def __set_ui_visible(self) -> None:
        self.__fresh_opened = False
        self.__gui.scrollAreaNextHoursWeather.setVisible(True)
        self.__gui.groupBoxWeatherNext3Days.setVisible(True)
        self.__gui.groupBoxGeneralInfo.setVisible(True)
        self.__gui.frameCurrentInfo.setVisible(True)

    def __set_current_data(self, data: dict):
        self.__gui.labelCity.setText(data["city"])
        self.__gui.labelCurrentTemperature.setText(FormatDataHelper.format_temp(data["current"]["temp"]))
        self.__gui.labelCurrentAdditionalInfo.setText("{}: {}".format(data["current"]["weather"][0]["main"],
                                                                      data["current"]["weather"][0]["description"]))
        self.__gui.labelCurrentAdditionalInfo_2.setPixmap(FormatDataHelper.get_image(data["current"]["weather"][0]["icon"]))

    def __set_next_hours(self, data: list) -> None:
        tmp_time = "labelTimeHourTemp"
        tmp_temp = "labelTemperatureHourTemp"
        tmp_img = "labelImageHourTemp"

        for index, item in enumerate(data):
            label_img = self.__gui.findChild(QLabel, tmp_img+str(index+1))
            label_time= self.__gui.findChild(QLabel, tmp_time+str(index+1))
            label_temp = self.__gui.findChild(QLabel, tmp_temp+str(index+1))

            label_time.setText(str(item["time"].split("~")[0].strip()))
            label_temp.setText(str(FormatDataHelper.format_temp(item["temperature"])))
            label_img.setPixmap(FormatDataHelper.get_image(item["icon"]))

    def __set_next_days_data(self, data: list) -> None:
        tmp_day = "labelDayName"
        tmp_img = "labelImageDay"
        tmp_min_temp = "labelMinTempDay"
        tmp_max_temp = "labelMaxTempDay"

        for index, item in enumerate(data):
            label_day = self.__gui.findChild(QLabel, tmp_day+str(index+1))
            label_img = self.__gui.findChild(QLabel, tmp_img+str(index+1))
            label_min_temp = self.__gui.findChild(QLabel, tmp_min_temp+str(index+1))
            label_max_temp = self.__gui.findChild(QLabel, tmp_max_temp+str(index+1))

            label_day.setText(str(item["time"].split("~")[1].strip()))
            label_img.setPixmap(FormatDataHelper.get_image(item["icon"]))
            label_min_temp.setText("Min: {}".format(FormatDataHelper.format_temp(item["min_temp"])))
            label_max_temp.setText("Max: {}".format(FormatDataHelper.format_temp(item["max_temp"])))

    def __set_general_information(self, data: dict) -> None:
        label_names = {
            "humidity": "labelHumidtyValue",
            "pressure": "labelPressureValue",
            "wind_speed": "labelWindSpeedValue",
            "visibility": "labelVisibilityValue",
            "feels_like": "labelFeelsLikeValue",
            "clouds": "labelCloudlinesValue"
        }

        for key in label_names.keys():
            print(key, label_names[key])
            label = self.__gui.findChild(QLabel, label_names[key])
            value = data[key]
            label.setText(str(value))

    def __set_gui_data(self, data: dict):
        self.__set_current_data(data)
        self.__set_next_days_data(data["daily"])
        self.__set_next_hours(data["hourly"])
        self.__set_general_information(data["current"])

    def get_gui_data(self) -> None:
        if self.__fresh_opened is True:
            self.__set_ui_visible()
            data = self.__data_manager.get_info(self.__gui.searchTextEdit.toPlainText().capitalize())
            self.__set_gui_data(data)
        else:
            data = self.__data_manager.get_info(self.__gui.searchTextEdit.toPlainText().capitalize())
            self.__set_gui_data(data)

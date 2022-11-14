from PyQt5 import QtGui, uic, QtMultimedia, QtCore
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import *
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QTableWidgetItem
import sys


class Hello(QDialog):
    def __init__(self):
        found_native_city = False
        try:
            with open('../Project-1.PyQt/native_city.txt', 'r', encoding='utf-8') as file:
                data = file.readlines()
                if data:
                    if functions.check_city_existence(data[-1]) == 1:
                        found_native_city = True
                        self.start_skeleton(data[-1])

        except FileNotFoundError:
            pass

        if not found_native_city:
            super(Hello, self).__init__()
            uic.loadUi('hello.ui', self)
            self.setFixedSize(400, 230)
            self.setWindowTitle('WeCha')
            self.setWindowIcon(QtGui.QIcon('window_icon.ico'))

            self.start_button.clicked.connect(self.run)

            self.show()

    def run(self):
        city = self.city_lineEdit.text()
        res = functions.check_city_existence(city)
        if res == 1:
            if self.checkBox.isChecked():
                with open('../Project-1.PyQt/native_city.txt', 'w', encoding='utf-8') as file:
                    file.write(city)
            self.close()
            self.start_skeleton(city)

        elif res == -1:
            self.status_bar.setText('город не найден')
        elif res == -2:
            self.status_bar.setText('нет подключения')
        elif res == -3:
            self.status_bar.setText('введите город')

    def start_skeleton(self, native_city):
        self.skeleton = Skeleton(native_city)
        self.skeleton.show()


class Skeleton(QWidget):
    def __init__(self, native_city):
        self.native_city = native_city
        super(Skeleton, self).__init__()
        uic.loadUi('skeleton.ui', self)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(500, 800)
        self.setWindowTitle('WeCha')
        self.setWindowIcon(QtGui.QIcon('window_icon.ico'))

        self.home_button.clicked.connect(self.start_home_page)
        self.search_button.clicked.connect(self.start_search_page)
        self.settings_button.clicked.connect(self.start_settings)

        self.widgets = {'home_page': None, 'search_page': None}
        self.start_home_page()

    def start_home_page(self):
        for widget in list(self.widgets.values()):
            if widget:
                widget.hide()

        if not self.widgets['home_page']:
            self.home_page = HomePage(self.native_city, self)
            self.home_page.move(0, 0)
            self.widgets['home_page'] = self.home_page
        self.home_page.show()

    def start_search_page(self):
        for widget in list(self.widgets.values()):
            if widget:
                widget.hide()

        if not self.widgets['search_page']:
            self.search_page = SearchPage(self)
            self.search_page.move(0, 0)
            self.widgets['search_page'] = self.search_page
        self.search_page.show()

    def start_settings(self):
        self.settings = Settings()
        self.settings.show()


class HomePage(QWidget):
    def __init__(self, native_city, mother=None):
        self.native_city = native_city
        super(HomePage, self).__init__(mother)
        uic.loadUi('home_page.ui', self)
        self.init_ui()

    def init_ui(self):
        self.setFixedSize(500, 675)

        self.day_1_weekday_button.clicked.connect(self.data_for_day)
        self.day_2_weekday_button.clicked.connect(self.data_for_day)
        self.day_3_weekday_button.clicked.connect(self.data_for_day)

        self.set_time_and_weekday()
        self.set_native_city(self.native_city)
        self.set_current_data()
        self.set_nearest_data()
        self.set_forecast_data()

    def set_time_and_weekday(self):
        weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        date, time, weekdaynum = functions.get_moscow_time_and_weekdaynum()
        weekday = weekdays[weekdaynum - 1]
        self.current_time_weekday.setText(f'{time}, {weekday}')

    def set_native_city(self, native_city):
        self.native_city_label.setText(native_city)

    def set_current_data(self):
        data = functions.get_current_weather(self.native_city)
        self.current_temp.setText(f"{round(data['temp'])}°C")
        self.current_description.setText(data['description'])
        self.current_feels_like.setText(f"Ощущается как {round(data['feels_like'])}°C")
        self.current_humidity.setText(f"Влажность: {data['humidity']}%")
        self.current_speed.setText(f"Скорость ветра: {data['speed']} м/с")
        self.current_pressure.setText(f"Давление: {data['pressure']} мм.")

        description = data['description']
        file_name = icon_dict(description)
        self.current_picture.setPixmap(QPixmap(f'{file_name}.png'))

    def set_nearest_data(self):
        self.forecast_data = functions.get_forecast(self.native_city)
        data = self.forecast_data

        data = list(data.values())
        new_data = list()
        for elem in data:
            for key, val in elem.items():
                if key != 'common':
                    new_data.append((key, val))
        data = new_data[1:4]

        description = data[0][1]['description']
        file_name = icon_dict(description)
        self.nearest_1_picture.setPixmap(QPixmap(f'{file_name}.png'))
        self.nearest_1_temp.setText(f"{round(data[0][1]['temp'])}°C")
        self.nearest_1_time.setText(data[0][0][:5])

        description = data[1][1]['description']
        file_name = icon_dict(description)
        self.nearest_2_picture.setPixmap(QPixmap(f'{file_name}.png'))
        self.nearest_2_temp.setText(f"{round(data[1][1]['temp'])}°C")
        self.nearest_2_time.setText(data[1][0][:5])

        description = data[2][1]['description']
        file_name = icon_dict(description)
        self.nearest_3_picture.setPixmap(QPixmap(f'{file_name}.png'))
        self.nearest_3_temp.setText(f"{round(data[2][1]['temp'])}°C")
        self.nearest_3_time.setText(data[2][0][:5])

    def set_forecast_data(self):
        weekdays = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        date, time, weekdaynum = functions.get_moscow_time_and_weekdaynum()
        weekdays = [weekdays[(weekdaynum + i) % 7] for i in range(3)]
        for i in range(3):
            eval(f"self.day_{i + 1}_weekday_button.setText(weekdays[{i}])")

        data = self.forecast_data
        dates = list(data.keys())[1:4]

        self.day_1_min_max_temp.setText(f"{data[dates[0]]['common']['temp_min']}°C -> "
                                        f"{data[dates[0]]['common']['temp_max']}°C")
        self.day_1_speed.setText(f"{data[dates[0]]['common']['speed']} м/с")
        description = data[dates[0]]['common']['description']
        file_name = icon_dict(description)
        self.day_1_picture.setPixmap(QPixmap(f'{file_name}.png'))

        self.day_2_min_max_temp.setText(f"{data[dates[1]]['common']['temp_min']}°C -> "
                                        f"{data[dates[1]]['common']['temp_max']}°C")
        self.day_2_speed.setText(f"{data[dates[1]]['common']['speed']} м/с")
        description = data[dates[1]]['common']['description']
        file_name = icon_dict(description)
        self.day_2_picture.setPixmap(QPixmap(f'{file_name}.png'))

        self.day_3_min_max_temp.setText(f"{data[dates[2]]['common']['temp_min']}°C -> "
                                        f"{data[dates[2]]['common']['temp_max']}°C")
        self.day_3_speed.setText(f"{data[dates[2]]['common']['speed']} м/с")
        description = data[dates[2]]['common']['description']
        file_name = icon_dict(description)
        self.day_3_picture.setPixmap(QPixmap(f'{file_name}.png'))

    def data_for_day(self):
        day_num = int(self.sender().objectName()[4])
        data = list(self.forecast_data.items())[day_num][1]
        self.start_day_data(data)

    def start_day_data(self, data):
        self.day_data = DayData(data)
        self.day_data.show()



sys._excepthook = sys.excepthook


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    music = PlayMusic()
    ex = Hello()
    sys.exit(app.exec())

import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidgetItem, QDialog
from __config__ import *

sys._excepthook = sys.excepthook


class HomePage(QWidget):
    def __init__(self):
        super(HomePage, self).__init__()
        uic.loadUi(f'{PROJECT_SOURCE_PATH_UI}/home_page.ui', self)
        self.pushButton.clicked.connect(self.pressed)
        self.show()

    def pressed(self):
        self.day_data = DayData([])
        self.day_data.show()


class DayData(QDialog):
    def __init__(self, data: list):
        super(DayData, self).__init__()
        uic.loadUi(f'{PROJECT_SOURCE_PATH_UI}/day_data.ui', self)
        self.init_ui(data)

    def init_ui(self, data: list):
        self.setWindowTitle('Все данные, что мы имеем')

        self.pushButton.clicked.connect(self.ok_pressed)

        headers = {
            'name': 'Название',
            'place': 'Местонахождение',
            'phone': 'Номер телефона',
            'admin': 'Управляющий',
            'description': 'Описание'

        }

        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(list(headers.values()))
        self.tableWidget.setRowCount(0)

        for elem in data:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for key, val in elem:
                for i, header in enumerate(list(headers.keys())):
                    table_widget_item = QTableWidgetItem(str(val[header]))
                    self.tableWidget.setItem(row_position, i + 1, table_widget_item)

    def ok_pressed(self):
        self.close()


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomePage()
    sys.exit(app.exec())

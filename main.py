import sys
from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QHeaderView, QTableWidget, QWidget, QTableWidgetItem, QDialog
from __config__ import *
from utils.database.db import *

sys._excepthook = sys.excepthook

headers_full = ['ID', 'Название', 'Местонахождение', 'Номер телефона', 'Управляющий', 'Описание']
headers_admins = ['ID', 'ФИО', 'Роль', 'Номер телефона', 'Email']
headers_regions = ['ID', 'Регион']


class HomePage(QWidget):
    def __init__(self):
        super(HomePage, self).__init__()
        uic.loadUi(f'{PROJECT_SOURCE_PATH_UI}/home_page.ui', self)
        self.setWindowTitle("Global Tour")
        self.setWindowIcon(QIcon(f'{PROJECT_SOURCE_PATH_ICONS}/icon_dark.png'))

        self.pushButton_full.clicked.connect(self.pressed)
        self.pushButton_admins.clicked.connect(self.pressed)
        self.pushButton_regions.clicked.connect(self.pressed)
        self.pushButton_hotels.clicked.connect(self.pressed)

        self.show()

    def pressed(self):
        if self.sender() == self.pushButton_full:
            self.table_view = TableViewWidget(Hotel().get_pretty_units()[0], headers_full)
        elif self.sender() == self.pushButton_hotels:
            self.table_view = TableViewWidget(Hotel().get_units(), headers_full)
        elif self.sender() == self.pushButton_admins:
            self.table_view = TableViewWidget(Admins().get_units(), headers_admins)
        elif self.sender() == self.pushButton_regions:
            self.table_view = TableViewWidget(Regions().get_units(), headers_regions)

        self.table_view.show()


class TableViewWidget(QDialog):
    def __init__(self, data: list, headers: list):
        super(TableViewWidget, self).__init__()
        uic.loadUi(f'{PROJECT_SOURCE_PATH_UI}/day_data.ui', self)
        self.init_ui(data, headers)

    def init_ui(self, data: list, headers: list):
        self.setWindowTitle('Data')
        self.setWindowIcon(QIcon(f'{PROJECT_SOURCE_PATH_ICONS}/icon_light.png'))

        self.pushButton.clicked.connect(self.ok_pressed)

        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setRowCount(0)
        # ui->tableWidget->verticalHeader()->setSectionResizeMode(QHeaderView::Fixed);
        self.tableWidget: QTableWidget
        self.tableWidget.verticalHeader().setMaximumSize(250, 50 * len(data))
        self.tableWidget.verticalHeader().hide()

        for elem in data:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for i, val in enumerate(elem):
                table_widget_item = QTableWidgetItem(str(val))
                self.tableWidget.setItem(row_position, i, table_widget_item)

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

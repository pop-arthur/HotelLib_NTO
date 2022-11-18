import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidget, QTableWidgetItem, QWidget

from __config__ import *
from utils.database.db import *
from utils.forms import Form

sys._excepthook = sys.excepthook

headers_full = ['ID', 'Название', 'Местонахождение', 'Номер телефона', 'Управляющий', 'Описание']
headers_admins = ['ID', 'ФИО', 'Роль', 'Номер телефона', 'Email']
headers_regions = ['ID', 'Регион']

CONVERTED_TYPES = {
    'INTEGER': int,
    'String': str,
    'VARCHAR': str,
}

HOTEL_MANAGER = Hotel()
ADMIN_MANAGER = Admins()
REGION_MANAGER = Regions()


class HomePage(QWidget):
    def __init__(self):
        super(HomePage, self).__init__()
        uic.loadUi(f'{PROJECT_SOURCE_PATH_UI}/home_page.ui', self)
        self.setWindowTitle("Global Tour")
        self.setWindowIcon(QIcon(f'{PROJECT_SOURCE_PATH_ICONS}/icon_dark.png'))

        # self.pushButton_full.clicked.connect(self.pressed)
        self.pushButton_admins.clicked.connect(self.pressed)
        self.pushButton_regions.clicked.connect(self.pressed)
        self.pushButton_hotels.clicked.connect(self.pressed)

        self.show()

    def pressed(self):
        # if self.sender() == self.pushButton_full:
        #     self.table_view = TableViewWidget(headers_full, HOTEL_MANAGER)
        if self.sender() == self.pushButton_hotels:
            self.table_view = TableViewWidget(headers_full, HOTEL_MANAGER)
        elif self.sender() == self.pushButton_admins:
            self.table_view = TableViewWidget(headers_admins, ADMIN_MANAGER)
        elif self.sender() == self.pushButton_regions:
            self.table_view = TableViewWidget(headers_regions, REGION_MANAGER)

        self.table_view.show()


class TableViewWidget(QDialog):
    def __init__(self, headers: list, table: Unit):
        super(TableViewWidget, self).__init__()

        self.table = table
        self.data = (
            self.table.get_units()
            if type(self.table) is not Hotel else self.table.get_pretty_units()[0]
        )
        self.init_ui(headers)

    def init_ui(self, headers: list):

        uic.loadUi(f'{PROJECT_SOURCE_PATH_UI}/day_data.ui', self)

        self.setWindowTitle('Data')
        self.setWindowIcon(QIcon(f'{PROJECT_SOURCE_PATH_ICONS}/icon_light.png'))

        self.pushButton.clicked.connect(self.ok_pressed)

        self.addButton.clicked.connect(self.add_data)
        self.editButton.clicked.connect(self.add_data)
        self.deleteButton.clicked.connect(self.add_data)

        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        self.tableWidget.setRowCount(0)
        # ui->tableWidget->verticalHeader()->setSectionResizeMode(QHeaderView::Fixed);
        self.tableWidget: QTableWidget
        self.tableWidget.verticalHeader().setMaximumSize(250, 50 * len(self.data))
        self.tableWidget.verticalHeader().hide()

        for elem in self.data:
            row_position = self.tableWidget.rowCount()
            self.tableWidget.insertRow(row_position)
            for i, val in enumerate(elem):
                table_widget_item = QTableWidgetItem(str(val))
                self.tableWidget.setItem(row_position, i, table_widget_item)

    def ok_pressed(self):
        self.close()

    def add_data(self):
        table = self.table.table

        form_data = {
            c.name: (CONVERTED_TYPES.get(str(c.type)) or CONVERTED_TYPES.get(str(c.type)[:str(c.type).find('(')]))
            for c in table.c
        }

        if form_data.get('place_id'):
            form_data['place_id'] = list
        if form_data.get('admin_id'):
            form_data['admin_id'] = list

        if self.sender() == self.addButton:

            del form_data['id']
            self.form = Form(form_data, self.table.__class__.__name__)

        elif self.sender() == self.editButton:

            # TODO запихать в values значения из записи тб
            #  в формате имя столбца: значение для записи

            values = {}
            self.form = Form(form_data, self.table.__class__.__name__, values)
        elif self.sender() == self.deleteButton:

            # TODO запихать в values значения из записи тб
            #  в формате имя столбца: значение для записи

            values = {}
            self.form = Form(form_data, self.table.__class__.__name__, values)

        self.form.show()


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomePage()
    sys.exit(app.exec())

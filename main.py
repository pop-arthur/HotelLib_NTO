import sys

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QDialog, QTableWidget, QTableWidgetItem, QWidget

from __config__ import *
from utils.database.db import *
from utils.forms import Form, DeleteForm

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
        self.headers = headers
        self.init_ui()

    def init_ui(self):

        uic.loadUi(f'{PROJECT_SOURCE_PATH_UI}/day_data.ui', self)

        self.setWindowTitle('Data')
        self.setWindowIcon(QIcon(f'{PROJECT_SOURCE_PATH_ICONS}/icon_light.png'))

        self.pushButton.clicked.connect(self.ok_pressed)

        self.addButton.clicked.connect(self.process_data)
        self.editButton.clicked.connect(self.process_data)
        self.deleteButton.clicked.connect(self.process_data)
        self.init_table()

    def init_table(self):
        data = self.table.get_units()
        if isinstance(self.table, Hotel):
            data = self.table.get_pretty_units()

        self.tableWidget.clear()
        self.tableWidget.setColumnCount(len(self.headers))
        self.tableWidget.setHorizontalHeaderLabels(self.headers)
        self.tableWidget.setRowCount(0)
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

    def process_data(self):
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
            self.form = Form(self, form_data, self.table.__class__.__name__)
            self.form.show()

            if self.form.exec():
                self.init_table()

        elif self.sender() == self.editButton:

            row_number = self.tableWidget.currentRow()
            if not row_number > 0:
                return -1

            row_data = [self.tableWidget.item(row_number, i).text() for i in range(len(self.headers))]

            values = {header: elem for header, elem in zip(list(form_data.keys()), row_data)}
            values['id'] = int(values['id'])
            values['row_number'] = row_number

            self.form = Form(self, form_data, self.table.__class__.__name__, values)
            self.form.show()

            if self.form.exec():
                self.init_table()

        elif self.sender() == self.deleteButton:
            row_number = self.tableWidget.currentRow()
            if not row_number > 0:
                return -1
            row_data = [self.tableWidget.item(row_number, i).text() for i in range(len(self.headers))]
            text = [f"{header}: {value}" for header, value in zip(self.headers, row_data)]
            delete_form = DeleteForm(text)
            if delete_form.exec():
                self.table.delete_unit_by_id(int(row_data[0]))
                self.init_table()


def exception_hook(exctype, value, traceback):
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


sys.excepthook = exception_hook

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = HomePage()
    sys.exit(app.exec())

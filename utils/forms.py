from datetime import datetime
from typing import Dict

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QComboBox, QDateEdit, QDialog, QLabel,
    QPushButton, QSpinBox, QTextEdit, QWidget,
    QDoubleSpinBox
)

from __config__ import PROJECT_SOURCE_PATH_ICONS, PROJECT_SOURCE_PATH_UI
from utils.database.db import Admins, Clients, Entities, Hotel, Regions, Tours

TYPE_TO_WIDGETS = {
    int: QSpinBox, str: QTextEdit,
    list: QComboBox, datetime: QDateEdit,
    float: QDoubleSpinBox
}


class Form(QDialog):
    def __init__(self, parent: QDialog, fields: Dict, form_name: str, values={}, window_title='Форма', headers=[]):
        super(Form, self).__init__()
        self.setWindowTitle(window_title)
        self.headers = headers

        self.fields = {key: TYPE_TO_WIDGETS[value] for key, value in fields.items()}

        self.regions = None
        self.admins = None

        self.parent = parent
        self.values = values

        if self.fields.get('place_id'):
            self.regions = {unit_id: region_name for unit_id, region_name in Regions().get_units()}

        if self.fields.get('admin_id'):
            self.admins = {unit[0]: unit[1] for unit in Admins().get_units()}

        self.form_name = form_name

        self.widget_style = "background-color: #1E1E1E;"
        self.input_widget_style = """
                color: #FFFFFF;
                text-shadow: 0px 0px 50px #FFFFFF;
                background-color: #666666;
                border: 1px solid #fff;
                border-radius: 15px;
                height: 50px;
                width: 300px;
                padding: 10px;
                margin: 10px;
                font-size: 16px;
                """
        self.title_style = """
                color: #FFFFFF;
                text-shadow: 0px 0px 50px #FFFFFF;
                height: 50px;
                width: 300px;
                padding: 10px;
                margin: 10px;
                text-align: center;
                font-size: 24px;
                """
        self.button_style = """	
                text-shadow: 0px 0px 50px #FFFFFF;
                background-color: #6CF1DA;
                border-radius: 15;
                margin: 10px;
                height: 30px;
                font-size: 16px;
                """

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet(self.widget_style)
        self.setGeometry(0, 0, 300, (len(self.fields) + 4) * 70)
        self.setWindowIcon(QIcon(f'{PROJECT_SOURCE_PATH_ICONS}/icon_light.png'))
        self.create_widgets()

    def create_widgets(self):
        self.widgets = dict()

        title = QLabel(self)

        title.setGeometry(0, 0, 300, 70)
        title.setStyleSheet(self.title_style)
        title.setText(self.form_name)

        for i, (name, field) in enumerate(self.fields.items()):

            i += 2
            widget = QWidget(self)
            widget.setGeometry(0, i * 70, 300, 70)
            widget.setStyleSheet(self.widget_style)

            new_field = field(widget)
            new_field.setGeometry(0, 0, 300, 70)
            new_field.setStyleSheet(self.input_widget_style)

            self.widgets[name] = new_field

            if name == 'id':
                new_field.setEnabled(False)

            if self.values != {}:
                if isinstance(new_field, QTextEdit):
                    new_field.setText(self.values.get(name, ''))
                elif isinstance(new_field, QSpinBox):
                    new_field.setValue(self.values.get(name, 0))
                elif isinstance(new_field, QDoubleSpinBox):
                    new_field.setValue(self.values.get(name, 0.0))
                # elif isinstance(new_field, QComboBox):
                #     new_field.setCurrentIndex(self.values['row_number'])

            if type(new_field) is QComboBox:

                data = {}
                if name == 'admin_id':
                    data = {unit[0]: unit[6] for unit in Admins().get_units()}
                elif name == 'place_id':
                    data = {unit_id: region_name for unit_id, region_name in Regions().get_units()}
                elif name == 'hotel_id':
                    data = {unit[0]: unit[1] for unit in Hotel().get_units()}
                elif name == 'entity_id':
                    data = {unit[0]: unit[6] for unit in Entities().get_units()}
                elif name == 'type':
                    if isinstance(self.parent.table, Clients):
                        data = {'legal': 'юридическое  лицо', 'individual': 'физическое лицо'}
                    elif isinstance(self.parent.table, Tours):
                        data = {
                            'without': 'без питания',
                            'with_breakfast': 'С завтраком',
                            'three_times': '3-х разовое',
                        }

                for j, (value_index, value) in enumerate(data.items()):
                    new_field.addItem(value)
                    if value == self.values.get(name):
                        new_field.setCurrentIndex(j)

            if type(new_field) not in [QSpinBox, QDoubleSpinBox, QDateEdit]:
                if 'id' in self.fields.keys():
                    new_field.setPlaceholderText(self.headers[i - 2])
                else:
                    new_field.setPlaceholderText(self.headers[(i - 1)])

        submit = QPushButton(self)
        submit.setGeometry(0, (len(self.fields) + 3) * 70, 300, 70)
        submit.setStyleSheet(self.button_style)
        submit.clicked.connect(self.ok_pressed)
        submit.setText('Подтвердить')

    def ok_pressed(self):

        admins = {elem[6]: elem[0] for elem in Admins().get_units()}
        regions = {elem[1]: elem[0] for elem in Regions().get_units()}
        entities = {elem[3]: elem[0] for elem in Entities().get_units()}
        hotels = {elem[1]: elem[0] for elem in Hotel().get_units()}
        print(hotels)
        tables = {
            'admin_id': admins,
            'place_id': regions,
            'entity_id': entities,
            'hotel_id': hotels,
        }

        data = dict()
        for key, widget in self.widgets.items():
            if isinstance(widget, QTextEdit):
                data[key] = widget.toPlainText()
            elif isinstance(widget, QSpinBox):
                data[key] = widget.value()
            elif isinstance(widget, QDoubleSpinBox):
                data[key] = widget.value()
            elif isinstance(widget, QDateEdit):
                data[key] = datetime.strptime(widget.dateTime().toString('yyyy.MM.dd'), '%Y.%m.%d')
            elif isinstance(widget, QComboBox):
                if key != 'type':
                    data[key] = tables[key][widget.currentText()]
                else:
                    if isinstance(self.parent.table, Clients):
                        data[key] = {'юридическое  лицо': 'legal', 'физическое лицо': 'individual'}[
                            widget.currentText()
                        ]
                    elif isinstance(self.parent.table, Tours):
                        data[key] = {
                            'без питания': 'without',
                            'С завтраком': 'with_breakfast',
                            '3-х разовое': 'three_times'
                        }[widget.currentText()]

        if 'id' in data:
            # edit
            self.parent.table.update_unit_by_id(self.values['id'], data)
            self.accept()
        else:
            self.parent.table.add_unit(data)
            self.accept()


class DeleteForm(QDialog):
    def __init__(self, text):
        super(DeleteForm, self).__init__()
        uic.loadUi(f'{PROJECT_SOURCE_PATH_UI}/form_delete.ui', self)
        self.setWindowTitle('Удалить?')
        self.setWindowIcon(QIcon(f'{PROJECT_SOURCE_PATH_ICONS}/icon_light.png'))

        self.label_data.setText('\n'.join(text))
        self.button_ok.clicked.connect(self.on_click)
        self.button_cancel.clicked.connect(self.on_click)

        self.show()

    def on_click(self):
        if self.sender() == self.button_ok:
            self.accept()
        elif self.sender() == self.button_cancel:
            self.reject()

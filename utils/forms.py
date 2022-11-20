from typing import Dict

from PyQt5 import uic
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QDialog, QLabel, QPushButton, QStyle, QTextEdit, QSpinBox, QComboBox, QWidget

from __config__ import PROJECT_SOURCE_PATH_ICONS, PROJECT_SOURCE_PATH_UI
from utils.database.db import Admins, Regions

TYPE_TO_WIDGETS = {
    int: QSpinBox,
    str: QTextEdit,
    list: QComboBox
}


class Form(QDialog):
    def __init__(self, fields: Dict, form_name: str, values={}):
        super(Form, self).__init__()

        self.fields = {key: TYPE_TO_WIDGETS[value] for key, value in fields.items()}

        self.regions = None
        self.admins = None
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
        self.setWindowTitle('Add Unit')
        self.setGeometry(800, 300, 300, (len(self.fields) + 4) * 70)
        self.setWindowIcon(QIcon(f'{PROJECT_SOURCE_PATH_ICONS}/icon_light.png'))
        self.create_widgets()

    def create_widgets(self):

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

            if name == 'id':
                new_field.setEnabled(False)

            if self.values != {}:
                if isinstance(new_field, QTextEdit):
                    new_field.setText(self.values.get(name, ''))
                elif isinstance(new_field, QSpinBox):
                    new_field.setValue(self.values.get(name, 0))

            if type(new_field) is not QSpinBox:
                new_field: QTextEdit
                new_field.setPlaceholderText(name)

            if type(new_field) is QComboBox:
                if name == 'admin_id':
                    for value_index, value in self.admins.items():
                        new_field.addItem(value)
                elif name == 'place_id':
                    for value_index, value in self.regions.items():
                        new_field.addItem(value)

        submit = QPushButton(self)
        submit.setGeometry(0, (len(self.fields) + 3) * 70, 300, 70)
        submit.setStyleSheet(self.button_style)
        submit.setText('Добавить')

    def ok_pressed(self):
        self.close()


class DeleteForm(QDialog):
    def __init__(self, data):
        super(DeleteForm, self).__init__()
        uic.loadUi(f'{PROJECT_SOURCE_PATH_UI}/form_delete.ui', self)

        self.label_data.setText('\n'.join(data))
        self.button_ok.clicked.connect(self.on_click)
        self.button_cancel.clicked.connect(self.on_click)

        self.show()

    def on_click(self):
        if self.sender() == self.button_ok:
            self.accept()
        elif self.sender() == self.button_cancel:
            self.reject()
        # self.close()
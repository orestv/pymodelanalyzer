# coding=utf-8
from PyQt4.QtCore import pyqtSignal, QLocale

from PyQt4.QtGui import QLabel, QWidget, QGridLayout, QLineEdit, QDoubleValidator, QIntValidator
from gui.filewidget import FileWidget


class ParamsWidget(QWidget):

    updated = pyqtSignal()

    def __init__(self):
        super(ParamsWidget, self).__init__()

        self.model_path = None
        self.excel_path = None

        self.model_file_picker = FileWidget(None, False)
        self.excel_file_picker = FileWidget('*.xlsx', True)
        self.edit_light_speed = QLineEdit()
        self.edit_frequency = QLineEdit()

        self.init_layout()
        self.init_widgets()
        self.init_events()

    def init_widgets(self):
        self.edit_light_speed.setText('299792458')
        self.edit_light_speed.setEnabled(False)

        self.edit_frequency.setText('95')

    def init_layout(self):
        table_layout = QGridLayout()

        table_layout.addWidget(QLabel(u'Файл моделі'), 0, 0)
        table_layout.addWidget(self.model_file_picker, 0, 1)

        table_layout.addWidget(QLabel(u'Файл результату'), 1, 0)
        table_layout.addWidget(self.excel_file_picker, 1, 1)

        table_layout.addWidget(QLabel(u'Швидкість світла, м/с'), 2, 0)
        table_layout.addWidget(self.edit_light_speed, 2, 1)

        table_layout.addWidget(QLabel(u'Частота скануючого сигналу, ГГц'), 3, 0)
        table_layout.addWidget(self.edit_frequency, 3, 1)

        self.setLayout(table_layout)

    def init_events(self):
        self.model_file_picker.selected.connect(self.model_file_selected)
        self.excel_file_picker.selected.connect(self.excel_file_selected)

    def model_file_selected(self, model_path):
        self.model_path = model_path
        self.updated.emit()

    def excel_file_selected(self, excel_path):
        self.excel_path = excel_path
        self.updated.emit()

    def is_params_specified(self):
        return self.model_path is not None and \
            self.excel_path is not None
# coding=utf-8
from PyQt4.QtCore import pyqtSignal, pyqtSlot

from PyQt4.QtGui import QLabel, QWidget, QGridLayout, QLineEdit
from gui.filewidget import FileWidget


LIGHT_SPEED = 299792458


class ParamsWidget(QWidget):

    updated = pyqtSignal()

    def __init__(self):
        super(ParamsWidget, self).__init__()

        self.model_path = None
        self.excel_path = None

        self.model_file_picker = FileWidget('*.obj', False)
        self.excel_file_picker = FileWidget('*.xlsx', True)
        self.edit_light_speed = QLineEdit()
        self.edit_frequency = QLineEdit()
        self.edit_wavelength = QLineEdit()
        self.edit_observation_point_distance = QLineEdit()
        self.edit_observation_point_height = QLineEdit()
        self.edit_observation_rotation_step = QLineEdit()

        self.init_layout()
        self.init_widgets()
        self.init_events()

        self.model_file_picker.set_path('models/t72.obj')
        self.excel_file_picker.set_path('output.xlsx')

    def init_widgets(self):
        self.edit_light_speed.setText('299792458')
        self.edit_light_speed.setEnabled(False)

        self.edit_frequency.setText('95')

        self.edit_wavelength.setEnabled(False)
        self.update_wavelength('95')

        self.edit_observation_point_distance.setText('20')
        self.edit_observation_point_height.setText('2')

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

        table_layout.addWidget(QLabel(u'Довжина хвилі, м'), 4, 0)
        table_layout.addWidget(self.edit_wavelength, 4, 1)

        table_layout.addWidget(QLabel(u'Відстань від ТС до об\'єкта, м'), 5, 0)
        table_layout.addWidget(self.edit_observation_point_distance, 5, 1)

        table_layout.addWidget(QLabel(u'Висота ТС, м'), 6, 0)
        table_layout.addWidget(self.edit_observation_point_height, 6, 1)

        table_layout.addWidget(QLabel(u'Крок повороту ТС, рад'), 7, 0)
        table_layout.addWidget(self.edit_observation_rotation_step, 7, 1)

        self.setLayout(table_layout)

    def init_events(self):
        self.model_file_picker.selected.connect(self.model_file_selected)
        self.excel_file_picker.selected.connect(self.excel_file_selected)
        self.edit_frequency.textChanged.connect(self.update_wavelength)

    def model_file_selected(self, model_path):
        self.model_path = model_path
        self.updated.emit()

    def excel_file_selected(self, excel_path):
        self.excel_path = excel_path
        self.updated.emit()

    def is_params_specified(self):
        return self.model_path is not None and \
            self.excel_path is not None

    def get_params(self):
        frequency = self.edit_frequency.text()
        frequency = float(frequency) * 10 ** 9
        wavelength = LIGHT_SPEED / frequency
        return {'model_path': self.model_path,
                'excel_path': self.excel_path,
                'frequency': frequency,
                'wavelength': wavelength}

    @pyqtSlot(str)
    def update_wavelength(self, frequency):
        if not frequency:
            self.edit_wavelength.setText(str())
            return
        frequency = float(frequency) * 10 ** 9
        wavelength = LIGHT_SPEED / frequency
        wavelength = '%.4f' % wavelength
        self.edit_wavelength.setText(wavelength)
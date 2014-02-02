# coding=utf-8
from PyQt4 import QtGui
from PyQt4.QtCore import Qt
from PyQt4.QtGui import QApplication, QProgressDialog
from geometry import importutils
from gui.calculator import Calculator
from gui.paramswidget import ParamsWidget


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.params = ParamsWidget()
        self.btn_run = QtGui.QPushButton(u"Запустити")

        self.setWindowTitle(u'Аналіз моделі')

        self.init_layout()
        self.init_events()

        self.adjustSize()
        self.move(QApplication.desktop().screen().rect().center()
                  - self.rect().center())

        self.update_widgets_state()

    def init_layout(self):
        vbox_layout = QtGui.QVBoxLayout()

        vbox_layout.addWidget(self.params)
        vbox_layout.addStretch(1)
        vbox_layout.addWidget(self.btn_run)

        self.setLayout(vbox_layout)

    def init_events(self):
        self.params.updated.connect(self.update_widgets_state)
        self.btn_run.clicked.connect(self.calculate)

    def update_widgets_state(self):
        params_ready = self.params.is_params_specified()
        self.btn_run.setEnabled(params_ready)

    def calculate(self):
        params = self.params.get_params()

        model_path = params['model_path']

        self.run_job(u'Імпорт файла...', importutils.get_faces,
                     (model_path,), None)


    def run_job(self, title, target, args, result_handler):
        progress_dialog = QProgressDialog(title, u'Зупинити', 0, 100, self)
        progress_dialog.setWindowModality(Qt.WindowModal)

        calc = Calculator(target=target, args=args)
        calc.updated.connect(progress_dialog.setValue)
        progress_dialog.canceled.connect(calc.cancel)
        calc.start()

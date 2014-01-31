# coding=utf-8
from PyQt4 import QtGui
from gui.paramswidget import ParamsWidget


class MainWindow(QtGui.QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.params = ParamsWidget()
        self.btn_run = QtGui.QPushButton(u"Запустити")

        self.setGeometry(300, 300, 350, 450)
        self.init_widgets()
        self.setWindowTitle(u'Аналіз моделі')

        self.update_widgets_state()

    def init_widgets(self):
        vbox_layout = QtGui.QVBoxLayout()

        vbox_layout.addWidget(self.params)
        vbox_layout.addStretch(1)
        vbox_layout.addWidget(self.btn_run)

        self.setLayout(vbox_layout)

    def update_widgets_state(self):
        params_ready = self.params.is_params_specified()
        self.btn_run.setEnabled(params_ready)

# coding=utf-8
from PyQt4 import QtGui
from PyQt4.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt4.QtGui import QApplication, QProgressDialog
from geometry import importutils
from gui.calculator import Calculator
from gui.paramswidget import ParamsWidget


class MainWindow(QtGui.QWidget):
    label_text_update_require = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.params = ParamsWidget()
        self.btn_run = QtGui.QPushButton(u"Запустити")
        self.progress_dialog = QProgressDialog(u'', u'Зупинити',
                                               0, 100, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)

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
        self.label_text_update_require.connect(self.update_progressdialog_label)

    def update_widgets_state(self):
        params_ready = self.params.is_params_specified()
        self.btn_run.setEnabled(params_ready)

    def calculate(self):
        self.run_job(u'Обробка файла...', self.process)

    def run_job(self, title, target, args=None, result_handler=None):
        self.progress_dialog.setWindowTitle(title)
        self.progress_dialog.setValue(0)

        calc = Calculator(target=target, args=args,
                          clean_up_handler=self.clean_up,
                          result_handler=result_handler)
        calc.updated.connect(self.progress_dialog.setValue)
        self.progress_dialog.canceled.connect(calc.cancel)
        calc.start()

    def clean_up(self, calculator):
        pass
        # self.progress_dialog.canceled.disconnect(calculator.cancel)
        # calculator.updated.disconnect(self.progress_dialog.setValue)

    def process(self, update_percentage=None, check_cancelled=None):
        params = self.params.get_params()
        model_path = params['model_path']

        self.label_text_update_require.emit(u'Імпорт файла... ')
        faces = importutils.get_faces(model_path, update_percentage,
                                      check_cancelled)
        self.label_text_update_require.emit(u'Перетворення трикутників... ')
        triangles = importutils.build_triangles(faces, update_percentage,
                                                check_cancelled)

    @pyqtSlot(str)
    def update_progressdialog_label(self, label):
        self.progress_dialog.setLabelText(label)

    @pyqtSlot(float)
    def update_eta(self, float):
        pass
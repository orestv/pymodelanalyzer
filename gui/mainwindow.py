# coding=utf-8
from PyQt4 import QtGui
import os
import pickle
import time

from PyQt4.QtCore import Qt, pyqtSlot, pyqtSignal
from PyQt4.QtGui import QApplication, QProgressDialog

from geometry import importutils, vector
from gui.calculator import Calculator
from gui.paramswidget import ParamsWidget
from processing import processor


class MainWindow(QtGui.QWidget):
    label_text_update_require = pyqtSignal(str)

    def __init__(self):
        super(MainWindow, self).__init__()

        self.params = ParamsWidget()
        self.btn_run = QtGui.QPushButton(u"Запустити")
        self.progress_dialog = QProgressDialog(u'', u'Зупинити',
                                               0, 100, self)
        self.progress_dialog.setWindowModality(Qt.WindowModal)
        self.progress_dialog.setAutoClose(False)

        self.progress_dialog_base_title = None

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

        self.calc = Calculator(target=target, args=args,
                               clean_up_handler=self.calc_finished,
                               result_handler=result_handler)
        self.calc.updated.connect(self.progress_dialog.setValue)
        self.calc.eta_updated.connect(self.update_eta_label)
        self.calc.finished.connect(self.calc_finished)
        self.progress_dialog.canceled.connect(self.calc.cancel)
        self.calc.start()

    @pyqtSlot()
    def calc_finished(self):
        self.progress_dialog.setAutoClose(True)
        self.progress_dialog.setValue(100)

    def process(self, update_percentage=None, check_cancelled=None):
        params = self.params.get_params()
        model_path = str(params['model_path'])

        filename, extension = os.path.splitext(model_path)
        if extension == '.obj':
            self.prepare_progressdialog(u'Імпорт файла... ')
            faces = importutils.get_faces(model_path, update_percentage,
                                          check_cancelled)
            print 'Faces imported'
            self.prepare_progressdialog(u'Перетворення трикутників... ')
            triangles = importutils.build_triangles(faces, update_percentage,
                                                    check_cancelled)

            self.prepare_progressdialog(u'Корекція моделі... ')
            clean_triangles = importutils.discard_invalid_triangles(triangles,
                                                                    vector.Vector(20, 2, 20),
                                                                    update_percentage,
                                                                    check_cancelled)
            print 'Triangles: %d, clean triangles: %d, diff: %d' % (
                len(triangles), len(clean_triangles), len(triangles) - len(clean_triangles))
            pickle_path = model_path + '.pickle'
            with open(pickle_path, 'wb') as pickle_file:
                try:
                    pickle.dump(clean_triangles, pickle_file, -1)
                    print 'Pickle saved to %s' % pickle_path
                except Exception as e:
                    print 'Failed to save clean triangles list: %s' % e
        elif extension == '.pickle':
            with open(model_path) as pickle_file:
                clean_triangles = pickle.load(pickle_file)
        else:
            raise Exception('Invalid extension %s' % extension)

        triangles = clean_triangles

        self.prepare_progressdialog(u'Обчислення E... ')
        E, sum_cos, sum_sin = processor.calculate_viewpoint_sums(triangles, params['wavelength'],
                                                                 vector.Vector(20, 2, 20),
                                                                 update_percentage, check_cancelled)

    def prepare_progressdialog(self, label):
        self.progress_dialog_base_title = label
        self.label_text_update_require.emit('')
        self.calc.mark_process_time()

    @pyqtSlot(str)
    def update_progressdialog_label(self, label):
        if not label:
            label = self.progress_dialog_base_title
        self.progress_dialog.setLabelText(label)

    @pyqtSlot(float)
    def update_eta_label(self, seconds):
        if seconds == 0:
            self.label_text_update_require.emit('')
            return
        t = time.gmtime(seconds)
        time_string = time.strftime('%M:%S', t)
        label_text = '%s %s' % (self.progress_dialog_base_title,
                                time_string)
        self.label_text_update_require.emit(label_text)
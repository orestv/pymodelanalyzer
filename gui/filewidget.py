# coding=utf-8

import os

from PyQt4.QtCore import pyqtSignal
from PyQt4.QtGui import QWidget, QLabel, QPushButton, QHBoxLayout, QFileDialog


class FileWidget(QWidget):

    selected = pyqtSignal(str)

    def __init__(self, files_filter=None, save=False):
        super(FileWidget, self).__init__()

        self.files_filter = files_filter
        if not self.files_filter:
            self.files_filter = '*.*'
        self.save = save
        self.path = None

        self.label_filename = QLabel('N/A')
        self.button_select = QPushButton(u'Відкрити...')

        self.init_layout()
        self.init_events()

    def init_layout(self):
        layout = QHBoxLayout()

        layout.addWidget(self.label_filename)
        layout.addStretch(1)
        layout.addWidget(self.button_select)

        self.setLayout(layout)

    def init_events(self):
        self.button_select.clicked.connect(self.button_select_clicked)

    def button_select_clicked(self):
        if self.save:
            path = QFileDialog.getSaveFileName(filter=self.files_filter)
        else:
            path = QFileDialog.getOpenFileName(filter=self.files_filter)

        if path:
            path = str(path)
            filename = os.path.basename(path)
            self.label_filename.setText(filename)
            self.selected.emit(path)
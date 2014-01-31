import sys

from PyQt4.QtGui import QApplication
from gui.mainwindow import MainWindow

__author__ = 'ovol'

if __name__ == '__main__':
    app = QApplication(sys.argv)

    w = MainWindow()
    w.show()

    app.exec_()
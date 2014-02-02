from PyQt4.QtGui import QWidget, QProgressBar


class ProgressWidget(QWidget):
    def __init__(self):
        super(ProgressWidget, self).__init__()

        self.progress_bar = QProgressBar

        self.init_layout()
        self.init_events()

    def init_layout(self):
        pass

    def init_events(self):
        pass
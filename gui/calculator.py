from threading import Event, Thread
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot


class Calculator(QObject):
    updated = pyqtSignal(float)
    eta_updated = pyqtSignal(float)

    def __init__(self, target=None, args=()):
        super(Calculator, self).__init__()

        self.target = target
        self.args = args

        self.running = True
        self.evt_updated = Event()
        self.percentage = 0

        Thread(target=self.thread_update).start()

    @pyqtSlot()
    def cancel(self):
        self.running = False
        self.evt_updated.set()

    def cancelled(self):
        return not self.running

    def thread_update(self):
        while self.running:
            self.evt_updated.wait()
            self.evt_updated.clear()
            if self.running:
                self.updated.emit(self.percentage)

    def update(self, percentage):
        self.percentage = percentage
        self.evt_updated.set()

    def start(self):
        self.running = True
        args = self.args + (self.update, self.cancelled)
        t = Thread(target=self.target, args=args)
        t.start()
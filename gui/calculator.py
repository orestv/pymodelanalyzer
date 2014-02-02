from threading import Event, Thread
from PyQt4.QtCore import QObject, pyqtSignal, pyqtSlot


class InterruptException(Exception):
    pass


class Calculator(QObject):
    updated = pyqtSignal(float)
    eta_updated = pyqtSignal(float)

    def __init__(self, target=None, args=None, clean_up_handler=None,
                 result_handler=None):
        super(Calculator, self).__init__()

        self.target = target
        self.args = args
        if self.args is None:
            self.args = ()
        self.result_handler = result_handler
        self.clean_up_handler = clean_up_handler
        self.time_per_percent = None

        self.running = True
        self.evt_updated = Event()
        self.percentage = 0

        Thread(target=self.thread_update).start()

    @pyqtSlot()
    def cancel(self):
        print 'calculator - cancel'
        self.running = False
        self.evt_updated.set()

    def check_cancelled(self):
        if not self.running:
            print 'Exception raised!'
            raise InterruptException()

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
        t = Thread(target=self.run)
        t.start()

    def clean_up(self):
        if self.clean_up_handler:
            self.clean_up_handler(self)
        self.time_per_percent = None
        if self.running:
            self.update(100)
        self.running = False

    def run(self):
        args = self.args + (self.update, self.check_cancelled)
        try:
            result = self.target(*args)
            success = True
        except InterruptException:
            success = False
        finally:
            self.clean_up()
        if success and self.result_handler:
            self.result_handler(result)

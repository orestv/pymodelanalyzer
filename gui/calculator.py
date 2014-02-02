from threading import Thread
import time

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
        self.start_time = None

        self.running = True
        self.percentage = 0

    @pyqtSlot()
    def cancel(self):
        print 'calculator - cancel'
        self.running = False

    def check_cancelled(self):
        if not self.running:
            print 'Exception raised!'
            raise InterruptException()

    def calculate_time_per_percent(self, percentage):
        time_passed = time.time() - self.start_time
        self.time_per_percent = time_passed / percentage

    def update(self, percentage):
        self.updated.emit(self.percentage)
        self.percentage = percentage
        if percentage > 5:
            self.calculate_time_per_percent(percentage)
        if self.time_per_percent:
            time_left = self.time_per_percent * (100 - percentage)
            self.eta_updated.emit(time_left)
        else:
            self.eta_updated.emit(0)

    def start(self):
        self.running = True
        t = Thread(target=self.run)
        self.mark_process_time()
        t.start()

    def clean_up(self):
        if self.clean_up_handler:
            self.clean_up_handler(self)
        self.time_per_percent = None
        if self.running:
            self.update(100)
        self.running = False

    def mark_process_time(self):
        self.start_time = time.time()

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

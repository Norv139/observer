import threading


class MyThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self, *args, **kwargs):
        super(MyThread, self).__init__(*args, **kwargs)
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()

    def stopped(self):
        return self._stop.is_set()

class CreateInfiniteLoop(MyThread):

    def __init__(self, fn):
        self.fn = fn
        self.practicethread = MyThread(target=self.infinite_loop_method)

    def start_practice(self):
        self.practicethread.start()

    def stop_practice(self):
        self.practicethread.stop()

    def infinite_loop_method(self):
        # print(self.practicethread.stopped())
        while not self.practicethread.stopped():
            self.fn()

    # #This doesn't seem to work and I am still stuck in the loop

    # def infinite_stop(self):
    #     if self.practicethread.isAlive():
    #         self.practicethread.stop()

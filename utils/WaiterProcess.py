import threading
import time


class WaiterProcess:
    def __init__(self, callback):
        self._variable = None
        self._lock = threading.Lock()
        self._change_event = threading.Event()
        self._stop_event = threading.Event()
        self._callback = callback
        self._thread = threading.Thread(target=self._watch_variable)
        self._thread.start()

    def set_variable(self, value):
        with self._lock:
            self._variable = value
            self._change_event.set()

    def stop(self):
        self._stop_event.set()
        self._change_event.set()
        self._thread.join()

    def _watch_variable(self):
        while not self._stop_event.is_set():
            self._change_event.wait()
            if self._stop_event.is_set():
                break

            self._change_event.clear()

            while True:
                time.sleep(1)
                with self._lock:
                    if self._change_event.is_set():
                        self._change_event.clear()
                    else:
                        self._callback()
                        break

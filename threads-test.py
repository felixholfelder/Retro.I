import threading
import time

class VariableWatcher:
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
            print(f"Variable changed to: {value}")
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
                time.sleep(2)
                with self._lock:
                    if self._change_event.is_set():
                        print("Variable changed within 2 seconds, restarting timer.")
                        self._change_event.clear()
                    else:
                        self._callback()
                        break

if __name__ == "__main__":
    def my_callback():
        print("2 seconds passed without change. Executing the callback function.")

    watcher = VariableWatcher(my_callback)

    try:
        while True:
            new_value = input("Enter new value for the variable (or 'stop' to end): ")
            watcher.set_variable(new_value)
    finally:
        watcher.stop()

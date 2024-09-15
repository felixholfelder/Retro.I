import threading
import time
from adafruit_led_animation.color import GREEN

class StripProcess:
	def __init__(self, animation):
		self._variable = None
		self._lock = threading.Lock()
		self._change_event = threading.Event()
		self._stop_event = threading.Event()
		self._callback = callback
		self._thread = threading.Thread(target=self.run_color(GREEN, animation)
		self._thread.start()

	def set_variable(self, value):
		with self._lock:
			self._variable = value
			self._change_event.set()
	
	def stop(self):
		self._stop_event.set()
		self._change_event.set()
		self._thread.join()
	
	def run_color(self, color, animation):
		while not self._stop_event.is_set():
			self._change_event.wait()
			if self._stop_event.is_set():
				break

			self.animation.animate()
			
			self._change_event.clear()

			while True:
				with self._lock:
					if self._change_event.is_set():
						self._change_event.clear()
					else:
						self._callback()
						break

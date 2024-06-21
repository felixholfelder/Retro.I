import threading
import board
import neopixel
import math
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import BLACK, GREEN, RED
from colors import ColorHelper
from WaiterProcess import WaiterProcess
from Constants import Constants

c = Constants()

class Strip:
	counter = 0
	curr_color = GREEN

	color_helper = ColorHelper()

	pixel_pin = board.D10
	pixel_num = 50

	pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=1, auto_write=True)
	animation = Pulse(pixels, min_intensity=0.1, speed=0.1, period=5, color=BLACK)

	def __init__(self):
		self.pixels.fill(GREEN)
		self.pixels.show()

	def callback(self):
		if not self.is_strip_active():
			self.animation.fill(BLACK)
		else:
			self.animation.resume()
		self.pixels.show()

	wait_proc = WaiterProcess(callback)

	def start(self):
		self.wait_proc = WaiterProcess(self.callback)

	def update_sound_strip(self, value):
		print(value)
		self.animation.freeze()

		self.wait_proc.set_variable(value)

		amount_pixels = math.floor((self.pixel_num) * (value / 100))
		self.pixels.fill(BLACK)
		if (amount_pixels == 0 and value > 0):
			self.pixels[0] = GREEN

		for i in range(amount_pixels):
			self.pixels[i] = GREEN

		self.pixels.show()

	def toggle_mute(self, is_mute):
		if self.is_strip_active():
			if is_mute:
				self.animation.freeze()
				self.pixels.fill(RED)
				self.pixels.show()
			else:
				self.animation.resume()
				self.pixels.show()

	def update_strip(self, color):
		strip_color = self.color_helper.toRgb(color)
		self.curr_color = strip_color
		self.animation.color = strip_color
		while (self.counter <= 1):
			try:
				self.animation.animate()
			except:
				pass

		self.kill_proc()

	def is_strip_active(self):
		lines = self.get_strip_settings()
		return bool(lines[0])

	def toggle_strip(self):
		if self.is_strip_active():
			self.animation.fill(BLACK)
			self.animation.freeze()
			self.update_settings(0, self.get_curr_brightness())
		else:
			self.animation.fill(self.curr_color)
			self.animation.resume()
			self.update_settings(1, self.get_curr_brightness())
		self.pixels.show()

	def get_curr_brightness(self):
		lines = self.get_strip_settings()
		return int(lines[1]) * 100

	def change_brightness(self, value):
		self.pixels.brightness = value / 100
		self.pixels.show()

	def fill(self, color):
		self.pixels.fill(color)

	def run(self, color):
		proc = threading.Thread(target=self.update_strip(color))
		proc.start()

	def kill_proc(self):
		self.counter -= 1

	def disable(self):
		self.animation.color=BLACK
		self.animation.reset()

	def get_strip_settings(self):
		lines = []
		with open(f"{c.pwd()}/settings/led-settings.csv", 'r') as file:
			lines = file.readlines()[0]

		return lines

	def update_settings(self, is_active, brightness):
		with open(f"{c.pwd()}/settings/led-settings.csv", 'w') as file:
			file.write(f"{int(is_active)};{brightness}")

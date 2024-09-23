import threading
import board
import neopixel
import math
import decimal
import csv
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import BLACK, GREEN, RED
from helper.ColorHelper import ColorHelper
from utils.WaiterProcess import WaiterProcess
from helper.Constants import Constants

c = Constants()

class Strip:
	counter = 0
	curr_color = GREEN

	color_helper = ColorHelper()

	pixel_pin = board.D10
	pixel_num = 62

	pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0, auto_write=True)
	animation = Pulse(pixels, min_intensity=0.1, speed=0.1, period=5, color=BLACK)

	def __init__(self):
		self.pixels.fill(GREEN)
		self.pixels.brightness = self.get_curr_brightness() / 100
		self.pixels.show()
		self.start()

	def callback(self):
		if not self.is_strip_active():
			self.animation.fill(BLACK)
		else:
			self.animation.resume()
		self.pixels.show()

	wait_proc = WaiterProcess(callback)

	def start(self):
		self.wait_proc = WaiterProcess(self.callback)
		self.animation.color = self.curr_color

	def update_sound_strip(self, value):
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
				self.pixels.fill(self.curr_color)
				self.animation.resume()
				self.pixels.show()

	def update_strip(self, color):
		self.counter = self.counter + 1

		strip_color = self.color_helper.toRgb(color)
		self.curr_color = strip_color
		self.animation.color = strip_color
		self.pixels.show()
		while (self.counter <= 1):
			try:
				self.animation.animate()
			except:
				pass

		self.kill_proc()

	def is_strip_active(self):
		lines = self.get_strip_settings()
		return bool(int(lines[0]))

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
		return float(lines[1])

	def change_brightness(self, e):
		value = e.control.value
		self.pixels.brightness = value / 100
		self.pixels.show()
		self.update_settings(self.is_strip_active(), float(round(value, 2)))

	def fill(self, color):
		if not self.is_strip_active():
			self.pixels.fill(color)

	def run(self, color):
		proc = threading.Thread(target=self.update_strip(color))
		proc.start()

	def kill_proc(self):
		self.counter -= 1

	def disable(self):
		self.pixels.fill(BLACK)
		self.animation.color=BLACK
		self.animation.reset()
		self.pixels.show()

	def get_strip_settings(self):
		line = ""
		with open(f"{c.pwd()}/settings/strip-settings.csv", newline='') as csvfile:
			reader = csv.reader(csvfile, delimiter=';', quotechar=' ')
			for row in reader:
				return row

	def update_settings(self, is_active, brightness):
		with open(f"{c.pwd()}/settings/strip-settings.csv", 'w', newline='') as csvfile:
			writer = csv.writer(csvfile, delimiter=';', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
			writer.writerow([int(is_active), brightness])

		with open(f"{c.pwd()}/settings/strip-settings.csv", 'w') as file:
			file.write(f"{int(is_active)};{brightness}")

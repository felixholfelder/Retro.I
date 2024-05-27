from multiprocessing import Process
import board
import neopixel
from adafruit_led_animation.animation.pulse import Pulse
from adafruit_led_animation.color import BLACK
from colors import ColorHelper

class Strip:
	counter = 0

	color_helper = ColorHelper()

	pixel_pin = board.D10
	pixel_num = 8
	
	pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=1, auto_write=True)
	animation = Pulse(pixels, min_intensity=0.1, speed=0.1, period=5, color=BLACK)

	def update_strip(self, color):
		strip_color = self.color_helper.toRgb(color)
		self.animation.color=strip_color
		while (self.counter <= 1):
			self.animation.animate()

		self.kill_proc()

	def run(self, color):
		proc = Process(target=self.update_strip(color))
		proc.start()

	def kill_proc(self):
		self.counter -= 1
	
	def disable(self):
		self.animation.color=BLACK
		self.animation.reset()

from PIL import ImageColor
from colorthief import ColorThief

class ColorHelper:
	def toRgb(self, hex_value):
		return ImageColor.getcolor(hex_value, "RGB")
	
	def extract_color(self, img_src):
		ct = ColorThief(img_src)
		palette = ct.get_palette(color_count=5)

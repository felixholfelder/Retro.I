from PIL import ImageColor
from colorthief import ColorThief

class ColorHelper:
	def toRgb(self, hex_value):
		return ImageColor.getcolor(hex_value, "RGB")
	
	def extract_color(self, img_src):
		ct = ColorThief(img_src)
		color = ct.get_color(quality=1)
		return f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}"
			

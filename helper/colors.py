from PIL import ImageColor

class ColorHelper:
	def toRgb(self, hex_value):
		return ImageColor.getcolor(hex_value, "RGB")

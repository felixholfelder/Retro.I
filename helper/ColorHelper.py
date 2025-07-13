from PIL import Image, ImageColor
import numpy as np
import cairosvg
from sklearn.cluster import KMeans
import requests
from io import BytesIO

tmp_path = "/tmp/output.png"

class ColorHelper:	
	def toRgb(self, hex_value):
		return ImageColor.getcolor(hex_value, "RGB")
	
	def extract_color(self, img_src):
		if img_src == "":
			return "#46a94b"
		
		if ".svg".upper() not in img_src.upper():
			response = requests.get(img_src)
			img = Image.open(BytesIO(response.content))
		else:
			cairosvg.svg2png(url=img_src, write_to=tmp_path)
			img = Image.open(tmp_path)

		img = img.convert("RGB")
		img_array = np.array(img)

		pixels = img_array.reshape((-1, 3))

		kmeans = KMeans(n_clusters=1)
		kmeans.fit(pixels)

		dominant_color = kmeans.cluster_centers_[0].astype(int)

		return f"#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}".upper()

	def get_navbar_icon_color(self, theme_color):
		color = theme_color[1:]

		hex_red = int(color[0:2], base=16)
		hex_green = int(color[2:4], base=16)
		hex_blue = int(color[4:6], base=16)

		if (hex_red*0.299 + hex_green*0.587 + hex_blue*0.114) > 186:
			return "#000000"

		return "#ffffff"

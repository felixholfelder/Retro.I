from PIL import Image
import numpy as np
from sklearn.cluster import KMeans
import requests
from io import BytesIO

def extract_color(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))

    img = img.convert("RGB")
    img_array = np.array(img)

    pixels = img_array.reshape((-1, 3))

    kmeans = KMeans(n_clusters=1)
    kmeans.fit(pixels)

    dominant_color = kmeans.cluster_centers_[0].astype(int)

    return f"#{dominant_color[0]:02x}{dominant_color[1]:02x}{dominant_color[2]:02x}".upper()
print(extract_color("https://play.you.radio/static/assets/img/apple-icon-120x120.png"))
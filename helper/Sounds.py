import json
import os
import random
import re
import struct

from helper.Constants import Constants

try:
	import urllib2
except ImportError:  # Python 3
	import urllib.request as urllib2

c = Constants()


class Sounds:
	def load_sounds(self):
		f = open(f"{c.pwd()}/assets/sounds.json")
		data = json.load(f)
		f.close()
		return data

	def get_random_toast(self):
		directory = c.toast_path()
		try:
			files = [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
			return random.choice(files)
		except FileNotFoundError:
			return "Directory not found."

	def get_song_info(self, url):
		encoding = 'utf-8'
		request = urllib2.Request(url, headers={'Icy-MetaData': 1})
		response = urllib2.urlopen(request)
		# print(response.headers, file=sys.stderr)
		metaint = int(response.headers['icy-metaint'])
		for _ in range(10):
			response.read(metaint)
			metadata_length = struct.unpack('B', response.read(1))[0] * 16
			metadata = response.read(metadata_length).rstrip(b'\0')
			m = re.search(br"StreamTitle='([^']*)';", metadata)
			if m:
				title = m.group(1)
				if title:
					titleString = title.decode(encoding, errors='replace')
					try:
						artist, title = titleString.split(" - ")
					except _:
						artist, title = titleString.split(": ")

					return artist, title
		else:
			return "", ""


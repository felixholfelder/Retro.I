import alsaaudio as audio


class Audio:
	def mixer(self):
		return audio.Mixer()

	def update_sound(self, value):
		if value >= 0 and value <= 100:
			self.mixer().setvolume(value)

	def mute(self):
		self.mixer().setmute(1)

	def unmute(self):
		self.mixer().setmute(0)
	
	def get_volume(self):
		print(self.mixer().getvolume()[0])
		return self.mixer().getvolume()[0]

	def toggle_mute(self):
		if self.mixer().getmute()[0] == 0:
			self.mute()
			return True
		self.unmute()
		return False

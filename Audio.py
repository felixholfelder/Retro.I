import alsaaudio as audio

class Audio:
	def mixer():
		return audio.Mixer()
		
		
	def update_sound(_, value):
		audio.Mixer().setvolume(value)


	def mute():
		audio.Mixer().setmute(1)


	def unmute():
		audio.Mixer().setmute(0)


	def toggle_mute(self):
		if audio.Mixer().getmute() == 0:
			self.mute()
			return True
		self.unmute()
		return True

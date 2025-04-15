import subprocess
import json
from helper.Constants import Constants

c = Constants()

class AudioEffects:
	effects_path = f"{c.pwd()}/assets/effects/effects"

	def __init__(self):
		pass

	def start(self):
		self.update_effects()
		command = ['easyeffects', '--gapplication-service']
		subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

	def stop(self):
		command = ['pkill', 'easyeffects']
		subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

	def get_config(self):
		f = open(f"{self.effects_path}.json")
		data = json.load(f)
		f.close()
		return data

	def get_bass_value(self):
		config = self.get_config()
		return config['output']['bass_enhancer#0']['amount']

	def get_pitch_value(self):
		config = self.get_config()
		return config['output']['pitch#0']['semitones']

	def update_bass(self, value):
		config = self.get_config()
		config['output']['bass_enhancer#0']['amount'] = value

		self.write_config(config)
		self.update_effects()

	def update_pitch(self, value):
		config = self.get_config()
		config['output']['pitch#0']['semitones'] = value

		self.write_config(config)
		self.update_effects()

	def write_config(self, config):
		with open(f"{self.effects_path}.json", "r+") as file:
			file_data = config
			json.dump(file_data, file, indent=4)

	def update_effects(self):
		command = ['easyeffects', '-l', self.effects_path]
		subprocess.run(command, stdout=subprocess.PIPE).stdout.decode('utf-8').strip()

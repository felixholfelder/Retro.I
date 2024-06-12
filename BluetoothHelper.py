import os
import subprocess
from multiprocessing import Process

class BluetoothHelper:
	discovery_on = False
	
	def is_discovery_on(self):
		return self.discovery_on

	def toggle_bluetooth_discovery(self, page):
		if self.discovery_on:
			self.bluetooth_discovery_off()
		else:
			self.bluetooth_discovery_on()

		page.update()
		return self.discovery_on

	def bluetooth_discovery_on(self):
		os.system('bluetoothctl discoverable on')
		self.discovery_on = True

	def bluetooth_discovery_off(self):
		os.system('bluetoothctl discoverable off')
		self.discovery_on = False

	def disconnect(self):
		address = self.get_device_mac()
		process = Process(target=lambda: os.system(f'bluetoothctl disconnect {address}'))
		process.start()
		
	def get_device(self):
		return subprocess.run(['bluetoothctl', 'devices', 'Connected'], stdout=subprocess.PIPE).stdout.decode('utf-8')
	
	def get_device_name(self):
		result = self.get_device()
		return result[25:]
	
	def get_device_mac(self):
		result = self.get_device()
		return result[7:24]
		

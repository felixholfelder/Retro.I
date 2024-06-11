import os

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

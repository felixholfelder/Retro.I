import os

class BluetoothHelper:
	discovery_on = False
	
	def is_discovery_on(self):
		return self.discovery_on

	def toggle_bluetooth_discovery(self):
		if self.discovery_on:
			return self.bluetooth_discovery_off
		return self.bluetooth_discovery_on

	def bluetooth_discovery_on(self):
		os.system('bluetoothctl discoverable on')
		return True
        
	def bluetooth_discovery_off(self):
		os.system('bluetoothctl discoverable off')
		return False

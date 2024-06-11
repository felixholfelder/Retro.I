import bluetooth
from bluetooth import *

def get_devices():
    print("Searching for devices...")
    devices = discover_devices(lookup_names=True)
    return devices

def select_device(devices):
    print("Available devices:")
    for idx, device in enumerate(devices):
        print(f"{idx}: {device[1]} - {device[0]}")

    selection = int(input("Select a device by number: "))
    return devices[selection]

def connect_device(address):
    port = 4  # Standard port for RFCOMM
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((address, port))
    return sock

def main():
    devices = get_devices()
    if not devices:
        print("No devices found. Exiting...")
        return

    selected_device = select_device(devices)
    print(f"Connecting to {selected_device[1]} - {selected_device[0]}")

    sock = None

    try:
        sock = connect_device(selected_device[0])
        print("Connected successfully.")

        while True:
            data = input("Enter data to send (or 'exit' to quit): ")
            if data == "exit":
                break
            sock.send(data)
            response = sock.recv(1024)
            print(f"Received: {response}")

    except bluetooth.btcommon.BluetoothError as err:
        print(f"An error occurred: {err}")
    finally:
        sock.close()

if __name__ == "__main__":
    main()

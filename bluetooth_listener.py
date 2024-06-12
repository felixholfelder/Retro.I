import dbus
import dbus.mainloop.glib
from gi.repository import GLib

def device_event_handler(*args, **kwargs):
    for arg in args:
        if isinstance(arg, dbus.String):
            device_path = str(arg)
            if "dev_" in device_path:
                if kwargs.get('member') == "InterfacesAdded":
                    print(f"Device connected: {device_path}")
                elif kwargs.get('member') == "InterfacesRemoved":
                    print(f"Device disconnected: {device_path}")

def main():
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    bus.add_signal_receiver(
        device_event_handler,
        dbus_interface="org.freedesktop.DBus.ObjectManager",
        signal_name="InterfacesAdded"
    )

    bus.add_signal_receiver(
        device_event_handler,
        dbus_interface="org.freedesktop.DBus.ObjectManager",
        signal_name="InterfacesRemoved"
    )

    loop = GLib.MainLoop()
    print("Listening for Bluetooth connection events...")
    loop.run()

if __name__ == "__main__":
    main()

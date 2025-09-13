#!/bin/bash

plymouth_shutdown_file="/usr/lib/systemd/system/plymouth-poweroff.service"
replacement="--mode=reboot"

sudo cp -rf "$RETROI_DIR/assets/splashscreen/splash.png" "/usr/share/plymouth/themes/pix/splash.png"
sudo update-initramfs -u

sudo sed -i "s/--mode=shutdown/$replacement/" "$plymouth_shutdown_file" > /dev/null 2>&1

if ! grep -- "$replacement" "$plymouth_shutdown_file"; then
  echo "Shutdown-Bild konnte nicht ausgetauscht werden!" >&2
  return 1
fi

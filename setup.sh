#!/bin/sh

# System-Einrichtung

# TODO - cooles ASCII-Art zu Beginn :D

# Splashscreen entfernen
printf "Entferne Splashscreen... "

fireware_config_path=/boot/firmware/config.txt
disable_splash_command="disable_splash=1"

firware_config=$(grep "^$disable_splash_command$" "$firmware_config_path")

if [ "$firmware_config" != "$disable_splash_command" ]; then
  sudo sh -c "echo '#Disable splashscreen' >> fireware_config_path"
  sudo sh -c "echo '$disable_splash' >> fireware_config_path"
fi

printf "ERFOLGREICH\n"

# Plymouth: Bild beim Systemstart ändern (in eigene Datei)
printf "Plymouth Bild bei Systemstart ändern... "

cp -rf /home/pi/Documents/Retro.I/assets/splashscreen/splash.png /usr/share/plymouth/themes/pix/splash.png
sudo update-initramfs -u

printf "ERFOLGREICH\n"

# Plymouth - Bild beim Shutdown anzeigen
printf "Plymouth Bild bei Shutdown zeigen... "

sed 's/ExecStart=\/usr\/sbin\/plymouthd --mode=shutdown --attach-to-session/ExecStart=\/usr\/sbin\/plymouthd --mode=reboot --attach-to-session/' /usr/lib/systemd/system/plymouth-poweroff.service

printf "ERFOLGREICH\n"

# Autostart-Datei erstellen
printf "Erstelle Autostart-Datei... "

sudo echo "[Desktop Entry]" > /etc/xdg/autostart/retroi.desktop
sudo echo "Name=Retro.I" >> /etc/xdg/autostart/retroi.desktop
sudo echo "Type=Application" >> /etc/xdg/autostart/retroi.desktop
sudo echo "Exec=sh /home/pi/Documents/Retro.I/scripts/start.sh" >> /etc/xdg/autostart/retroi.desktop
sudo echo "Terminal=true" >> /etc/xdg/autostart/retroi.desktop

printf "ERFOLGREICH\n"

# Taskbar ausblenden
printf "Taskbar ausblenden... "

wf_panel_path=/home/pi/.config/wf-panel-pi.ini
wf_panel_config=$(grep "^autohide=true$" "$wf_panel_path")

if [ "$wf_panel_config" != "autohide_true" ]; then
  echo "#Hide taskbar" >> wf_panel_path
  echo "autohide=true" >> wf_panel_path
  echo "autohide_duration=500" >> wf_panel_path
fi

printf "ERFOLGREICH\n"

# TODO - Hintergrund entfernen

# SSH aktivieren
printf "Aktiviere SSH... "
sudo raspi-config nonint do_ssh 0
printf "ERFOLGREICH\n"

# VNC aktivieren
printf "Aktiviere VNC... "
sudo raspi-config nonint do_vnc 0
printf "ERFOLGREICH\n"

# SPI aktivieren
printf "Aktiviere SPI... "
sudo raspi-config nonint do_spi 0
printf "ERFOLGREICH\n"

# easyeffects installieren
printf "Installiere easyeffects... "
sudo apt-get install easyeffects -y

# Fehlenden config order erstellen
mkdir -p /home/pi/.config/easyeffects/output

# TODO - easyeffects config nach /home/pi/.config/easyeffects/output/retroi.json kopieren
sudo cp /home/pi/Documents/Retro.I/assets/effects/effects.json /home/pi/.config/easyeffects/output/retroi.json

printf "ERFOLGREICH\n"

# Bildschirm-Tastatur installieren
printf "Installiere Bildschirmtastatur... "
sudo apt install wvkbd
printf "ERFOLGREICH\n"

printf "Systemeinrichtung abgeschlossen! Weiter mit App-Einrichtung... "

# System-Einrichtung abgeschlossen!

# Weiter mit App-Einrichtung:

# .venv einrichten (python -m venv /home/pi/Documents/Retro.I/.venv)
printf "VENV einrichten... "
python -m venv /home/pi/Documents/Retro.I/.venv

# ~.bashrc anpassen, dass bei jedem Terminalstart .venv gestartet wird
bashrc_path=/home/pi/.bashrc
bashrc_config=$(grep "^.venv/bin/activate" "$wf_panel_path")

if [ "$bashrc_config" != "autohide_true" ]; then
  echo "#Activate venv" >> bashrc_path
  echo "cd /home/pi/Documents/Retro.I" >> bashrc_path
  echo "source .venv/bin/activate" >> bashrc_path
fi

printf "ERFOLGREICH\n"

# Pakete für alsaaudio installieren
printf "Installiere Pakete für alsaaudio... "
sudo apt-get install libasound2-dev -y
printf "ERFOLGREICH\n"

# Pakete für flet-ui installieren
printf "Installiere Pakete für flet-ui... "

sudo apt install libmpv-dev mpv -y

# Symlink erstellen - für flet-ui
sudo ln -s /usr/lib/aarchlinux-gnu/libmpv.so /usr/lib/aarchlinux-gnu/libmpv.so.1

printf "ERFOLGREICH\n"

# TODO - User fragen, wie viele LED's sein LED-Streifen hat
# -> Mit Hinweis "Wichtig für Animation der Lautstärke"

# pip install -r requirements.txt
printf "Installiere Python-Pakete... "
pip install -r requirements.txt

printf "ERFOLGREICH\n"

printf "Setup erfolgreich abgeschlossen!"

# TODO - cooles ASCII-Art zum Ende :D

# App-Einrichtung abgeschlossen!
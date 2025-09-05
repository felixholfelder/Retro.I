#!/bin/sh

GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

success() {
  echo -e "${GREEN}$1${NC}"
}

error() {
  echo -e "${RED}$1${NC}"
}

run_step() {
  DESCRIPTION="$1"
  shift
  COMMAND="$@"

  echo -n "$DESCRIPTION ... "

  if $COMMAND > /dev/null 2>&1; then
    success "ERFOLGREICH"
  else
    error "FEHLGESCHLAGEN"
  fi
}

# System-Einrichtung
remove_splashscreen() {
  fireware_config_path="/boot/firmware/config.txt"
  disable_splash_command="disable_splash=1"

  if ! grep -qxF "$disable_splash_command" "$firmware_config_path"; then
    sudo sh -c "echo '# Disable splashscreen' >> '$fireware_config_path'"
    sudo sh -c "echo '$disable_splash_command' >> '$fireware_config_path'"
  fi
}

change_plymouth_pic() {
  sudo cp -rf /home/pi/Documents/Retro.I/assets/splashscreen/splash.png /usr/share/plymouth/themes/pix/splash.png
  sudo update-initramfs -u
}

show_plymouth_pic_on_shutdown() {
  sudo sed -i 's/--mode=shutdown/--mode=reboot/' /usr/lib/systemd/system/plymouth-poweroff.service > /dev/null 2>&1
}

create_autostart_file() {
  autostart_path="/etc/xdg/autostart/retroi.desktop"

  if [ ! -e "$autostart_path" ]; then
    sudo touch "$autostart_path"

    sudo echo "[Desktop Entry]" > $autostart_path
    sudo echo "Name=Retro.I" >> $autostart_path
    sudo echo "Type=Application" >> $autostart_path
    sudo echo "Exec=sh /home/pi/Documents/Retro.I/scripts/start.sh" >> $autostart_path
    sudo echo "Terminal=true" >> $autostart_path
  fi
}

hide_taskbar() {
  wf_panel_path=/home/pi/.config/wf-panel-pi.ini
  wf_panel_config=$(grep "^autohide=true$" "$wf_panel_path")

  if [ "$wf_panel_config" != "autohide_true" ]; then
    echo "#Hide taskbar" >> wf_panel_path
    echo "autohide=true" >> wf_panel_path
    echo "autohide_duration=500" >> wf_panel_path
  fi
}

remove_background_image() {
  # TODO - Hintergrund entfernen
  echo ""
}

install_easyeffects() {
  sudo apt-get install easyeffects -y -qqq

  # Fehlenden config order erstellen
  mkdir -p /home/pi/.config/easyeffects/output

  # TODO - easyeffects config nach /home/pi/.config/easyeffects/output/retroi.json kopieren
  sudo cp /home/pi/Documents/Retro.I/assets/effects/effects.json /home/pi/.config/easyeffects/output/retroi.json
}

setup_venv() {
  python -m venv /home/pi/Documents/Retro.I/.venv

  # ~.bashrc anpassen, dass bei jedem Terminalstart .venv gestartet wird
  bashrc_path=/home/pi/.bashrc
  bashrc_config=$(grep "^.venv/bin/activate" "$wf_panel_path")

  if [ "$bashrc_config" != "autohide_true" ]; then
    echo "#Activate venv" >> bashrc_path
    echo "cd /home/pi/Documents/Retro.I" >> bashrc_path
    echo "source .venv/bin/activate" >> bashrc_path
  fi
}

setup_alsaaudio() {
  sudo apt-get install libasound2-dev -y -qqq
}

setup_fletui() {
  sudo apt install libmpv-dev mpv -y -qqq

  # Symlink erstellen - für flet-ui
  sudo ln -s -f /usr/lib/aarch64-linux-gnu/libmpv.so /usr/lib/aarch64-linux-gnu/libmpv.so.1
}

install_python_packages() {
  pip install -r requirements.txt -q
}

# TODO - cooles ASCII-Art zu Beginn :D

# Splashscreen entfernen
run_step "Entferne Splashscreen" remove_splashscreen

# Plymouth: Bild beim Systemstart ändern (in eigene Datei)
run_step "Plymouth Bild bei Systemstart ändern" change_plymouth_pic

# Plymouth - Bild beim Shutdown anzeigen
run_step "Plymouth Bild bei Shutdown zeigen" show_plymouth_pic_on_shutdown

# Autostart-Datei erstellen
run_step "Erstelle Autostart-Datei" create_autostart_file

# Taskbar ausblenden
run_step "Taskbar ausblenden" hide_taskbar

run_step "Hintergrund entfernen" remove_background_image

# SSH aktivieren
run_step "Aktiviere SSH" sudo raspi-config nonint do_ssh 0

# VNC aktivieren
run_step "Aktiviere VNC" sudo raspi-config nonint do_vnc 0

# SPI aktivieren
run_step "Aktiviere SPI" sudo raspi-config nonint do_spi 0

# easyeffects installieren
run_step "Installiere easyeffects" install_easyeffects

# Bildschirm-Tastatur installieren
run_step "Installiere Bildschirmtastatur" sudo apt-get install wvkbd -qq

# System-Einrichtung abgeschlossen!
success "Systemeinrichtung abgeschlossen!"

# Weiter mit App-Einrichtung:
printf "\nWeiter mit App-Einrichtung...\n"

# .venv einrichten (python -m venv /home/pi/Documents/Retro.I/.venv)
run_step "VENV einrichten" setup_venv

# Pakete für alsaaudio installieren
run_step "Installiere Pakete für alsaaudio" setup_alsaaudio

# Pakete für flet-ui installieren
run_step "Installiere Pakete für flet-ui" setup_fletui

# TODO - User fragen, wie viele LED's sein LED-Streifen hat
# -> Mit Hinweis "Wichtig für Animation der Lautstärke"

# pip install -r requirements.txt
run_step "Installiere Python-Pakete" install_python_packages

success "Setup erfolgreich abgeschlossen!\n"

# TODO - cooles ASCII-Art zum Ende :D

# App-Einrichtung abgeschlossen!
#!/bin/sh

GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

success() {
  echo "${GREEN}$1${NC}"
}

error() {
  echo "${RED}$1${NC}"
}

run_step() {
  DESCRIPTION="$1"
  shift
  COMMAND="$@"

  echo -n "$DESCRIPTION ... "

  # Capture output and exit code
  OUTPUT=$($COMMAND 2>&1)
  STATUS=$?

  if [ $STATUS -eq 0 ]; then
    success "ERFOLGREICH"
  else
    error "FEHLGESCHLAGEN"
    echo "↳ $OUTPUT" >&2
  fi
}

# System-Einrichtung
remove_splashscreen() {
  firmware_config_path="/boot/firmware/config.txt"
  disable_splash_command="disable_splash=1"

  # Check if file exists
  if [ ! -f "$firmware_config_path" ]; then
    echo "Config file not found: $firmware_config_path" >&2
    return 1
  fi

  if ! grep -- "$disable_splash_command" "$firmware_config_path"; then
    sudo sh -c "echo '# Disable splashscreen' >> '$firmware_config_path'"
    sudo sh -c "echo '$disable_splash_command' >> '$firmware_config_path'"
  fi
}

change_plymouth_pic() {
  plymouth_shutdown_file="/usr/lib/systemd/system/plymouth-poweroff.service"
  replacement="--mode=reboot"

  sudo cp -rf /home/pi/Documents/Retro.I/assets/splashscreen/splash.png /usr/share/plymouth/themes/pix/splash.png
  sudo update-initramfs -u

  sudo sed -i "s/--mode=shutdown/$replacement/" "$plymouth_shutdown_file" > /dev/null 2>&1

  if ! grep -- "$replacement" "$plymouth_shutdown_file"; then
    echo "Shutdown-Bild konnte nicht ausgetauscht werden!" >&2
    return 1
  fi
}

create_autostart_file() {
  autostart_path="/etc/xdg/autostart/retroi.desktop"
  header="[Desktop Entry]"

  sudo tee "$autostart_path" > /dev/null <<EOF
[Desktop Entry]
Name=Retro.I
Type=Application
Exec=sh -c '/home/pi/Documents/Retro.I/scripts/start.sh >> /home/pi/autostart.log 2>&1'
Terminal=true
EOF

  # Verify creation
  if ! grep -q -- "^\[Desktop Entry\]" "$autostart_path"; then
    echo "Autostart file could not be created correctly!" >&2
    return 1
  fi
}

hide_taskbar() {
  wf_panel_path=/home/pi/.config/wf-panel-pi.ini

  sudo tee "$wf_panel_path" > /dev/null <<EOF
# Hide taskbar
[panel]
autohide=true
autohide_duration=500
heightwhenhidden=0
EOF

  # Verify creation
  if ! grep -q -- "autohide=true" "$wf_panel_path"; then
    echo "Hiding taskbar failed!" >&2
    return 1
  fi
}

remove_background_image() {
  # TODO - Hintergrund entfernen
  echo ""
}

install_easyeffects() {
  project_preset="/home/pi/Documents/Retro.I/assets/effects/effects.json"
  preset="/home/pi/.config/easyeffects/output/retro.json"

  sudo apt-get install easyeffects -y -qqq

  # Fehlenden config order erstellen
  mkdir -p /home/pi/.config/easyeffects/output

  sudo cp "$project_preset" "$preset"
  sudo chmod 644 "$preset"

  # Verify installation and preset copy
  if [ ! -f "$preset" ]; then
    echo "Preset file not found" >&2
    return 1
  fi

  if easyeffects -l retroi >/dev/null 2>&1; then
    echo "Preset retroi detected"
  else
    echo "Warning: preset retroi not yet recognized by easyeffects" >&2
    # Don’t fail the whole step
  fi
}

install_screen_keyboard() {
  sudo apt-get install wvkbd -y -qqq

  # Verify installation
  wvkbd-mobintl -L 1&
  pkill wvkbd-mobintl
}

setup_venv() {
  VENV_PATH="/home/pi/Documents/Retro.I/.venv"
  BASHRC_PATH="/home/pi/.bashrc"

  # Create virtual environment
  python -m venv "$VENV_PATH"

  # Ensure the .venv directory exists
  if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment creation failed!" >&2
    return 1
  fi

  # Append venv activation to .bashrc if not already present
  if ! grep -q "source $VENV_PATH/bin/activate" "$BASHRC_PATH"; then
    cat <<'EOF' >> "$BASHRC_PATH"

# venv for Retro.I
cd /home/pi/Documents/Retro.I
source /home/pi/Documents/Retro.I/.venv/bin/activate
EOF
  fi

  # Verify that the snippet was added
  if ! grep -q "source $VENV_PATH/bin/activate" "$BASHRC_PATH"; then
    echo "Activating venv in .bashrc failed!" >&2
    return 1
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

#run_step "Entferne Splashscreen" remove_splashscreen
#run_step "Plymouth Bild bei Systemstart ändern" change_plymouth_pic
#run_step "Erstelle Autostart-Datei" create_autostart_file
#run_step "Taskbar ausblenden" hide_taskbar
#run_step "Hintergrund entfernen" remove_background_image
#run_step "Aktiviere SSH" sudo raspi-config nonint do_ssh 0
#run_step "Aktiviere VNC" sudo raspi-config nonint do_vnc 0
#run_step "Aktiviere SPI" sudo raspi-config nonint do_spi 0
#run_step "Installiere easyeffects" install_easyeffects
#run_step "Installiere Bildschirmtastatur" install_screen_keyboard

success "Systemeinrichtung abgeschlossen!"
printf "\nWeiter mit App-Einrichtung...\n"

#run_step "VENV einrichten" setup_venv
#run_step "Installiere Pakete für alsaaudio" setup_alsaaudio
#run_step "Installiere Pakete für flet-ui" setup_fletui

# TODO - User fragen, wie viele LED's sein LED-Streifen hat
# -> Mit Hinweis "Wichtig für Animation der Lautstärke"

run_step "Installiere Python-Pakete" install_python_packages

success "Setup erfolgreich abgeschlossen!\n"

# TODO - cooles ASCII-Art zum Ende :D

# App-Einrichtung abgeschlossen!
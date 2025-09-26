#!/bin/bash

GREEN="\033[0;32m"
RED="\033[0;31m"
NC="\033[0m"

success() {
  echo -e "${GREEN}$1${NC}"
}

error() {
  echo -e "${RED}$1${NC}"
}

spinner() {
  local pid=$1
  local delay=0.1
  local spinstr='|/-\'
  while kill -0 $pid 2>/dev/null; do
    for i in $(seq 0 3); do
      printf "\r%s ... (%c)" "$DESCRIPTION" "${spinstr:$i:1}"
      sleep $delay
    done
  done
  printf "\r%s ...     " "$DESCRIPTION"  # overwrite spinner with spaces
}

run_step() {
  DESCRIPTION="$1"
  shift
  COMMAND="$@"

  # Run command in background, capture stdout+stderr
  OUTPUT_FILE=$(mktemp)
  ($COMMAND >"$OUTPUT_FILE" 2>&1) &
  cmd_pid=$!

  # Show spinner while command runs
  spinner $cmd_pid
  wait $cmd_pid
  STATUS=$?

  OUTPUT=$(cat "$OUTPUT_FILE")
  rm "$OUTPUT_FILE"

  if [ $STATUS -eq 0 ]; then
    printf "\r%s ... " "$DESCRIPTION"
    success "ERFOLGREICH"
  else
    printf "\r%s ... " "$DESCRIPTION"
    error "FEHLGESCHLAGEN"
    echo "❌ $OUTPUT" >&2
  fi
}

# System-Einrichtung
set_project_path() {
  printf "Projektpfad setzen ... "
  BASHRC_PATH="$HOME/.bashrc"
  ENV_PATH="/etc/environment"
  current_path=$(pwd)

  if [[ "$current_path" != *Retro* ]]; then
    error "FEHLGESCHLAGEN"
    echo "Du befindest dich im falschen Pfad. Wechsle zuerst in das \"Retro.I\" Verzeichnis" >&2
    exit 1
  fi

  export RETROI_DIR="$current_path"

  # Append venv activation to .bashrc if not already present
  if ! grep -q "export RETROI_DIR=\"$current_path\"" "$BASHRC_PATH"; then
    cat <<EOF >> "$BASHRC_PATH"
export RETROI_DIR="$current_path"
EOF
  fi

  sudo tee "$ENV_PATH" > /dev/null <<EOF
RETROI_DIR="$current_path"
EOF

  source "$ENV_PATH"

  if [ -z "$RETROI_DIR" ]; then
    error "FEHLGESCHLAGEN"
    echo "Pfad-Variablen konnten nicht gesetzt werden" >&2
    return 1
  fi

  success "ERFOLGREICH"
}

remove_splashscreen() {
  firmware_config_path="/boot/firmware/config.txt"
  disable_splash_command="disable_splash=1"
  boot_delay_command="boot_delay=0"

  # Check if file exists
  if [ ! -f "$firmware_config_path" ]; then
    echo "Config file not found: $firmware_config_path" >&2
    return 1
  fi

  if ! grep -- "$disable_splash_command" "$firmware_config_path"; then
    sudo sh -c "echo '# Disable splashscreen' >> '$firmware_config_path'"
    sudo sh -c "echo '$disable_splash_command' >> '$firmware_config_path'"
    sudo sh -c "echo '$boot_delay_command' >> '$firmware_config_path'"
  fi
}

apply_audio_group() {
  sudo usermod -aG audio $USER
}

create_systemd_service() {
  systemd_path="/etc/systemd/system/retroi.service"

  user_id=$(id -u)

  sudo tee "$systemd_path" > /dev/null <<EOF
[Unit]
Description=Retro.I Desktop App
After=graphical.target

[Service]
Type=simple
User=pi
Group=pi
WorkingDirectory=$RETROI_DIR
ExecStart=$RETROI_DIR/.venv/bin/python $RETROI_DIR/main.py
Restart=no
Environment=DISPLAY=:0
Environment=XAUTHORITY=/home/pi/.Xauthority
Environment=XDG_RUNTIME_DIR=/run/user/$user_id
Environment=PULSE_SERVER=unix:/run/user/$user_id/pulse/native
TimeoutStopSec=1
KillSignal=SIGKILL
KillMode=control-group

[Install]
WantedBy=graphical.target
EOF

  # Verify creation
  if ! grep -q -- "^\[Service\]" "$systemd_path"; then
    echo "Systemd file could not be created correctly!" >&2
    return 1
  fi

  sudo systemctl enable retroi.service
}

hide_taskbar() {
  wf_panel_path="$HOME/.config/wf-panel-pi.ini"

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
  pcmanfm --set-wallpaper "" --wallpaper-mode=color

  mkdir -p "$HOME/.config/pcmanfm"

  pcmanfm --reconfigure
  sleep 0.5

  CONFIG_FILES=$(find "$HOME/.config/pcmanfm" -type f -name "desktop-items-*.conf" 2>/dev/null)

  if [ -z "$CONFIG_FILES" ]; then
    echo "No pcmanfm desktop config files found." >&2
    return 1
  fi

  for CONFIG_FILE in $CONFIG_FILES; do
    # Set background color to black
    if grep -q "^desktop_bg=" "$CONFIG_FILE"; then
      sed -i 's/^desktop_bg=.*/desktop_bg=#000000/' "$CONFIG_FILE"
    else
      echo "desktop_bg=#000000" >> "$CONFIG_FILE"
    fi
  done

  pcmanfm --reconfigure
}

remove_trash_basket() {
  CONFIG_FILES=$(find "$HOME/.config/pcmanfm" -type f -name "desktop-items-*.conf" 2>/dev/null)

  if [ -z "$CONFIG_FILES" ]; then
    echo "No pcmanfm desktop config files found." >&2
    return 1
  fi

  for CONFIG_FILE in $CONFIG_FILES; do
    echo "Processing $CONFIG_FILE"

    # Make a backup first
    cp "$CONFIG_FILE" "$CONFIG_FILE.bak"

    # Ensure section exists and disable trash
    for key in show_trash show_home show_documents show_mounts; do
      if grep -q "^$key=" "$CONFIG_FILE"; then
        sed -i "s/^$key=.*/$key=0/" "$CONFIG_FILE"
      else
        echo "$key=0" >> "$CONFIG_FILE"
      fi
    done

    # Verify the change
    if ! grep -q "^show_trash=0" "$CONFIG_FILE"; then
      echo "Failed to update $CONFIG_FILE" >&2
      return 1
    fi
  done

  # Reload pcmanfm so changes take effect
  if command -v pcmanfm >/dev/null 2>&1; then
    pcmanfm --reconfigure || {
      echo "Warning: Could not reload pcmanfm automatically" >&2
    }
  fi

  pcmanfm --reconfigure
}

deactivate_services() {
  sudo systemctl disable NetworkManager-wait-online.service
  sudo systemctl disable e2scrub_reap.service
  sudo systemctl disable ModemManager.service
  sudo systemctl disable rpi-eeprom-update.service
}

install_easyeffects() {
  project_preset="$RETROI_DIR/assets/effects/effects.json"
  preset="$HOME/.config/easyeffects/output/retroi.json"

  sudo apt-get install easyeffects -y -qqq

  # Fehlenden config order erstellen
  mkdir -p "$HOME/.config/easyeffects/output"

  sudo cp "$project_preset" "$preset"
  sudo chmod 777 "$preset"

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
  VENV_PATH="$RETROI_DIR/.venv"
  BASHRC_PATH="$HOME/.bashrc"

  # Create virtual environment
  python -m venv "$VENV_PATH"

  # Ensure the .venv directory exists
  if [ ! -d "$VENV_PATH" ]; then
    echo "Virtual environment creation failed!" >&2
    return 1
  fi

  # Append venv activation to .bashrc if not already present
  if ! grep -q "source $VENV_PATH/bin/activate" "$BASHRC_PATH"; then
    cat <<EOF >> "$BASHRC_PATH"
# venv for Retro.I
cd $RETROI_DIR
source $VENV_PATH/bin/activate
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
  sudo apt-get update

  if ! sudo apt-get install libmpv-dev mpv -y -qqq; then
    echo "Installation von libmpv-dev/mpv fehlgeschlagen!" >&2
    return 1
  fi

  # Symlink erstellen
  TARGET="/usr/lib/aarch64-linux-gnu/libmpv.so"
  LINK="/usr/lib/aarch64-linux-gnu/libmpv.so.1"

  if [ ! -f "$TARGET" ]; then
    echo "Zielbibliothek $TARGET existiert nicht!" >&2
    return 1
  fi

  sudo ln -s -f "$TARGET" "$LINK"

  # Prüfen, ob Symlink korrekt gesetzt ist
  if [ ! -L "$LINK" ]; then
    echo "Symlink $LINK konnte nicht korrekt erstellt werden!" >&2
    return 1
  fi
}

install_python_packages() {
  source "$RETROI_DIR/.venv/bin/activate" && pip install -r requirements.txt -q
}

enter_led_length() {
  while true; do
    settings_file="$RETROI_DIR/settings/strip-settings.csv"
    IFS=';' read -r is_active brightness count_led < "$settings_file"

    read -p "Anzahl der LED's des LED-Streifens ($count_led): " led_input

    if [ "$led_input" == "" ]; then
      printf "%s;%s;%s" "$is_active" "$brightness" "$count_led" > "$settings_file"
      break
    fi

    if [[ "$led_input" =~ ^[0-9]+$ ]]; then
      printf "%s;%s;%s" "$is_active" "$brightness" "$led_input" > "$settings_file"
      break
    else
      echo "Bitte eine gültige Zahl eingeben!"
    fi
  done
}

enter_led_length() {
  while true; do
    settings_file="settings/strip-settings.csv"
    IFS=';' read -r is_active brightness count_led < "$settings_file"

    read -p "Anzahl der LED's des LED-Streifens ($count_led): " led_input

    if [ "$led_input" == "" ]; then
      printf "%s;%s;%s" "$is_active" "$brightness" "$count_led" > "$settings_file"
      break
    fi

    if [[ "$led_input" =~ ^[0-9]+$ ]]; then
      printf "%s;%s;%s" "$is_active" "$brightness" "$led_input" > "$settings_file"
      break
    else
      echo "Bitte eine gültige Zahl eingeben!"
    fi
  done
}

print_ascii_art() {
  echo "
 _______  _______  _________ _______  _______    _________
(  ____ )(  ____ \ \__   __/(  ____ )(  ___  )   \__   __/
| (    )|| (    \/    ) (   | (    )|| (   ) |      ) (
| (____)|| (__        | |   | (____)|| |   | |      | |
|     __)|  __)       | |   |     __)| |   | |      | |
| (\ (   | (          | |   | (\ (   | |   | |      | |
| ) \ \__| (____/\    | |   | ) \ \__| (___) | _ ___) (___
|/   \__/(_______/    )_(   |/   \__/(_______)(_)\_______/
                                                                 "
}

clear

print_ascii_art
echo -e "Sollte dieses Setup-Script bei einem Schritt fehlschlagen, kannst du im Projekt in der SETUP.md nachschlagen.\n\n"
read -p "Drücke <ENTER> um das Setup zu beginnen..."

set_project_path
run_step "Entferne Splashscreen" remove_splashscreen
run_step "System-Splashscreen ändern" sudo -E bash -c "$RETROI_DIR/update-system-splash.sh"
run_step "User zur \"audio\" Gruppe hinzufügen" apply_audio_group
run_step "Systemd-Datei für Systemstart erstellen" create_systemd_service
run_step "Taskbar ausblenden" hide_taskbar
run_step "Hintergrund entfernen" remove_background_image
run_step "Mülleimer entfernen" remove_trash_basket
run_step "Aktiviere SSH" sudo raspi-config nonint do_ssh 0
run_step "Aktiviere VNC" sudo raspi-config nonint do_vnc 0
run_step "Aktiviere SPI" sudo raspi-config nonint do_spi 0
run_step "Deaktiviere unnötige Services" deactivate_services
run_step "Installiere easyeffects" install_easyeffects
run_step "Installiere Bildschirmtastatur" install_screen_keyboard

success "\nSystemeinrichtung abgeschlossen!\n"
printf "\nWeiter mit App-Einrichtung...\n"

run_step "VENV einrichten" setup_venv
run_step "Installiere Pakete für alsaaudio" setup_alsaaudio
run_step "Installiere Pakete für flet-ui" setup_fletui

run_step "Installiere Python-Pakete" install_python_packages

enter_led_length

success "Setup erfolgreich abgeschlossen!\n\n"

print_ascii_art

echo "Retro.I neustarten, um Setup abzuschließen..."

while true; do
  read -p "Retro.I neustarten? [J]a, [N]ein: " choice
  case "$choice" in
    j|J )
      sudo reboot
      break
      ;;
    n|N )
      echo "Kein Neustart."
      break
      ;;
    * )
      echo "Bitte gib entweder \"J\" oder \"N\" ein!"
      ;;
  esac
done

# App-Einrichtung abgeschlossen!

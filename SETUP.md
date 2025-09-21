# Setup
Hier findest du Informationen zum Setup-Skript (`setup.sh`)

> Manchmal empfiehlt es sich einfach, das Skript noch einmal zu starten!

## Systemeinrichtung
### Projektpfad setzen
In der Datei `/etc/environment` wird die Variable `RETROI_DIR` auf den Pfad des geklonten Projekts gesetzt.
mit dem Befehl `source "/etc/environment"` wird die Umgebungsvariable global gesetzt und für die folgenden Schritte verwendet!

### Entferne Splashscreen
Hier wird in der Datei `/boot/firmware/config.txt`, wenn noch nicht vorhanden, die Zeile `disable_splash=1` hinzugefügt!

### System-Splashscreen ändern
Hierfür gibt es ein eigenes Skript, solltest du den System-Splashscreen ändern wollen.
Allerdings ist es zu empfehlen, dass du das gleiche Bild unter `$RETROI_DIR/assets/splashscreen/splash.png` ablegst, damit das Skript das Bild an die richtige Stelle kopieren kann.\
Das Bild wird nach `/usr/share/plymouth/themes/pix/splash.png` kopiert.\
Durch den Befehl
```
sudo update-initramfs -u
```
wird das Bild systemweit aktualisiert.\
Im Plymouth Poweroff-Service muss eine Kleinigkeit ausgetauscht werden, damit das Bild nicht nur beim Reboot, sondern auch beim Herunterfahren angezeigt wird.\
In der Datei `/usr/lib/systemd/system/plymouth-poweroff.service` muss `--mode=shutdown` durch `--mode=reboot` ersetzt werden.\
Klingt nach einer Art "Trick-17"... Aber es funktioniert ;)

### Erstelle Autostart-Datei
Damit die Software nach dem Systemstart von selbst startet, muss eine Autostart-Datei angelegt werden.\
Unter `/etc/xdg/autostart/retroi.desktop` wird folgendes hinzugefügt:
```
[Desktop Entry]
Name=Retro.I
Type=Application
Exec=sh -c '$RETROI_DIR/scripts/start.sh >> $HOME/autostart.log 2>&1'
Terminal=true
```

### Taskbar ausblenden
Die Datei `$HOME/.config/wf-panel-pi.ini` wird angepasst und folgendes hinzugefügt:
```
# Hide taskbar
[panel]
autohide=true
autohide_duration=500
heightwhenhidden=0
```

### Hintergrund entfernen
Das Hintergrundbild des Desktop's wird entfernt und die Hintergrundfarbe auf Schwarz gestellt.\
Sollte dies nicht funktionieren, kann das Skript erneut ausgeführt werden oder händisch über die Einstellungen der Hintergrund geändert werden.
Ausgeführte Befehle:
```
pcmanfm --set-wallpaper "" --wallpaper-mode=color
```

und in den conf-Dateien unter `$HOME/.config/pcmanfm`
```
desktop_bg=#000000
```
setzen.

### Mülleimer entfernen
In den conf-Dateien in `$HOME/.config/pcmanfm` werden folgende Zeilen hinzugefügt/geändert:
```
show_trash=0
show_home=0
show_documents=0
show_mounts=0
```
Diese entfernen unnötige Icon's vom Desktop.

### Aktiviere SSH
Es wird SSH aktiviert

### Aktiviere VNC
Es wird VNC aktiviert. Speziell für Debugging hilfreich.

### Aktiviere SPI
Es wird SPI aktiviert. Die ist notwendig, damit der LED-Streifen über den GPIO-Pin 10 richtig verwendet werden kann!

### Deaktiviere unnötige Services
Es werden unnötige Services, welche nicht benötigt werden, deaktiviert, um den Boot-Prozess zu beschleunigen:
```
sudo systemctl disable NetworkManager-wait-online.service
sudo systemctl disable e2scrub_reap.service
sudo systemctl disable ModemManager.service
sudo systemctl disable rpi-eeprom-update.service
```

### Installiere easyeffects
Mit diesem Tool kann der Bass und die Höhen eingestellt werden.
Wird mit folgendem Befehl installiert
```
sudo apt-get intsall easyeffects
```
Im Projekt befindet sich unter `assets/effects` die Datei `effects.json`.\
Diese wird nach erfolgreicher Installation nach `$HOME/.config/easyeffects/output/retroi.json` kopiert.\
Das Programm passt diese Datei entsprechend eingestellten Bass und Höhen an und lädt die Konfigurationen neu.

### Installiere Bildschirmtastatur
Für die Verwendung eines Touch-Displays wird eine Bildschirmtastatur benötigt.
Diese wird mit folgendem dem Befehl
```
sudo apt-get install wvkbd -y -qqq
```
Gestartet wird die Tastatur mit folgendem Befehl `wvkbd-mobintl`
Mit Strg+C wird die Tastatur geschlossen.

## App-Einrichtung
### VENV einrichten
Mit dem Befehl
```
python -m venv "$RETROI_DIR/.venv"
```
wird venv als virtuelles Environment angelegt.\
In diesem werden später alle Python-Pakete installiert und müssten somit nicht direkt systemweit, sondern in dieser virtuellen Umgebung, installiert werden.
Zusätzlich, wird die `.bashrc` angepasst, damit bei jedem Start eines Terminals in den Projektordner gewechselt und die virtuelle Umgebung gestartet wird:
```
# venv for Retro.I
cd /home/pi/Documents/Retro.I
source /home/pi/Documents/Retro.I/.venv/bin/activate
```

### Installiere Pakete für alsaaudio
Für alsaaudio wird das Paket `libasound2-dev` benötigt:
```
sudo apt-get install libasound2-dev -y -qqq
```

### Installiere Pakete für flet-ui
Für flet-ui als UI-Framework werden zwei weitere Pakete benötigt:
```
sudo apt install libmpv-dev mpv -y -qqq
```
Zusätzlich muss ein Symlink erstellt werden, damit flet-ui richtig starten kann:
```
sudo ln -s -f "/usr/lib/aarch64-linux-gnu/libmpv.so" "/usr/lib/aarch64-linux-gnu/libmpv.so.1"
```

### Installiere Python-Pakete
Zuletzt müssen alle Python-Pakete aus der `requirements.txt` **in venv** installiert werden:
```
source "$RETROI_DIR/.venv/bin/activate" && pip install -r requirements.txt -q
```

### Eingabe Länge LED-Streifen
In diesem Schritt wird die Anzahl der LED's des LED-Streifens eingegeben. \
Die eingegebene Zahl wird in die Datei `$RETROI_DIR/settings/strip-settings.csv` an Stelle 3 (Index 2) geschrieben. \
Die genaue Angabe ist für verschiedene Animationen mit dem Streifen notwendig. \
Sollte kein LED-Streifen verbaut sein, kann die Zahl beliebig gewählt werden.

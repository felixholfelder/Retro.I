# Retro.I
Ein Projekt der FWI1 des BSZ-Wiesau\
Einem Radio aus den 1950er/1960er Jahren wird neues Leben eingehaucht!\
Dazu werden folgende Technologien verwendet:
* Raspberry PI 4 (4GB)
* Python
* Circuitpython
* Flet

Folgende Hardware wurde verwendet:
* WS2812B LED-Streifen
* Rotary Drehregler
* 4 Passiv-Lautsprecher
* Touch-Display

## How to
Der Radio wurde zu einem Internetradio umgebaut. Die Auswahl der Radiosender erfolgt über ein Touch-Display, welches oben auf dem Radio eingelassen wurde.

## Konfigurationen
## Retro.I Image beim Start
Beim Start wird ein Bild angezeigt. Das Bild liegt unter `/usr/share/plymouth/themes/pix/splash.png` und hat die exakte Größe für das Touch Display.
Das Bild ist außerdem im Projektordner unter `assets/splashscreen/splash.png`.
Um das Bild zu generieren, muss ein Befehl ausgeführt werden: `sudo update-initramfs -u`.
Um den Rainbow-Splashscreen zu deaktivieren, muss in der Datei `/boot/firmare/config.txt` die Option `disable_splash=1` vorhanden sein.

[//]: # (## HifiBerry)

[//]: # (In der Datei `/boot/firmare/config.txt` müssen folgende Optionen auskommentiert werden:)

[//]: # (- `dtparam=audio=on`)

[//]: # ()
[//]: # (folgenden Block finden:)

[//]: # (```)

[//]: # (# Enable DRM VC4 V3D driver)

[//]: # (dtoverlay=vc4-kms-v3d)

[//]: # (max_framebuffers=2)

[//]: # (```)

[//]: # ()
[//]: # (und folgenden Befehl darunter einfügen:)

[//]: # (- `dtoverlay=vc4-kms-v3d,noaudio`)

[//]: # ()
[//]: # (damit der Block am Ende so aussieht:)

[//]: # (```)

[//]: # (# Enable DRM VC4 V3D driver)

[//]: # (dtoverlay=vc4-kms-v3d)

[//]: # (max_framebuffers=2)

[//]: # (# Also for HifiBerry...)

[//]: # (dtoverlay=vc4-kms-v3d,noaudio)

[//]: # (```)

[//]: # ()
[//]: # (Und folgenden Block einfügen:)

[//]: # (```)

[//]: # ([all])

[//]: # (# For the Hifiberry AMP 2)

[//]: # (force_eeprom_read = 0)

[//]: # (dtoverlay=hifiberry-dacplus)

[//]: # (# dtoverlay=hifiberry-dacplus-std)

[//]: # (```)

[//]: # ()
[//]: # (Außerdem muss die Datei /etc/assound.conf mit folgendem Inhalt erstellt werden:)

[//]: # (```)

[//]: # (pcm.!default {)

[//]: # (  type hw card 0)

[//]: # (})

[//]: # (ctl.!default {)

[//]: # (  type hw card 0)

[//]: # (})

[//]: # (```)
<hr>

## Taskbar ausblenden
Um die Taskbar auszublenden müssen die folgenden Zeilen in der Datei `/home/pi/.config/wf-panel-pi.ini` hinzugefügt werden:\
```
autohide=true
autohide_duration=500
```
<hr>

## On-Screen Keyboard
Um per Touch Eingaben zu tätigen, muss ein On-Screen Keyboard installiert werden.\
Mit den folgenden Befehlen, kann die Tastatur installiert werden:
```
sudo apt install wvkbd
```
Durch entsprechende Kommandos kann die Tastatur nun sichtbar/unsichtbar gemacht werden.
<hr>

## Autostart
### Start der Anwendung
Die Anwendung zur Steuerung des Radio's wird automatisch nach dem Boot des Raspberry's gestartet (`start.sh`)\
Der Aufruf des Start-Skripts erfolgt über eine Desktop-Datei (`retroi.desktop`). Diese liegt im Ordner `/etc/xdg/autostart`.\
Inhalt von `retroi.desktop`:
```
[Desktop Entry]
Name=Retro.I
Type=Application
Exec=sh /home/pi/Documents/Retro.I/scripts/start.sh
Terminal=false
```
## Packages
### Pulseaudio
Das Programm verwendet Pulseaudio für die Audioausgabe. Hierzu müssen folgende Pakete installiert werden:
```
sudo apt-get install python3-alsaaudio
sudo apt-get install alsaaudio
sudo apt-get install python-alsaaudio
```
### SPI
Über `sudo raspi-config` muss in den `Interface Options` SPI aktiviert werden.

### Updates
Bei jedem Boot des Raspberry's wird ein Update-Skript (`update.sh`) ausgeführt.\
Dieses Skript prüft, ob neue Updates verfügbar sind, indem es die aktuelle Tag-Version auf dem Raspberry mit dem neuesten Tag im Github-Repo vergleicht.\
Ist ein neues Update für die Anwendung verfügbar wird der neueste Tag heruntergeladen.

## Lautstärke
Die Lautstärkenregelung erfolgt über den original Drehknopf des Radios!\
Der Rotary Drehregler gibt sein Signal an den Raspberry weiter und dieser steuert die Lautstärke des Geräts.

## Stummschaltung
Der Wechsel von Stummschaltung/Aufhebung erfolgt über Drücken des gleichen Drehreglers wie zur Veränderung der Lautstärke.

## WS2812B LED-Streifen
Der LED-Streifen mit `62` LED's wird ebenfalls über den Raspberry angesteuert.\
Jeder Radiosender verfügt über eine Farbe, welche den Radiosender repräsentiert. Diese Farbe wird bei Auswahl des jeweiligen Radiosenders auf dem Streifen in einer Animation angezeigt.

## Verwendung der GPIO-Pin's
### Rotary Drehregler:
* `5` - SW-PIN: Stummschaltung/Aufhebung Stummschaltung
* `6` - DT-PIN: Verringerung der Lautstärke
* `13` - CLK-PIN: Erhöhung der Lautstärke

### LED-Streifen:
* `10` - Datenpin für Ansteuerung des WS2812B LED-Streifens

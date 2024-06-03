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
* HiFiBerry
* 2 Lautsprecher
* Touch-Display

## How to
Der Radio wurde zu einem Internetradio umgebaut. Die Auswahl der Radiosender erfolgt über ein Touch-Display, welches oben auf dem Radio eingelassen wurde.

## Autostart
### Start der Anwendung
Die Anwendung zur Steuerung des Radio's wird automatisch nach dem Boot des Raspberry's gestartet (`start.sh`)\
Der Aufruf des Start-Skripts erfolgt über eine Desktop-Datei (`retroi.desktop`). Diese liegt im Ordner `/etc/xdg/autostart`.

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
Der LED-Streifen mit `7` LED's wird ebenfalls über den Raspberry angesteuert.\
Jeder Radiosender verfügt über eine Farbe, welche den Radiosender repräsentiert. Diese Farbe wird bei Auswahl des jeweiligen Radiosenders auf dem Streifen in einer Animation angezeigt.

## Verwendung der GPIO-Pin's
### Rotary Drehregler:
* `26` - CLK-PIN: Erhöhung der Lautstärke
* `4` - DT-PIN: Verringerung der Lautstärke
* `21` - SW-PIN: Stummschaltung/Aufhebung Stummschaltung

### LED-Streifen:
* `10` - Datenpin für Ansteuerung des WS2812B LED-Streifens

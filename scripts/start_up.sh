#!/bin/bash

cd /home/pi/Desktop || return
./update.sh
cd /home/pi/Desktop/Retro.I || return

echo "Update finished! Starting app..."

pip install -r requirements.txt


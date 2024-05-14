#!/bin/bash

cd ~/Desktop || return
./update.sh
cd ~/Desktop/Retro.I || return

echo "Update finished! Starting app..."

python main.py
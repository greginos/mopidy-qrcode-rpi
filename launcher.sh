#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/ruby-mopidy
sudo python3.7 barcodeplay.py

#!/bin/bash
sudo apt-get update
sudo apt-get autoremove -y bluez
sudo apt-get install -y build-essential libreadline-dev libical-dev libdbus-1-dev libudev-dev libglib2.0-dev python3-docutils python3-pip python3-dev python3-pandas python3-pil python3-numpy
wget -P ~/bluez http://www.kernel.org/pub/linux/bluetooth/bluez-5.66.tar.xz
tar -xf ~/bluez/bluez-* -C ~/bluez
rm -r ~/bluez/bluez-*.tar.xz
cd ~/bluez/bluez-*
./configure 
make 
sudo make install
cd -
sudo sed -i '/ExecStart=/ s/$/ --experimental/' /lib/systemd/system/bluetooth.service
sudo systemctl daemon-reload
sudo systemctl unmask bluetooth.service
sudo systemctl restart bluetooth
# Reqired for some installations of dbus-fast
export SKIP_CYTHON=false
pip3 install bless yfinance pyyaml
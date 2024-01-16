# rpi_asset_tracker
An always-on asset tracker for use with a raspberrypi and an e-ink display.

Can track any asset supported by yfinance. Supports multiple assets concurrently.

Start with fresh rpi zero 2 W with raspberry pi OS Lite

# Enable SPI Interface
sudo raspi-config

# Install git and pip
sudo apt update
sudo apt upgrade
sudo apt install git-all python3-pip python3-dev python3-pandas

git clone https://github.com/waveshare/e-Paper.git

pip install ~/e-Paper/RaspberryPi_JetsonNano/python/
pip install yfinance

git clone https://github.com/TomMcKenna1/rpi_asset_tracker.git
#!/bin/bash

# Step 1: Update all packages if necessary
echo "Updating all packages..."
sudo apt update

# Step 2: Install InfluxDB
echo "Installing Influxdb..."
echo "Check this website for further purpose : https://medium.com/yavar/install-and-setup-influxdb-on-ubuntu-20-04-22-04-3d6e090ec70c"

sudo apt-get update
wget -q https://repos.influxdata.com/influxdata-archive_compat.key
echo '393e8779c89ac8d958f81f942f9ad7fb82a25e133faddaf92e15b16e6ac9ce4c influxdata-archive_compat.key' | sha256sum -c && cat influxdata-archive_compat.key | gpg --dearmor | sudo tee /etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg > /dev/null
echo 'deb [signed-by=/etc/apt/trusted.gpg.d/influxdata-archive_compat.gpg] https://repos.influxdata.com/debian stable main' | sudo tee /etc/apt/sources.list.d/influxdata.list

sudo apt-get update

sudo apt-get install influxdb2

sudo systemctl start influxdb

sudo systemctl enable influxdb
echo "One can check the status this way: sudo service influxdb status"
echo "http://localhost:8086"


# Step 3: Install MQTT package (paho-mqtt)
echo "Installing MQTT (paho-mqtt)..."
pip install paho-mqtt

# Step 4: Install InfluxDB Python client
echo "Installing InfluxDB Python client..."
pip install 'influxdb-client[ciso]'

# Step 5: Install pandas
echo "Installing pandas..."
pip install pandas

# Step 6: Install net-tools
sudo apt install net-tools

echo "Installation complete!"

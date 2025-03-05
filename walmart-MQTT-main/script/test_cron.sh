#!/bin/bash
echo "Cron test ran $(date)" >> /home/aub-rfid-10/walmart-MQTT-main/cron-test.log

/usr/bin/python3 /home/aub-rfid-10/walmart-MQTT-main/script/data_get.py --auto >> /home/aub-rfid-10/walmart-MQTT-main/cron.log 2>&1

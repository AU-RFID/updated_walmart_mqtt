crontab -e
choose : option 1

PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
PYTHONPATH=/usr/lib/python3.8
00 02  * * * /home/aub-rfid-3//walmart-MQTT-main/script/test_cron.s



chmod +x data_get.py 
chmod +x test_cron.sh 


Terminal
wsl

ssh-copy-id aub-rfid-3@192.168.0.30

sudo -i

ssh-copy-id aub-rfid-3@192.168.0.30




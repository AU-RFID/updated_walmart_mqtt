import threading
import sys
import os
import paho.mqtt.client as mqtt
import ssl
import random
import json
from time import time
import datetime

# Assuming 'config' and 'CMD' are defined in your config.py and payload_template.py respectively
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from config import config
from payload_template import CMD, RESPONSE


class MQTTSecureSubscriber:
    # Existing __init__ and other methods remain unchanged...
    def __init__(self, broker_address, broker_port, topic_callbacks, cafile, certfile=None, keyfile=None):
        self.directory = os.path.dirname(__file__)
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.cafile = cafile
        self.certfile = certfile
        self.keyfile = keyfile
        client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)

        # # Set SSL/TLS configuration
        # self.client.tls_set(ca_certs=self.cafile, certfile=self.certfile, keyfile=self.keyfile,
        #                     tls_version=ssl.PROTOCOL_TLS)
        # self.client.tls_insecure_set(True)

        # Assign event callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.topic_callbacks = {}

        self.add_topic_callback(topic_callbacks['mng_res'], self.callback_for_mng_res)
        self.add_topic_callback(topic_callbacks['ctrl_res'], self.callback_for_ctrl_res)

    def RFID_request(self, reqType, startTime, endTime):
        if self.rfidReqGen(reqType, startTime, endTime):
            self.client.publish(config.TOPICLIST['RFID_req'], self.rfidReqGen(reqType, startTime, endTime))

    def rfidReqGen(self, rtype, stime, etime):
        if rtype == 'report':
            rfidReqPayload = CMD.report_request
            rfidReqPayload['payload']['SessionStartTime'] = stime
            rfidReqPayload['payload']['SessionEndTime'] = etime
            return json.dumps(rfidReqPayload)
        elif rtype == 'analysis':
            rfidReqPayload = CMD.analysis_request
            rfidReqPayload['payload']['SessionStartTime'] = stime
            rfidReqPayload['payload']['SessionEndTime'] = etime
            return json.dumps(rfidReqPayload)
        else:
            print('ILLEAGL INPUT')
            return 0

    def add_topic_callback(self, topic, callback):
        self.topic_callbacks[topic] = callback
        # Subscribe to the topic
        self.client.subscribe(topic)

    def init_inv_settings(self):
        # Publish the message
        result = self.client.publish(config.TOPICLIST['ctrl'], json.dumps(CMD.set_mode))
        print('control res:', result)

    def start_inv(self):
        # Publish the message
        self.client.publish(config.TOPICLIST['ctrl'], json.dumps(CMD.stop))
        self.client.publish(config.TOPICLIST['ctrl'], json.dumps(CMD.set_mode))
        self.client.publish(config.TOPICLIST['ctrl'], json.dumps(CMD.start))

    def stop_inv(self):
        # Publish the message
        self.client.publish(config.TOPICLIST['ctrl'], json.dumps(CMD.stop))



    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            # Subscribe to all topics in the mapping
            for topic in self.topic_callbacks.keys():
                client.subscribe(topic)
        else:
            print(f"Failed to connect, return code {rc}\n")

    def on_message(self, client, userdata, msg):
        # Check if the topic has a dedicated callback function
        if msg.topic in self.topic_callbacks:
            self.topic_callbacks[msg.topic](client, userdata, msg)
        else:
            print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic without a dedicated callback")


    def start(self):
        # Connect to the broker
        self.client.connect(self.broker_address, self.broker_port)
        self.client.loop_start()

        # Start the control panel in a separate thread
        control_panel_thread = threading.Thread(target=self.run_control_panel)
        control_panel_thread.start()


    def run_control_panel(self):
        while True:
            print("\nControl Panel Options:")
            print("1. set mode")
            print("2. start Inventory")
            print("3. stop Inventory")
            print("4. rfid request")
            print("0. exit")

            choice = input("Enter your choice (0-4): ")

            if choice == '1':
                self.init_inv_settings()
            elif choice == '2':
                print('start inventory')
                self.start_inv()
            elif choice == '3':
                print('stop inventory')
                self.stop_inv()
            elif choice == '4':
                print('RFID Process Request')
                # startTime = input("Enter your start time (YYYY-MM-DDThh:mm:ss.sssZ): ")
                # endTime = input("Enter your start time (YYYY-MM-DDThh:mm:ss.sssZ): ")
                # reqType = input("Enter request type(report/analysis): ")
                # for future input f"{y}-{m}-{d}T{h}:{m}:{s}Z"
                time_span = 10 * 60
                startTime_value = (int(time()) - time_span) * 1000
                startTime = datetime.datetime.fromtimestamp(int(startTime_value / 1000)).strftime('%Y-%m-%dT%H:%M:%SZ')
                endTime_value = int(time() * 1000)
                endTime = datetime.datetime.fromtimestamp(int(endTime_value / 1000)).strftime('%Y-%m-%dT%H:%M:%SZ')
                reqType = 'report'
                '''
                ISO 8601 standard
                YYYY: Represents the year with four digits (e.g., 2023)
                MM: Represents the month with two digits (e.g., 03 for March)
                DD: Represents the day of the month with two digits (e.g., 15)
                ‘T‘: A literal ‘T’ character that separates the date from the time
                hh: Represents the hour of the day in 24-hour format (e.g., 14 for 2 PM)
                mm: Represents the minutes (e.g., 30)
                ss: Represents the seconds (e.g., 45)
                sss: Represents milliseconds (optional and may vary in length)
                ‘Z‘: A literal ‘Z’ character that indicates the time is in Coordinated Universal Time (UTC)
                '''
                print(f'start time:{startTime}, end time: {endTime}')
                self.RFID_request(reqType, startTime, endTime)

            elif choice == '0':
                print("Exiting control panel and stopping MQTT client loop.")
                self.client.loop_stop()  # Stop the loop before exiting
                break
            else:
                print("Invalid choice. Please enter a number between 0 and 4.")

    # Callback functions
    def callback_for_mng_res(self, client, userdata, msg):
        print(f"Callback for mng_res: Received `{msg.payload.decode()}`")

    def callback_for_ctrl_res(self, client, userdata, msg):
        print(f"Callback for ctrl_res: Received `{msg.payload.decode()}`")


if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    broker_address = 'localhost'
    broker_port = 1883
    cafile = ''
    certfile = ''
    keyfile = ''

    subscriber = MQTTSecureSubscriber(broker_address, broker_port, config.TOPICLIST, cafile, certfile, keyfile)

    subscriber.start()

import copy
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import paho.mqtt.client as mqtt
import queue
import ssl
import random
from config import config
from payload_template import CMD, RESPONSE
import json
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import threading
from datetime import datetime


class RFIDReadingProcessor:
    def __init__(self, broker_address, broker_port,
                 cafile=None,
                 certfile=None,
                 keyfile=None,
                 db_url=None,
                 db_token=None,
                 db_org=None,
                 db_bucket=None):

        # ============== init InfluxDB ==============
        # Create a client instance
        self.dbclient = InfluxDBClient(url=db_url, token=db_token, org=db_org)

        # Get the write API
        self.write_api = self.dbclient.write_api(write_options=SYNCHRONOUS)
        # Get the query API
        self.query_api = self.dbclient.query_api()

        # ============== init MQTT ==============
        self.broker_address = broker_address
        self.broker_port = broker_port
        self.cafile = cafile
        self.certfile = certfile
        self.keyfile = keyfile

        client_id = f'python-mqtt-{random.randint(0, 1000)}'
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id)

        # Set SSL/TLS configuration
        # self.client.tls_set(ca_certs=self.cafile, certfile=self.certfile, keyfile=self.keyfile,
        #                     tls_version=ssl.PROTOCOL_TLS)
        # self.client.tls_insecure_set(True)

        # Assign event callbacks
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        # Connect to the broker
        self.client.connect(self.broker_address, self.broker_port)

        # Queues for message handling
        self.rfid_reading_queue = queue.Queue()
        self.rfid_request_queue = queue.Queue()
        # Start standby threads for handling sensor data and requests
        threading.Thread(target=self.handle_rfid_reading, daemon=True).start()
        threading.Thread(target=self.handle_rfid_request, daemon=True).start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
            # Subscribe to all topics in the mapping
            for topic in config.TOPICLIST.values():
                print('available topics:', topic)
                client.subscribe(topic)
        else:
            print(f"Failed to connect, return code {rc}\n")

    def on_message(self, client, userdata, msg):
        if msg.topic == config.TOPICLIST['tag_event']:
            self.rfid_reading_queue.put(msg.payload)
        elif msg.topic == config.TOPICLIST['RFID_req']:
            self.rfid_request_queue.put(msg)
        elif msg.topic == config.TOPICLIST['mng_event']:
            print('mng_event')
        else:
            print(f"Received msg from `{msg.topic}` topic without a dedicated callback")

    def retrieve_data_from_DB_with_Time(self, start_time, end_time):
        """
        The function retrieve the data from the database with the transaction start time and end time
        :param start_time:  TBD
        :param end_time:  TBD
        :return: A pandas dataframe including original RFID readings
        """

        current_measurement = config.DB_PARAMETER['db_measurement']

        query = f'''
        from(bucket: "{config.DB_PARAMETER['db_bucket']}")
          |> range(start: {start_time}, stop: {end_time})
          |> filter(fn: (r) => r._measurement == "{current_measurement}")
          |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")
        '''
        result = self.query_api.query_data_frame(query)
        if not result.empty:
            result = result.drop(columns=['result', '_start', '_stop', '_time', 'table', '_measurement'])
            print('result:', result)
        return result

    def prepare_rfid_data(self, request_msg):
        """
        Parsing the time information from the request and using it to retrieve data from the database
        :param request_msg: a rfid_process_request
        :return: reading list, command in the payload, transaction start time, transaction end time
        """
        msg_dict = json.loads(request_msg.payload.decode())
        rfid_start_time = msg_dict['payload']['transactionStartTime']
        rfid_end_time = msg_dict['payload']['transactionEndTime']
        rfid_readings = self.retrieve_data_from_DB_with_Time(rfid_start_time, rfid_end_time)
        # print(rfid_readings)
        return rfid_readings, msg_dict['command'], rfid_start_time, rfid_end_time

    def rfid_request_reporter(self, data_to_publish, msg_template, start_time, end_time):
        """
        Prepare the final json file with the processed data, and sent it
        :param data_to_publish: a list of rfid reading dict/ a list of rfid analysis dict
        :param msg_template: the response template
        :param start_time: transaction start time
        :param end_time: transaction end time
        :return: N/A
        """
        msg_template['payload']['transactionStartTime'] = start_time
        msg_template['payload']['transactionEndTime'] = end_time
        msg_template['payload']['data'] = data_to_publish.to_dict('records')
        self.client.publish(config.TOPICLIST['RFID_res'], json.dumps(msg_template))

    def analyze_readings(self, readingss):
        """
        Generate RFID analysis report with raw rfid readings
        :param readings: raw rfid readings
        :return: an analysis report?
        """
        return readingss

    def start(self):
        # Start the loop to process received messages
        self.client.loop_forever()

    def handle_rfid_reading(self):
        """
        The callback for saving every received reading to InfluxDB
        :return:
        """
        while True:
            # print('new rfid reading')
            payload = self.rfid_reading_queue.get()
            # convert received reading(JSON) as a dictionary
            dict_msg = json.loads(payload.decode())
            # print(dict_msg)
            point_data = self.prepare_point_data(dict_msg)
            self.write_api.write(bucket=config.DB_PARAMETER['db_bucket']
                                 , org=config.DB_PARAMETER['db_org']
                                 , record=point_data)

    def handle_rfid_request(self):
        """
        With different command type, choosing response template and publish the rfid report/analysis
        :return:
        """
        response_template = None
        while True:
            if self.rfid_request_queue.qsize() > 0:
                print('new rfid request')
                rfid_request = self.rfid_request_queue.get()
                rfid_readings, command_type, stime, etime = self.prepare_rfid_data(rfid_request)
                if command_type == 'analysisRequest':
                    rfid_readings = self.analyze_readings(rfid_readings)
                    response_template = copy.deepcopy(RESPONSE.analysisRequest)
                elif command_type == 'reportRequest':
                    response_template = copy.deepcopy(RESPONSE.reportRequest)
                self.rfid_request_reporter(rfid_readings, response_template, stime, etime)

    def prepare_point_data(self, raw_msg_dict):
        """
        Parse received RFID readings(dict) and convert it to Point which is supported by InfluxDB
        :param raw_msg_dict:
        :return:
        """
        EPC = str(raw_msg_dict['data']['idHex'])
        peakRSSI = int(raw_msg_dict['data']['peakRssi'])
        phase = float(raw_msg_dict['data']['phase'])
        # Unix timestamp (including milliseconds) convert to an integer
        timeStamp = int(datetime.strptime(str(raw_msg_dict['timestamp']), "%Y-%m-%dT%H:%M:%S.%f%z").timestamp() * 1000)
        channel = float(raw_msg_dict['data']['channel'])
        antenna = int(raw_msg_dict['data']['antenna'])
        unique_id = str(timeStamp) + ':' + str(raw_msg_dict['data']['eventNum'])
        current_measurement = config.DB_PARAMETER['db_measurement']
        point_data = Point(current_measurement) \
            .field('EPC', EPC).field('peakRSSI', peakRSSI).field('phase', phase) \
            .field('channel', channel).field('antenna', antenna).field('timestamp:eventNum', unique_id) \
            .time(timeStamp, WritePrecision.MS)
        return [point_data]


if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    broker_address = 'localhost'
    # broker_port = 8883
    broker_port = 1883
    # cafile = os.path.join(dir, config.CERTPATH['cafile'])  # Path to the CA certificate
    # certfile = os.path.join(dir, config.CERTPATH['certfile'])  # Path to the client certificate
    # keyfile = os.path.join(dir, config.CERTPATH['keyfile'])  # Path to the client key
    cafile = ''
    certfile = ''
    keyfile = ''

    subscriber = RFIDReadingProcessor(broker_address, broker_port,
                                      cafile,
                                      certfile,
                                      keyfile,
                                      config.DB_PARAMETER['db_url'],
                                      config.DB_PARAMETER['db_token'],
                                      config.DB_PARAMETER['db_org'],
                                      config.DB_PARAMETER['db_bucket'])

    subscriber.start()

from processorBase import RFIDReadingProcessor
import os
from config import config
import socket
from datetime import datetime
import time
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



class RFIDReceiver(RFIDReadingProcessor):
    def __init__(self, broker_address, broker_port,
                 cafile=None,
                 certfile=None,
                 keyfile=None,
                 db_url=None,
                 db_token=None,
                 db_org=None,
                 db_bucket=None,
                 debug_switch=False):
        super().__init__(broker_address, broker_port,
                         cafile,
                         certfile,
                         keyfile,
                         db_url,
                         db_token,
                         db_org,
                         db_bucket,
                         rfid_receiver=True,
                         rfid_analyzer=False,
                         debug_switch=debug_switch)
        self.comp_id = socket.gethostname()

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
        .tag('comp_id', self.comp_id) \
        .field('EPC', EPC) \
        .field('peakRSSI', peakRSSI) \
        .field('phase', phase) \
        .field('channel', channel) \
        .field('antenna', antenna) \
        .field('timestamp:eventNum', unique_id) \
        .time(timeStamp, WritePrecision.MS)
        return [point_data]

        
        


if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    broker_address = 'localhost'
    broker_port = 1883
    cafile = ''
    certfile = ''
    keyfile = ''

    receiver = RFIDReceiver(broker_address, broker_port,
                            cafile,
                            certfile,
                            keyfile,
                            config.DB_PARAMETER['db_url'],
                            config.DB_PARAMETER['db_token'],
                            config.DB_PARAMETER['db_org'],
                            config.DB_PARAMETER['db_bucket'],
                            )

    receiver.start()

from processorBase import RFIDReadingProcessor
import os
from config import config
import argparse


class RFIDAnalyzer(RFIDReadingProcessor):
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
                         rfid_receiver=False,
                         rfid_analyzer=True,
                         debug_switch=debug_switch)


if __name__ == "__main__":
    dir = os.path.dirname(__file__)
    broker_address = 'localhost'
    broker_port = 1883
    cafile = ''
    certfile = ''
    keyfile = ''

    parser = argparse.ArgumentParser()
    parser.add_argument('-debug', action='store_true', default=False)
    args = parser.parse_args()

    analyzer = RFIDAnalyzer(broker_address, broker_port,
                            cafile,
                            certfile,
                            keyfile,
                            config.DB_PARAMETER['db_url'],
                            config.DB_PARAMETER['db_token'],
                            config.DB_PARAMETER['db_org'],
                            config.DB_PARAMETER['db_bucket'],
                            args.debug)

    analyzer.start()

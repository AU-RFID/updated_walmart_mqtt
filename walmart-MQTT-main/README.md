# walmart-MQTT API


## Getting started

### Installation

The MQTT broker is **the backend system which coordinates messages between the different clients**. Theoretically, our API and the mock system are compathible with all open-source MQTT brokers. Currently, a Mosquitto MQTT Broker is implemented with Docker.

#### 1. Install Docker Engine on Ubuntu

The [document](https://docs.docker.com/engine/install/ubuntu/) provides you all the information needed to get up and running the Docker Engine.

#### 2. Run the eclipse-mosquitto MQTT Broker in a docker container

```github
docker run -it -p 18083:18083 -p 18084:18084 -p 1883:1883 -p 8883:8883 -p 8083:8083 -p 8084:8084 -v /mosquitto/certs -v /mosquitto/data -v /mosquitto/log eclipse-mosquitto
```

#### 3. Configure the mosquitto broker using a configuration file

login the container’s directory `/mosquitto/config` and refer the following configuration to modify `mosquitto.conf`:

```github
persistence true
persistence_location /mosquitto/data/
log_dest file /mosquitto/log/mosquitto.log

listener 1883
listener 8883
allow_anonymous true
require_certificate false
```

In order for changes in the `mosquitto.conf` file to become effective you **must** **restart** the mosquitto broker.

Now, if you have docker desktop, the container could be seen in the panel.

#### 4. Setup InfluxDB
a. make two folders, `data` and `config` in the current folder\
b. run the following script
```github
docker run -d -p 8086:8086 \
    -v "$PWD/data:/var/lib/influxdb2" \
    -v "$PWD/config:/etc/influxdb2" \
    -e DOCKER_INFLUXDB_INIT_MODE=setup \
    -e DOCKER_INFLUXDB_INIT_USERNAME=automation_team \
    -e DOCKER_INFLUXDB_INIT_PASSWORD=1qaz2wsx \
    -e DOCKER_INFLUXDB_INIT_ORG=AU_RFIDLAB \
    -e DOCKER_INFLUXDB_INIT_BUCKET=rfid_readings_test \
    -e DOCKER_INFLUXDB_INIT_RETENTION=1w \
    -e DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=!QAZ2wsx \
    influxdb:2
```

#### 5.Set up dependencies and start the system

The system uses the Eclipse Paho MQTT Python client library. This package provides a client class which enables applications to connect to an [MQTT](http://mqtt.org/) broker to publish messages, and to subscribe to topics and receive published messages.

The package can be installed using

```github
pip install paho-mqtt
```

Also, a python InfluxDB client is essential for the API. The client is available with:
```github
pip install 'influxdb-client[ciso]'
```

Currently, all code is base on `paho-mqtt 2.0.0` and `influxdb-client 1.41.0`.

you mau also need pandas `pip install pandas`

Now you are good to run: \
        `processor_analysis_and_report.py` --- subscribe /RFID_process_request and generate RFID report \
        `processor_push_to_database.py` --- subscribe /tag_event topic and save the rag readings in InfluxDB \
        `controller_multithread.py` --- a temporary controller


#### 5. Massages and error response

The predifined payloads (commands and responses) are stored in `./payload_template/CMD.py` and `./payload_template/RESPONSE.py`. The payload format is available in our API design document and [Zebra's RAW MQTT Playload Schemas](https://zebradevs.github.io/rfid-ziotc-docs/schemas/raw_mqtt_payloads/index.html).


All the topic name and InfluxDB parameters are defined in `./config/config.py`. The `db_token` is available form the InfluxDB's control panel.

```github
TOPICLIST = {'mng_event': '/FX9600xxxxxx/management_event',
             'tag_event': '/FX9600xxxxxx/tag_event',
             'mng': '/FX9600xxxxxx/management',
             'mng_res': '/FX9600xxxxxx/management_response',
             'ctrl': '/FX9600xxxxxx/control',
             'ctrl_res': '/FX9600xxxxxx/control_response',
             'RFID_req': '/FX9600xxxxxx/RFID_process_request',
             'RFID_res': '/FX9600xxxxxx/RFID_process_response',
            }
DB_PARAMETER = {'db_url': 'http://localhost:8086',
                'db_token': 'g_4-NdTwUFmkat-HQBjiwnd6mDNDcs9UxHXQuhOI4wWoJ2fidK9QlQptM4vADtdIYe4uxOZ3tlDr2cX9uT7nfA==',
                'db_org': 'AU_RFIDLAB',
                'db_bucket': 'rfid_readings_test',
                'db_measurement': 'test'}
```


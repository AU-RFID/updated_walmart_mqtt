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
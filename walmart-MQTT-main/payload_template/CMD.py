get_version = {
  "command": "get_version",
  "command_id": "a12cb5677",
  "payload": {}
}
get_network = {
  "command": "get_network",
  "command_id": "a12cb345654",
  "payload": {}
}

get_config = {
  "command": "get_config",
  "command_id": "1a234",
  "payload": {
    "verbose": True
  }
}

set_network = {
  "command": "set_network",
  "command_id": "abcd345",
  "payload": {
    "hostName": "FX9600F0F4B5",
    "ipAddress": "192.168.1.10",
    "gatewayAddress": "192.168.1.1",
    "subnetMask": "255.255.255.0",
    "dnsAddress": "8.8.8.8",
    "dhcp": "True",
    "macAddress": "84:24:8D:F0:F4:B5"
  }
}

get_status = {
  "command": "get_status",
  "command_id": "abcd1234",
  "payload": {}
}

reboot = {
  "command": "reboot",
  "command_id": "abcd1431243",
  "payload": {}
}

set_gpo = {
  "command": "set_gpo",
  "command_id": "abcd1324",
  "payload": {
    "port": 1,
    "state": False
  }
}

get_appled = {
  "command": "get_appled",
  "command_id": "string",
  "payload": {}
}

set_appled = {
  "command": "set_appled",
  "command_id": "abcd1243",
  "payload": {
    "color": "red",
    "seconds": 60,
    "flash": True
  }
}

get_region = {
  "command": "get_region",
  "command_id": "a1b2c3345",
  "payload": {}
}

start = {
  "command": "start",
  "command_id": "abcd1432",
  "payload": {
    "doNotPersistState": True
  }
}

stop = {
  "command": "stop",
  "command_id": "abcd1324",
  "payload": {}
}

get_mode = {
  "command": "get_mode",
  "command_id": "a134454",
  "payload": {
    "verbose": True
  }
}

set_mode = {
    "command": "set_mode",
    "command_id": "abcd134",
    "payload": {
        "antennaStopCondition": [
            {
                "type": "DURATION",
                "value": 65535
            },
            {
                "type": "DURATION",
                "value": 65535
            },
            {
                "type": "DURATION",
                "value": 65535
            },
            {
                "type": "DURATION",
                "value": 65535
            }
        
        ],

        "delayAfterSelects": 0,
        "delayBetweenAntennaCycles": {
            "duration": 0,
            "type": "DISABLED"
        },
        "environment": "DEMO",
        "modeSpecificSettings": {
            "interval": {
                "unit": "seconds",
                "value": 0
            }
        },
        "radioStartConditions": {},
        "radioStopConditions": {},
        "tagMetaData": [
            "ANTENNA",
            "RSSI",
            "CHANNEL",
            "SEEN_COUNT",
            "PHASE",
            {
                "userDefined": "readerABC"
            },
            "EPC"
        ],
        "transmitPower": 30.0,
        "type": "INVENTORY",
        "query": {
          "sel": "ALL",
          "session": "S0",
          "target": "AB"
        }
    }
}

set_os = {
  "command": "set_os",
  "command_id": "abdc123",
  "payload": {
    "url": "https://192.168.29.39:8000/Build-3.10.27/Firmware",
    "authenticationType": "BASIC",
    "options": {
      "username": "test",
      "password": "test"
    },
    "verifyPeer": True,
    "verifyHost": True,
    "CACertificateFileContent": "\"-----BEGIN CERTIFICATE-----\\r\\n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\\r\\n7ZkfOkNrbiHMZJ7xQyFtS35gPtMoh6sOTSvPUdg=\\r\\n-----END CERTIFICATE-----\\r\\n\"",
    "CACertificateFileLocation": "/apps/ca.crt"
  }
}

set_config = {
  "command": "set_config",
  "command_id": "abdc2134",
  "payload": {
    "xml": "string",
    "GPIO-LED": {
      "GPODefaults": {
        "1": "HIGH",
        "2": "LOW",
        "3": "HIGH",
        "4": "HIGH"
      },
      "LEDDefaults": {
        "3": "GREEN"
      },
      "GPI_1_H": [
        {
          "type": "GPO",
          "pin": 1,
          "state": "HIGH",
          "postActionState": "HIGH",
          "blink": {
            "ON": 0,
            "OFF": 0,
            "DURATION": 0
          },
          "conditions": [
            "IS_CLOUD_CONNECTED"
          ]
        }
      ],
      "GPI_1_L": [
        {
          "type": "GPO",
          "pin": 1,
          "state": "HIGH",
          "postActionState": "HIGH",
          "blink": {
            "ON": 0,
            "OFF": 0,
            "DURATION": 0
          },
          "conditions": [
            "IS_CLOUD_CONNECTED"
          ]
        }
      ],
      "GPI_2_H": [
        {
          "type": "GPO",
          "pin": 1,
          "state": "HIGH",
          "postActionState": "HIGH",
          "blink": {
            "ON": 0,
            "OFF": 0,
            "DURATION": 0
          },
          "conditions": [
            "IS_CLOUD_CONNECTED"
          ]
        }
      ],
      "GPI_2_L": [
        {
          "type": "GPO",
          "pin": 1,
          "state": "HIGH",
          "postActionState": "HIGH",
          "blink": {
            "ON": 0,
            "OFF": 0,
            "DURATION": 0
          },
          "conditions": [
            "IS_CLOUD_CONNECTED"
          ]
        }
      ],
      "CLOUD_DISCONNECT": [
        {
          "type": "GPO",
          "pin": 1,
          "state": "HIGH",
          "postActionState": "HIGH",
          "blink": {
            "ON": 0,
            "OFF": 0,
            "DURATION": 0
          },
          "conditions": [
            "IS_CLOUD_CONNECTED"
          ]
        }
      ],
      "CLOUD_CONNECT": [
        {
          "type": "GPO",
          "pin": 1,
          "state": "HIGH",
          "postActionState": "HIGH",
          "blink": {
            "ON": 0,
            "OFF": 0,
            "DURATION": 0
          },
          "conditions": [
            "IS_CLOUD_CONNECTED"
          ]
        }
      ],
      "TAG_READ": [
        {
          "type": "GPO",
          "pin": 1,
          "state": "HIGH",
          "postActionState": "HIGH",
          "blink": {
            "ON": 0,
            "OFF": 0,
            "DURATION": 0
          },
          "conditions": [
            "IS_CLOUD_CONNECTED"
          ]
        }
      ],
      "RADIO_START": [
        {
          "type": "GPO",
          "pin": 1,
          "state": "HIGH",
          "postActionState": "HIGH",
          "blink": {
            "ON": 0,
            "OFF": 0,
            "DURATION": 0
          },
          "conditions": [
            "IS_CLOUD_CONNECTED"
          ]
        }
      ],
      "RADIO_STOP": [
        {
          "type": "GPO",
          "pin": 1,
          "state": "HIGH",
          "postActionState": "HIGH",
          "blink": {
            "ON": 0,
            "OFF": 0,
            "DURATION": 0
          },
          "conditions": [
            "IS_CLOUD_CONNECTED"
          ]
        }
      ]
    },
    "READER-GATEWAY": {
      "retention": {
        "throttle": 200,
        "maxNumEvents": 150000,
        "maxEventRetentionTimeInMin": 10
      },
      "batching": {
        "reportingInterval": 1000,
        "maxPayloadSizePerReport": "256KB"
      },
      "managementEventConfig": {
        "errors": {
          "cpu": {
            "threshold": 90,
            "reportIntervalInSec": 1800
          },
          "flash": {
            "threshold": 90,
            "reportIntervalInSec": 1800
          },
          "ram": {
            "threshold": 90,
            "reportIntervalInSec": 1800
          },
          "reader_gateway": True,
          "antenna": True,
          "database": True,
          "radio": True,
          "radio_control": True
        },
        "warnings": {
          "cpu": {
            "threshold": 80,
            "reportIntervalInSec": 1800
          },
          "flash": {
            "threshold": 90,
            "reportIntervalInSec": 1800
          },
          "ram": {
            "threshold": 90,
            "reportIntervalInSec": 1800
          },
          "ntp": {
            "threshold": 0,
            "reportIntervalInSec": 0
          },
          "temperature": {
            "ambient": 75,
            "pa": 105
          },
          "database": True,
          "radio_api": True,
          "radio_control": True,
          "reader_gateway": True
        },
        "heartbeat": {
          "fields": {
            "radio_control": [
              "ANTENNAS"
            ],
            "reader_gateway": [
              "NUM_DATA_MESSAGES_RXED"
            ],
            "system": [
              "CPU"
            ],
            "userapps": [
              "STATUS"
            ],
            "userDefined": "string"
          },
          "interval": 60
        },
        "gpiEvents": True,
        "userappEvents": True
      },
      "endpointConfig": {
        "data": {
          "event": {
            "connections": [
              {
                "type": "mqtt",
                "options": {
                  "endpoint": {
                    "hostName": "10.17.231.77",
                    "port": 8883,
                    "protocol": "tcp"
                  },
                  "enableSecurity": True,
                  "security": {
                    "keyFormat": "PEM",
                    "keyAlgorithm": "RSA256",
                    "CACertificateFileLocation": "string",
                    "publicKeyFileLocation": "string",
                    "privateKeyFileLocation": "string",
                    "verifyHostName": True
                  },
                  "basicAuthentication": {
                    "username": "string",
                    "password": "string"
                  },
                  "additional": {
                    "keepAlive": 0,
                    "cleanSession": True,
                    "debug": True,
                    "reconnectDelay": 0,
                    "reconnectDelayMax": 0,
                    "clientId": "string",
                    "qos": 0
                  },
                  "publishTopic": [
                    "string"
                  ],
                  "subscribeTopic": [
                    "string"
                  ]
                },
                "name": "string",
                "description": "string",
                "additionalOptions": {
                  "batching": {
                    "reportingInterval": 1000,
                    "maxPayloadSizePerReport": 256000
                  },
                  "retention": {
                    "throttle": 200,
                    "maxNumEvents": 150000,
                    "maxEventRetentionTimeInMin": 10
                  }
                }
              }
            ]
          }
        }
      }
    }
  }
}

get_logs = {
  "command": "get_logs",
  "command_id": "a2134",
  "payload": {}
}

set_logs = {
  "command": "set_logs",
  "command_id": "abcd2134234",
  "payload": {
    "radioPacketLog": True,
    "components": [
      {
        "componentName": "RC",
        "level": "DEBUG"
      }
    ]
  }
}

get_logs_syslog = {
  "command": "get_logs_syslog",
  "command_id": "a132234",
  "payload": {}
}

get_logs_radioPacketLog = {
  "command": "get_logs_radioPacketLog",
  "command_id": "a1324",
  "payload": {}
}

del_logs_syslog = {
  "command": "del_logs_syslog",
  "command_id": "abcd1234",
  "payload": {}
}

del_logs_radioPacketLog = {
  "command": "del_logs_radioPacketLog",
  "command_id": "abcd2342",
  "payload": {}
}

get_logs_rgErrorLog = {
  "command": "get_logs_rgErrorLog",
  "command_id": "ab32445",
  "payload": {}
}

get_logs_rgWarningLog = {
  "command": "get_logs_rgWarningLog",
  "command_id": "abf868234",
  "payload": {}
}

get_logs_rcLog = {
  "command": "get_logs_rcLog",
  "command_id": "abd12354",
  "payload": {}
}

set_reqToUserapp = {
  "command": "set_reqToUserapp",
  "command_id": "abcd13212",
  "payload": {
    "userapp": "sample",
    "command": "version"
  }
}

set_installUserapp = {
  "command": "set_installUserapp",
  "command_id": "abcd123",
  "payload": {
    "url": "https://example.com/apps/",
    "filename": "sample_1.0.0.deb",
    "authenticationType": "NONE",
    "options": {
      "username": "string",
      "password": "string"
    },
    "verifyPeer": True,
    "verifyHost": True,
    "CACertificateFileLocation": "/apps/ca.pem",
    "CACertificateFileContent": "string"
  }
}

set_uninstallUserapp = {
  "command": "set_uninstallUserapp",
  "command_id": "abcd134",
  "payload": {
    "appname": "sample"
  }
}

set_startUserapp = {
  "command": "set_startUserapp",
  "command_id": "abcd1324",
  "payload": {
    "appname": "sample"
  }
}

set_stopUserapp = {
  "command": "set_stopUserapp",
  "command_id": "abcd1324",
  "payload": {
    "appname": "sample"
  }
}

set_autostartUserapp = {
  "command": "set_autostartUserapp",
  "command_id": "abcd1234",
  "payload": {
    "appname": "userapp name",
    "autostart": True
  }
}

get_userapps = {
  "command": "get_userapps",
  "command_id": "abcd243324",
  "payload": {}
}

get_certificates = {
  "command": "get_certificates",
  "command_id": "abcd12354",
  "payload": {}
}

del_certificate = {
  "command": "del_certificate",
  "command_id": "abcd1234",
  "payload": {
    "name": "string",
    "type": "client"
  }
}

set_updateCertificate = {
  "command": "set_updateCertificate",
  "command_id": "abcd1324",
  "payload": {
    "name": "test",
    "type": "client",
    "url": "ftps://10.17.231.92/CA-Certs_3.18.2/myCA/reader.pfx",
    "authenticationType": {
      "authenticationType": "BASIC"
    },
    "pfxPassword": "abcd12345",
    "pfxFileName": "dfbhnhf",
    "pfxContent": "mhmfgm",
    "timeoutInSec": 0,
    "filename": "czdsvfs",
    "verifyPeer": True,
    "verifyHost": True,
    "CACertificateFileLocation": "gfwwhg",
    "CACertificateFileContent": "wehwe",
    "installedCertificateType": "string",
    "installedCertificateName": "string",
    "publicKeyFileLocation": "string",
    "publicKeyFileContent": "string",
    "privateKeyFileLocation": "string",
    "privateKeyFileContent": "string",
    "headers": {}
  }
}

set_refreshCertificate = {
  "command": "set_refreshCertificate",
  "command_id": "abcd1324",
  "payload": {
    "name": "string",
    "type": "string"
  }
}

set_revertbackOS = {
  "command": "set_revertbackOS",
  "command_id": "abcd1434",
  "payload": {}
}

get_gpoStatus = {
  "command": "get_gpoStatus",
  "command_id": "abdc453254",
  "payload": {}
}

get_gpiStatus = {
  "command": "get_gpiStatus",
  "command_id": "abcd21344",
  "payload": {}
}

get_supportedRegionList = {
  "command": "get_supportedRegionList",
  "command_id": "gvjh",
  "payload": {}
}

get_supportedStandardlist = {
  "command": "get_supportedStandardlist",
  "command_id": "sdgf",
  "payload": {
    "region": "Argentina"
  }
}

get_timeZone = {
  "command": "get_timeZone",
  "command_id": "abcd21344",
  "payload": {}
}

set_timeZone = {
  "command": "set_timeZone",
  "command_id": "abcd1324",
  "payload": {
    "timeZone": "International Date Line West"
  }
}

get_ntpServer = {
  "command": "get_ntpServer",
  "command_id": "abcd1324",
  "payload": {}
}

set_ntpServer = {
  "command": "set_ntpServer",
  "command_id": "abcd1324",
  "payload": {
    "server": "time.google.com"
  }
}

get_cableLossCompensation = {
  "command": "get_cableLossCompensation",
  "command_id": "abcd1324",
  "payload": {}
}

set_cableLossCompensation = {
  "command": "set_cableLossCompensation",
  "command_id": "abcd1324",
  "payload": {
    "1": {
      "cableLossPerHundredFt": 0,
      "cableLength": 5
    },
    "2": {
      "cableLossPerHundredFt": 10,
      "cableLength": 15
    },
    "3": {
      "cableLossPerHundredFt": 20,
      "cableLength": 25
    },
    "4": {
      "cableLossPerHundredFt": 30,
      "cableLength": 35
    }
  }
}

get_readerCapabilities = {
  "command": "get_readerCapabilities",
  "command_id": "abcd21344",
  "payload": {}
}

set_nameAndDescription = {
  "command": "set_nameAndDescription",
  "command_id": "abcd1324",
  "payload": {
    "name": "string",
    "description": "string"
  }
}

get_nameAndDescription = {
  "command": "get_nameAndDescription",
  "command_id": "abcd21344",
  "payload": {}
}


report_request = {
            "command": "reportRequest",
            "command_id": "rfid123",
            "payload": {
                        "SessionStartTime": "2019-08-24T14:15:22Z",
                        "SessionEndTime": "2019-08-24T14:21:99Z"
                        }
}

analysis_request = {
            "command": "analysisRequest",
            "command_id": "rfid223",
            "payload": {
                        "SessionStartTime": "2019-08-24T14:15:22Z",
                        "SessionEndTime": "2019-08-24T14:21:99Z"
                        }
}

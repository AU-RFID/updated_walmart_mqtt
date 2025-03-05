get_version = {
  "command": "get_version",
  "command_id": "string",
  "response": "success",
  "payload": {
    "readerApplication": "2.7.19.0",
    "radioApi": "2.2.8.2",
    "radioFirmware": "2.1.14.0",
    "radioControlApplication": "1.0.0",
    "readerOS": "2.2.15.0",
    "readerHardware": "0.0.5.0",
    "readerBootLoader": "2.1.2.0",
    "readerFileSystem": "2.1.2.0",
    "cloudAgentApplication": "1.0.0",
    "fpga": "1.8.0.0",
    "revertBackFirmware": {
      "readerApplication": "3.10.30.0",
      "readerBootLoader": "3.17.3.0",
      "readerFileSystem": "3.17.11.0",
      "readerOS": "3.10.3.0"
    }
  }
}

get_network = {
  "command": "get_network",
  "command_id": "a12cb345654",
  "response": "success",
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

get_config = {
  "command": "get_config",
  "command_id": "1a234",
  "response": "success",
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
        "1": "GREEN",
        "2": "GREEN",
        "3": "RED"
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
            ]
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
                }
              }
            ]
          }
        }
      }
    }
  }
}

set_network = {
  "command": "set_network",
  "command_id": "abcd345",
  "response": "success",
  "payload": {}
}

get_status = {
  "command": "get_status",
  "command_id": "abcd1234",
  "response": "success",
  "payload": {
    "uptime": "26 days 01:11:17",
    "systemTime": "2020-01-08T15:36:53+00:00",
    "ram": {
      "total": "26098076",
      "free": "195612672",
      "used": "65368064"
    },
    "flash": {
      "deviceId": "RFIDF0F4B5",
      "rootFileSystem": {
        "total": "26098076",
        "free": "195612672",
        "used": "65368064"
      },
      "platform": {
        "total": "26098076",
        "free": "195612672",
        "used": "65368064"
      },
      "readerConfig": {
        "total": "26098076",
        "free": "195612672",
        "used": "65368064"
      },
      "readerData": {
        "total": "26098076",
        "free": "195612672",
        "used": "65368064"
      }
    },
    "cpu": {
      "user": "42",
      "system": "32"
    },
    "radioConnection": "connected",
    "antennas": {
      "0": "connected",
      "1": "connected",
      "2": "connected",
      "3": "connected",
      "4": "connected",
      "5": "connected",
      "6": "connected",
      "7": "connected",
      "8": "connected",
      "9": "connected",
      "10": "connected",
      "11": "connected",
      "12": "connected",
      "13": "connected"
    },
    "temperature": 31,
    "radioActivitiy": "active",
    "powerSource": "DC",
    "powerNegotiation": "disabled",
    "ntp": {
      "offset": 120,
      "reach": 377
    }
  }
}

reboot = {
  "command": "reboot",
  "command_id": "abcd1431243",
  "response": "success",
  "payload": {}
}

set_gpo = {
  "command": "set_gpo",
  "command_id": "abcd1324",
  "response": "success",
  "payload": {}
}

get_appled = {
  "command": "get_appled",
  "command_id": "string",
  "response": "success",
  "payload": {
    "status": "DEFAULT"
  }
}

set_appled = {
  "command": "set_appled",
  "command_id": "abcd1243",
  "response": "success",
  "payload": {}
}

get_region = {
  "command": "get_region",
  "command_id": "a1b2c3345",
  "response": "success",
  "payload": {
    "region": "US",
    "regulatoryStandard": "FCC",
    "lbtEnabled": "false",
    "channelData": [
      915250,
      915750,
      903250,
      926750,
      926250,
      904250,
      927250,
      920250,
      919250,
      909250,
      918750,
      917750,
      905250,
      904750,
      925250,
      921750,
      914750,
      906750,
      913750,
      922250,
      911250,
      911750,
      903750,
      908750,
      905750,
      912250,
      906250,
      917250,
      914250,
      907250,
      918250,
      916250,
      910250,
      910750,
      907750,
      924750,
      909750,
      919750,
      916750,
      913250,
      923750,
      908250,
      925750,
      912750,
      924250,
      921250,
      920750,
      922750,
      902750,
      923250
    ],
    "minTxPowerSupported": 100,
    "maxTxPowerSupported": 300
  }
}

start = {
  "command": "start",
  "command_id": "abcd1432",
  "response": "success",
  "payload": {}
}

stop = {
  "command": "stop",
  "command_id": "abcd1324",
  "response": "success",
  "payload": {}
}

get_mode = {
  "command": "get_mode",
  "command_id": "a134454",
  "response": "success",
  "payload": {
    "type": "INVENTORY",
    "antennas": [
      1,
      2,
      3
    ],
    "transmitPower": 30.1,
    "antennaStopCondition": [
      {
        "type": "DURATION",
        "value": 500
      },
      {
        "type": "INVENTORY_COUNT",
        "value": 1
      },
      {
        "type": "GPI",
        "value": {
          "port": 2,
          "signal": "HIGH"
        }
      }
    ],
    "tagMetaData": [
      "PC",
      "CRC",
      {
        "userDefined": "readerABC"
      }
    ],
    "rssiFilter": {
      "threshold": -72
    }
  }
}

set_mode = {
  "command": "set_mode",
  "command_id": "abcd134",
  "response": "success",
  "payload": {}
}

set_os = {
  "command": "set_os",
  "command_id": "abdc123",
  "response": "success",
  "payload": {}
}

set_config = {
  "command": "set_config",
  "command_id": "abdc2134",
  "response": "success",
  "payload": {}
}

get_logs = {
  "command": "get_logs",
  "command_id": "a2134",
  "response": "success",
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

set_logs = {
  "command": "set_logs",
  "command_id": "abcd2134234",
  "response": "success",
  "payload": {}
}

get_logs_syslog = {
  "command": "get_logs_syslog",
  "command_id": "a132234",
  "response": "success",
  "payload": {
    "filename": "syslog.tar.gz",
    "binary": "string"
  }
}

get_logs_radioPacketLog = {
  "command": "get_logs_radioPacketLog",
  "command_id": "a1324",
  "response": "success",
  "payload": {
    "filename": "radioPktLog.tar.gz",
    "binary": "string"
  }
}

del_logs_syslog = {
  "command": "del_logs_syslog",
  "command_id": "abcd1234",
  "response": "success",
  "payload": {}
}

del_logs_radioPacketLog = {
  "command": "del_logs_radioPacketLog",
  "command_id": "abcd2342",
  "response": "success",
  "payload": {}
}

get_logs_rgErrorLog = {
  "command": "get_logs_rgErrorLog",
  "command_id": "ab32445",
  "response": "success",
  "payload": {
    "filename": "rgErrorLog.tar.gz",
    "binary": "string"
  }
}

get_logs_rgWarningLog = {
  "command": "get_logs_rgWarningLog",
  "command_id": "abf868234",
  "response": "success",
  "payload": {
    "filename": "rgWarningLog.tar.gz",
    "binary": "string"
  }
}

get_logs_rcLog = {
  "command": "get_logs_rcLog",
  "command_id": "abd12354",
  "response": "success",
  "payload": {
    "filename": "rcErrorLog.tar.gz",
    "binary": "string"
  }
}

set_reqToUserapp = {
  "command": "set_reqToUserapp",
  "command_id": "abcd13212",
  "response": "success",
  "payload": {
    "response": "string"
  }
}

set_installUserapp = {
  "command": "set_installUserapp",
  "command_id": "abcd123",
  "response": "success",
  "payload": {}
}

set_uninstallUserapp = {
  "command": "set_uninstallUserapp",
  "command_id": "abcd134",
  "response": "success",
  "payload": {}
}

set_startUserapp = {
  "command": "set_startUserapp",
  "command_id": "abcd1324",
  "response": "success",
  "payload": {}
}

set_stopUserapp = {
  "command": "set_stopUserapp",
  "command_id": "abcd1324",
  "response": "success",
  "payload": {}
}

set_autostartUserapp = {
  "command": "set_autostartUserapp",
  "command_id": "abcd1234",
  "response": "success",
  "payload": {}
}

get_userapps = {
  "command": "get_userapps",
  "command_id": "abcd243324",
  "response": "success",
  "payload": [
    {
      "appname": "sample",
      "autostart": True,
      "metadata": "string",
      "runningStatus": True
    }
  ]
}

get_certificates = {
  "command": "get_certificates",
  "command_id": "abcd12354",
  "response": "success",
  "payload": [
    {
      "name": "Reader Main Certificates",
      "type": "server",
      "installTime": "Mon Jun 21 12:38:03 2021",
      "issuerName": "FX9600EE5729",
      "publickey": "string",
      "serial": "410835777",
      "subjectName": "FX9600EE5729",
      "validityStart": "21/06/2021",
      "validityEnd": "16/06/2041"
    }
  ]
}

del_certificate = {
  "command": "del_certificate",
  "command_id": "abcd1234",
  "response": "success",
  "payload": {}
}

set_updateCertificate = {
  "command": "set_updateCertificate",
  "command_id": "abcd1324",
  "response": "success",
  "payload": {}
}

set_refreshCertificate = {
  "command": "set_refreshCertificate",
  "command_id": "abcd1324",
  "response": "success",
  "payload": {}
}

set_revertbackOS = {
  "command": "set_revertbackOS",
  "command_id": "abcd1434",
  "response": "success",
  "payload": {}
}

get_gpoStatus = {
  "command": "get_gpoStatus",
  "command_id": "abdc453254",
  "response": "success",
  "payload": {
    "1": "HIGH",
    "2": "HIGH",
    "3": "HIGH",
    "4": "HIGH"
  }
}

get_gpiStatus = {
  "command": "get_gpiStatus",
  "command_id": "abcd21344",
  "response": "success",
  "payload": {
    "1": "HIGH",
    "2": "HIGH",
    "3": "HIGH",
    "4": "LOW"
  }
}

get_supportedStandardList = {
  "command": "get_supportedStandardList",
  "command_id": "gfdd",
  "payload": {
    "SupportedStandards": [
      {
        "StandardName": "Argentina",
        "isLBTConfigurable": "false",
        "channelData": [
          915250,
          915750,
          903250,
          926750,
          926250,
          904250,
          927250,
          920250,
          919250,
          909250,
          918750,
          917750,
          905250,
          904750,
          925250,
          921750,
          914750,
          906750,
          913750,
          922250,
          911250,
          911750,
          903750,
          908750,
          905750,
          912250,
          906250,
          917250,
          914250,
          907250,
          918250,
          916250,
          910250,
          910750,
          907750,
          924750,
          909750,
          919750,
          916750,
          913250,
          923750,
          908250,
          925750,
          912750,
          924250,
          921250,
          920750,
          922750,
          902750,
          923250
        ],
        "isHoppingConfigurable": "false"
      }
    ]
  },
  "response": "success"
}

get_supportedRegionList = {
  "command": "get_supportedRegionList",
  "command_id": "1a234",
  "response": "success",
  "payload": {
    "SupportedRegions": [
      "Argentina",
      "Australia",
      "Bangladesh",
      "Brazil",
      "Cambodia",
      "Canada",
      "China",
      "Colombia",
      "Costa",
      "Rica",
      "European",
      "Union",
      "Ghana",
      "Hong Kong",
      "India",
      "Indonesia",
      "Jordan",
      "Korea",
      "Laos",
      "Malaysia",
      "Mexico",
      "Morocco",
      "New Zealand",
      "Peru",
      "Philippines",
      "Russia",
      "Saudi Arabia",
      "Singapore",
      "South Africa",
      "Taiwan",
      "UAE",
      "Ukraine",
      "Venezuela",
      "Vietnam"
    ]
  }
}

set_timeZone = {
  "command": "set_timeZone",
  "command_id": "abcd1324",
  "response": "success",
  "payload": {}
}

get_timeZone = {
  "command": "get_timeZone",
  "command_id": "abdc453254",
  "response": "success",
  "payload": {
    "timeZone": "(GMT-12:00) International Date Line West"
  }
}

get_ntpServer = {
  "command": "get_ntpServer",
  "command_id": "abdc453254",
  "response": "success",
  "payload": {
    "server": "time.google.com"
  }
}

set_ntpServer = {
  "command": "set_ntpServer",
  "command_id": "abdc453254",
  "response": "success",
  "payload": {}
}

set_cableLossCompensation = {
  "command": "set_cableLossCompensation",
  "command_id": "abdc453254",
  "response": "success",
  "payload": {}
}

get_cableLossCompensation = {
  "command": "get_cableLossCompensation",
  "command_id": "abdc453254",
  "response": "success",
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

get_readerCapabilites = {
  "command": "get_readerCapabilites",
  "command_id": "abdc453254",
  "response": "success",
  "payload": {
    "capabilities": {
      "antennas": [
        {
          "port": 1,
          "type": "INTERNAL"
        }
      ],
      "apiSupported": {
        "versions": {
          "documentation": "https://zebradevs.github.io/rfid-ziotc-docs/about/index.html",
          "version": "v1"
        }
      },
      "appLedColors": [
        "RED"
      ],
      "asyncManagementEventsSupported": True,
      "beepersSupported": True,
      "clockSupport": True,
      "daAppPackageFormat": [
        "DEBIAN"
      ],
      "daAppsSupported": True,
      "daLanguageBindings": [
        "PYTHON"
      ],
      "directionalitySupported": True,
      "endpointTypesSupported": [
        {
          "SSLSupported": True,
          "authenticationTypesSupported": [
            "MTLS"
          ],
          "batchingSupported": True,
          "dataOnly": True,
          "retentionSupported": True,
          "type": "MQTT"
        }
      ],
      "externalSerialPort": [
        "NONE"
      ],
      "keypadSupport": [
        "NONE"
      ],
      "llrpSupported": True,
      "maxAppLEDs": 0,
      "maxDataEndpoints": 0,
      "maxNumOperationsInAccessSequence": 0,
      "maxNumPreFilters": 0,
      "messageFormatsSupported": [
        "JSON"
      ],
      "networkInterfaces": [
        {
          "802.1x": True,
          "internal": True,
          "ipAssignment": [
            "STATIC"
          ],
          "ipStack": [
            "IPv4"
          ],
          "type": "ETHERNET"
        }
      ],
      "numGPIs": 0,
      "numGPOs": 0,
      "restAPISupported": True,
      "rssiFilterSupported": True,
      "supportedDisplayType": [
        "NONE"
      ],
      "supportedPowerSource": [
        "DC"
      ],
      "supportedTagDataFormat": [
        "GS1"
      ],
      "tagLocationingSupported": True,
      "triggers": [
        "GPI"
      ]
    }
  }
}

set_nameAndDescription = {
  "command": "set_nameAndDescription",
  "command_id": "abdc453254",
  "response": "success",
  "payload": {}
}

get_nameAndDescription = {
  "command": "get_nameAndDescription",
  "command_id": "abdc453254",
  "response": "success",
  "payload": {
    "name": "string",
    "description": "string"
  }
}

tag = {
  "type": "SIMPLE",
  "timestamp": "2019-08-24T14:15:22Z",
  "data": {
    "CRC": "b06a",
    "PC": "3000",
    "TID": "e20060030178529d",
    "USER": "123433331234567812345678",
    "antenna": 1,
    "channel": 911.75,
    "eventNum": 1,
    "format": "epc",
    "idHex": "3005fb63ac1f3681ec880468",
    "peakRssi": -39,
    "phase": 0,
    "reads": 1,
    "XPC": "string",
    "accessResults": [
      "SUCCESS"
    ]
  }
}

reportRequest = {
  "command": "reportRequest",
  "command_id": "rfid123",
  "response": "success",
  "payload": {
    "SessionStartTime": "2019-08-24T14:15:22Z",
    "SessionEndTime": "2019-08-24T14:21:99Z",
    "data": [
      {"antenna": "checkAntenna",
       "channel": 911.75,
       "epc": "3005fb63ac1f3681ec880468",
       "peakRssi": -39,
       "phase": 0,
       "timeStamp": "2019-08-24T14:15:23Z"
       },
      {"antenna": "baggingAntenna",
       "channel": 911.75,
       "epc": "3005fb63ac1f3681ec880468",
       "peakRssi": -21,
       "phase": 0,
       "timeStamp": "2019-08-24T14:15:24Z"
       }
    ]

  }
}

analysisRequest = {
  "command": " analysisRequest ",
  "command_id": "rfid223",
  "response": "success",
  "payload": {
    "SessionStartTime": "2019-08-24T14:15:22Z",
    "SessionEndTime": "2019-08-24T14:21:99Z",
    "data": [
      {"epc": "3005fb63ac1f3681ec880468",
       "baggingAreaIndicator": True,
       "checkIndicator": True,
       "cartAreaIndicator:": False,
       },
      {"epc": "3005fb63ac1f3681ec880469",
       "baggingAreaIndicator": True,
       "checkIndicator": False,
       "cartAreaIndicator:": False,
       },
      {"epc": "3005fb63ac1f3681ec880470",
       "baggingAreaIndicator": False,
       "checkIndicator": True,
       "cartAreaIndicator:": True,
       }
    ]

  }
}
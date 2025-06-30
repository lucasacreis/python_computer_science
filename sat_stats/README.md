# Satellite Data Analisys

Under construction!

## Collect data

Collects satellite data from Station INPE EMMN's API and save them in an '.xlsx' file.

## Beacon Saver

Import the BeaconDecoder¹ to decode the information from the telemetries and save them in a '.JSON' file.

¹Platform-1 BeaconDecoder is not avaible to public repositories due to Endurosat's policies.

## Satellite Report

Under construction... May produce relevant satellite statistics data graphics to report.

## Directory structure

Under construction...

```tree
sat_stats/
├── data/
│   └── sat-<id>/
│       └── <Year-month>/
│           ├── telemetry/
│           │   └── <Initial date (Y-m-d)>_<Final date (Y-m-d)>_sat-<id>_telemetry.xlsx
│           ├── status/
│           │   └── <Initial date (Y-m-d)>_<Final date (Y-m-d)>_sat-<id>_status.json
│           ├── graphs/
│           │   ├── <Initial date (Y-m-d)>_<Final date (Y-m-d)>_sat-<id>_graph_crc.png
│           │   ├── <Initial date (Y-m-d)>_<Final date (Y-m-d)>_sat-<id>_graph_handshakes.png
│           │   ├── <Initial date (Y-m-d)>_<Final date (Y-m-d)>_sat-<id>_graph_mcu-temp.png
│           │   ├── <Initial date (Y-m-d)>_<Final date (Y-m-d)>_sat-<id>_graph_memory.png
│           │   ├── <Initial date (Y-m-d)>_<Final date (Y-m-d)>_sat-<id>_graph_packets.png
│           │   └── <Initial date (Y-m-d)>_<Final date (Y-m-d)>_sat-<id>_graph_por.png
│           └── report/
│               └── <Initial date (Y-m-d)>_<Final date (Y-m-d)>_sat-<id>_report.png
└── lib/
    ├── collect_data.py
    ├── beacon_reader.py
    ├── beacon_saver.py
    └── sattelite_report.py
```

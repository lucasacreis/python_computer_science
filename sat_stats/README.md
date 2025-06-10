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
│   └── sat-19/
│       └── 2025-05/
│           ├── telemetry/
│           │   └── 2025-05-01_2025-05-31_sat-19_telemetry.xlsx
│           ├── status/
│           │   └── 2025-05-01_2025-05-31_sat-19_status.json
│           ├── graphs/
│           │   ├── 2025-05-01_2025-05-31_sat-19_graph_crc.png
│           │   ├── 2025-05-01_2025-05-31_sat-19_graph_handshakes.png
│           │   ├── 2025-05-01_2025-05-31_sat-19_graph_mcu-temp.png
│           │   ├── 2025-05-01_2025-05-31_sat-19_graph_memory.png
│           │   ├── 2025-05-01_2025-05-31_sat-19_graph_packets.png
│           │   └── 2025-05-01_2025-05-31_sat-19_graph_por.png
│           └── report/
│               └── 2025-05-01_2025-05-31_sat-19_report.png
└── lib/
    ├── collect_data.py
    ├── beacon_reader.py
    ├── beacon_saver.py
    └── sattelite_report.py
```

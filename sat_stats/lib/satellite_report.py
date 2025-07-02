# Graph Builder for SAT Statistics
# This module provides functionality to build a graph from SAT statistics data.
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_args, get_user_inputs, search_files

"""
=======================================================================================================
                Geração de gráficos de beacons de satélites EMMN INPE - Versão: 1.0
                Data: 2025-06-06 - por Lucas Reis                    
=======================================================================================================
Este script coleta dados de beacons de satélites salvos e gera gráficos a partir desses dados.
Ele permite que o usuário especifique o ID do satélite e o intervalo de datas para a coleta.
O script pesquisa dados de JSON salvos referentes ao intervalo de datas para busca, gera gráficos
e salva-os em arquivos PNG.
=======================================================================================================
Uso:
python satellite_report.py --sat_id <ID_DO_SATÉLITE> --time_init <DATA_INICIAL> --time_end <DATA_FINAL>
Ou, se os argumentos não forem passados, o usuário será solicitado a inseri-los interativamente.
=======================================================================================================
"""

if __name__ == "__main__":
    # Checagem de argumentos
    args = get_args()
    # Se argumentos não foram passados, usa input interativo
    args = get_user_inputs(args)
    sat_id = args.sat_id
    time_init = args.time_init
    time_end = args.time_end
    path_base = f"sat_stats/data/sat_{sat_id}/"

    # Procurar arquivos de status sat_stats/data/sat_19/2025-05/
    arquivos = search_files(args, 'status', 'json')
    print(f"Arquivos encontrados: {arquivos}")
    if not arquivos:
        print("Nenhum arquivo encontrado para o satélite especificado.")
        exit(1)

    # === 1. Carregar dados dos arquivos JSON ===
    beacons = []
    for arq in arquivos:
        path_name = f"{path_base}{arq[22:30]}graphs/"
        os.makedirs(path_name, exist_ok=True)
        with open(arq, "r") as f:
            beacons.extend(json.load(f))

        prefix = arq[37:65]

        # === 2. Filtrar e preparar dados de tipo 02 (UHF Stats) ===
        uhf_stats = [b for b in beacons if b["decoded"].get("type") == "02"]
        print(f"Número de beacons do tipo 02 (UHF Stats): {len(uhf_stats)}")

        # Criar DataFrame
        df = pd.DataFrame([{
            "timestamp": pd.to_datetime(b["timestamp"]),
            "MCU_Temp": b["decoded"].get("MCU_Temp"),
            "Tx_Packets": b["decoded"].get("Tx_Packets"),
            "Rx_Packets": b["decoded"].get("Rx_Packets"),
            "RxPackets_CrcErr": b["decoded"].get("RxPackets_CrcErr"),
        } for b in uhf_stats])

        df["CRC_Error_Rate"] = 100 * df["RxPackets_CrcErr"] / df["Rx_Packets"]

        # === 3. Plotar gráficos ===
        plt.style.use("seaborn-v0_8-darkgrid")

        # Temperatura do MCU
        plt.figure(figsize=(10, 4))
        plt.plot(df["timestamp"], df["MCU_Temp"], marker='o', linestyle='--', label="MCU Temp (°C)")
        plt.title("Temperatura do MCU ao longo do tempo")
        plt.xlabel("Timestamp")
        plt.ylabel("Temperatura (°C)")
        # --- Annotate First Point ---
        first_timestamp = df["timestamp"].iloc[0]
        first_mcu_temp = df["MCU_Temp"].iloc[0]
        plt.text(first_timestamp, first_mcu_temp, f'{first_mcu_temp}°C',
                verticalalignment='bottom', horizontalalignment='right', color='blue')

        # --- Annotate Last Point ---
        last_timestamp = df["timestamp"].iloc[-1]
        last_mcu_temp = df["MCU_Temp"].iloc[-1]
        plt.text(last_timestamp, last_mcu_temp, f'{last_mcu_temp}°C',
                 verticalalignment='bottom', horizontalalignment='left', color='red')

        plt.tight_layout()
        plt.savefig(f"{path_name}{prefix}_graph_mcu-temp.png")

        # Pacotes Tx e Rx
        plt.figure(figsize=(10, 4))
        plt.plot(df["timestamp"], df["Tx_Packets"], marker='o', linestyle='--', label="Tx_Packets")
        plt.plot(df["timestamp"], df["Rx_Packets"], marker='o', linestyle='--', label="Rx_Packets")
        plt.title("Pacotes Transmitidos e Recebidos")
        plt.xlabel("Timestamp")
        plt.ylabel("Número de Pacotes")
        plt.legend()
        # --- Annotate First Point ---
        first_timestamp = df["timestamp"].iloc[0]
        first_tx_packets = df["Tx_Packets"].iloc[0]
        first_rx_packets = df["Rx_Packets"].iloc[0]
        plt.text(first_timestamp, first_tx_packets, f'{first_tx_packets} Tx',
                verticalalignment='bottom', horizontalalignment='right', color='blue')
        plt.text(first_timestamp, first_rx_packets, f'{first_rx_packets} Rx',
                verticalalignment='bottom', horizontalalignment='right', color='orange')

        # --- Annotate Last Point ---
        last_timestamp = df["timestamp"].iloc[-1]
        last_tx_packets = df["Tx_Packets"].iloc[-1]
        last_rx_packets = df["Rx_Packets"].iloc[-1]
        plt.text(last_timestamp, last_tx_packets, f'{last_tx_packets} Tx',
                 verticalalignment='bottom', horizontalalignment='left', color='blue')
        plt.text(last_timestamp, last_rx_packets, f'{last_rx_packets} Rx',
                 verticalalignment='bottom', horizontalalignment='left', color='orange')
        
        plt.tight_layout()
        plt.savefig(f"{path_name}{prefix}_graph_packets.png")

        # Taxa de erro CRC
        plt.figure(figsize=(10, 4))
        plt.plot(df["timestamp"], df["CRC_Error_Rate"], color='red', marker='o', linestyle='--', label="Taxa de Erro CRC")
        plt.title("Taxa de Erro CRC em Pacotes Recebidos (%)")
        plt.xlabel("Timestamp")
        plt.ylabel("Erro CRC (%)")
        # --- Annotate First Point ---
        first_timestamp = df["timestamp"].iloc[0]
        first_crc_error = round(df["CRC_Error_Rate"].iloc[0],3)
        plt.text(first_timestamp, first_crc_error, f'{first_crc_error}%',
                verticalalignment='bottom', horizontalalignment='right', color='blue')

        # --- Annotate Last Point ---
        last_timestamp = df["timestamp"].iloc[-1]
        last_crc_error = round(df["CRC_Error_Rate"].iloc[-1],3)
        plt.text(last_timestamp, last_crc_error, f'{last_crc_error}%',
                 verticalalignment='bottom', horizontalalignment='left', color='red')
        plt.tight_layout()
        plt.savefig(f"{path_name}{prefix}_graph_crc.png")

        # === 4. Filtrar e preparar dados de tipo 03 (Debug) ===
        debug_data = [b for b in beacons if b["decoded"].get("type") == "03"]

        df_debug = pd.DataFrame([{
            "timestamp": pd.to_datetime(b["timestamp"]),
            "ConOpsMode": b["decoded"].get("ConOpsMode"),
            "POR": b["decoded"].get("POR"),
            "GS_Handshakes": b["decoded"].get("GS_Handshakes"),
            "NvMWriteFails": b["decoded"].get("NvMWriteFails"),
            "NvMReadFails": b["decoded"].get("NvMReadFails"),
            "ExtFRAM_corruptions": b["decoded"].get("ExtFRAM_corruptions"),
            "ExtFRAM_gone": b["decoded"].get("ExtFRAM_gone"),
        } for b in debug_data])

        # === 5. Plotar gráficos para debug ===

        # POR (Power-On Resets)
        plt.figure(figsize=(10, 4))
        plt.plot(df_debug["timestamp"], df_debug["POR"], marker='o', linestyle='--', color='orange')
        plt.title("Contador de Reinicializações (POR)")
        plt.xlabel("Timestamp")
        plt.ylabel("POR")
        # --- Annotate First Point ---
        first_timestamp = df_debug["timestamp"].iloc[0]
        first_por = round(df_debug["POR"].iloc[0],3)
        plt.text(first_timestamp, first_por, f'{first_por}%',
                verticalalignment='bottom', horizontalalignment='right', color='blue')

        # --- Annotate Last Point ---
        last_timestamp = df_debug["timestamp"].iloc[-1]
        last_por = round(df_debug["POR"].iloc[-1],3)
        plt.text(last_timestamp, last_por, f'{last_por}%',
                 verticalalignment='bottom', horizontalalignment='left', color='red')
        plt.tight_layout()
        plt.savefig(f"{path_name}{prefix}_graph_por.png")

        # Falhas de memória externa
        plt.figure(figsize=(10, 4))
        plt.plot(df_debug["timestamp"], df_debug["ExtFRAM_corruptions"], label="FRAM Corruptions")
        plt.plot(df_debug["timestamp"], df_debug["ExtFRAM_gone"], label="FRAM Gone")
        plt.title("Falhas de Memória Externa")
        plt.xlabel("Timestamp")
        plt.ylabel("Contagem")
        plt.legend()
        # --- Annotate First Point ---
        first_timestamp = df_debug["timestamp"].iloc[0]
        first_ExtFRAMCorruptions = df_debug["ExtFRAM_corruptions"].iloc[0]
        first_ExtFRAMGone = df_debug["ExtFRAM_gone"].iloc[0]
        plt.text(first_timestamp, first_ExtFRAMCorruptions, f'{first_ExtFRAMCorruptions}',
                verticalalignment='bottom', horizontalalignment='right', color='blue')
        plt.text(first_timestamp, first_ExtFRAMGone, f'{first_ExtFRAMGone}',
                verticalalignment='bottom', horizontalalignment='right', color='blue')

        # --- Annotate Last Point ---
        last_timestamp = df_debug["timestamp"].iloc[-1]
        last_ExtFRAMCorruptions = df_debug["ExtFRAM_corruptions"].iloc[-1]
        last_ExtFRAMGone = df_debug["ExtFRAM_gone"].iloc[-1]
        plt.text(last_timestamp, last_ExtFRAMCorruptions, f'{last_ExtFRAMCorruptions}',
                 verticalalignment='bottom', horizontalalignment='left', color='red')
        plt.text(last_timestamp, last_ExtFRAMGone, f'{last_ExtFRAMGone}',
                 verticalalignment='bottom', horizontalalignment='left', color='red')
        plt.tight_layout()
        plt.savefig(f"{path_name}{prefix}_graph_memory.png")

        # GS Handshakes
        plt.figure(figsize=(10, 4))
        plt.plot(df_debug["timestamp"], df_debug["GS_Handshakes"], color='green')
        plt.title("Acúmulo de Handshakes com Estação Terrena")
        plt.xlabel("Timestamp")
        plt.ylabel("Contagem")
        # --- Annotate First Point ---
        first_timestamp = df_debug["timestamp"].iloc[0]
        first_handshakes = df_debug["GS_Handshakes"].iloc[0]
        plt.text(first_timestamp, first_handshakes, f'{first_handshakes}',
                verticalalignment='bottom', horizontalalignment='right', color='blue')
        # --- Annotate Last Point ---
        last_timestamp = df_debug["timestamp"].iloc[-1]
        last_handshakes = df_debug["GS_Handshakes"].iloc[-1]
        plt.text(last_timestamp, last_handshakes, f'{last_handshakes}',
                 verticalalignment='bottom', horizontalalignment='left', color='red')
        plt.tight_layout()
        plt.savefig(f"{path_name}{prefix}_graph_handshakes.png")

        print(f"Gráficos salvos com sucesso em {path_name}.")

# Graph Builder for SAT Statistics
# This module provides functionality to build a graph from SAT statistics data.
import os
import json
import pandas as pd
import matplotlib.pyplot as plt
from utils import get_args, get_user_inputs, search_files

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

        df["CRC_Error_Rate"] = df["RxPackets_CrcErr"] / df["Rx_Packets"]

        # === 3. Plotar gráficos ===
        plt.style.use("seaborn-v0_8-darkgrid")

        # Temperatura do MCU
        plt.figure(figsize=(10, 4))
        plt.plot(df["timestamp"], df["MCU_Temp"], marker='o', label="MCU Temp (°C)")
        plt.title("Temperatura do MCU ao longo do tempo")
        plt.xlabel("Timestamp")
        plt.ylabel("Temperatura (°C)")
        plt.tight_layout()
        plt.savefig(f"{path_name}grafico_mcu_temp.png")

        # Pacotes Tx e Rx
        plt.figure(figsize=(10, 4))
        plt.plot(df["timestamp"], df["Tx_Packets"], label="Tx_Packets")
        plt.plot(df["timestamp"], df["Rx_Packets"], label="Rx_Packets")
        plt.title("Pacotes Transmitidos e Recebidos")
        plt.xlabel("Timestamp")
        plt.ylabel("Número de Pacotes")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{path_name}grafico_pacotes.png")

        # Taxa de erro CRC
        plt.figure(figsize=(10, 4))
        plt.plot(df["timestamp"], df["CRC_Error_Rate"], color='red', marker='x')
        plt.title("Taxa de Erro CRC em Pacotes Recebidos")
        plt.xlabel("Timestamp")
        plt.ylabel("Erro CRC (%)")
        plt.tight_layout()
        plt.savefig(f"{path_name}grafico_crc.png")

        print("Gráficos salvos com sucesso.")

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
        plt.plot(df_debug["timestamp"], df_debug["POR"], marker='o')
        plt.title("Contador de Reinicializações (POR)")
        plt.xlabel("Timestamp")
        plt.ylabel("POR")
        plt.tight_layout()
        plt.savefig(f"{path_name}grafico_por.png")

        # Falhas de memória externa
        plt.figure(figsize=(10, 4))
        plt.plot(df_debug["timestamp"], df_debug["ExtFRAM_corruptions"], label="FRAM Corruptions")
        plt.plot(df_debug["timestamp"], df_debug["ExtFRAM_gone"], label="FRAM Gone")
        plt.title("Falhas de Memória Externa")
        plt.xlabel("Timestamp")
        plt.ylabel("Contagem")
        plt.legend()
        plt.tight_layout()
        plt.savefig(f"{path_name}grafico_memoria.png")

        # GS Handshakes
        plt.figure(figsize=(10, 4))
        plt.plot(df_debug["timestamp"], df_debug["GS_Handshakes"], color='green')
        plt.title("Acúmulo de Handshakes com Estação Terrena")
        plt.xlabel("Timestamp")
        plt.ylabel("Contagem")
        plt.tight_layout()
        plt.savefig(f"{path_name}grafico_handshakes.png")

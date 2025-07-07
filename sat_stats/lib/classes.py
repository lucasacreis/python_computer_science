import os
import sys
import json
import requests
import getpass
import pandas as pd
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime, time
from lib.beacon_reader import BeaconDecoder

class satellite_data:
    def __init__ (self, get_args, get_user_inputs, search_files, save_json):
        # Checagem de argumentos
        self.args = get_args()
        # Se argumentos não foram passados, usa input interativo
        self.args = get_user_inputs(self.args)

        self.sat_id = self.args.sat_id
        self.time_init = self.args.time_init
        self.time_end = self.args.time_end

        # Inicializa as funções auxiliares
        self.search_files = search_files
        self.save_json = save_json

    
    def collect_data(self):
        """
        ===================================================================================================
        Coleta dados de telemetria de satélites a partir do API station da EMMN INPE.
        O script autentica o usuário, faz a requisição dos dados e salva os resultados em um arquivo Excel.
        ===================================================================================================
        """

        # Define a URL para coletar os dados de telemetria
        url = f"http://station/satelites/Satellite/communications/{self.sat_id}/?time_init={self.time_init}&time_end={self.time_end}&tipo=telemetrias&qtd_linhas=50"
        usuario = input("=> Digite o nome de usuário: ")
        senha = getpass.getpass("=> Digite a senha: ")
        # Cria uma sessão autenticada
        try:
            session = requests.Session()
            login_url = "http://station/login/"
        except requests.RequestException as e:
            print(f"=> Erro ao criar sessão: {e}")
            sys.exit(1)
        try:
            # Obtém o token CSRF da página de login
            resp = session.get(login_url)
            resp.raise_for_status()
            resp = session.get(login_url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            csrf_token = soup.find("input", attrs={"name": "csrfmiddlewaretoken"}).get("value")
        except requests.RequestException as e:
            print(f"=> Erro ao acessar a URL de login: {e}")
            sys.exit(1)
        if not csrf_token:
            print("=> Token CSRF não encontrado na página de login.")
            sys.exit(1)
        try:
            print("===========================================================================================")
            print(f"=================           AUTENTICANDO USUÁRIO: {usuario:<11}           ===================")
            print("===========================================================================================")
            # Envia os dados de login
            login_data = {
                "username": usuario,
                "password": senha,
                "csrfmiddlewaretoken": csrf_token
            }
            headers = {"Referer": login_url}
            session.post(login_url, data=login_data, headers=headers)
        except requests.RequestException as e:
            print(f"=> Erro ao enviar dados de login: {e}")
            sys.exit(1)
        if "Login" in session.get(login_url).text:
            print("=> Falha no login. Verifique suas credenciais.")
            sys.exit(1)
        try:
            print("=> Usuário autenticado com sucesso.")
            print("===========================================================================================")
            print(f"============      COLETANDO DADOS DE TELEMETRIA DO SATÉLITE {self.sat_id} EM STATION      ============")
            print("===========================================================================================")
            # Acessa a URL de telemetria
            res = session.get(url)
            soup = BeautifulSoup(res.text, 'html.parser')
            rows = soup.select("table tr")[1:]
        except requests.RequestException as e:
            print(f"=> Erro ao acessar a URL de telemetria: {e}")
            sys.exit(1)
        if not rows:
            print("=> Nenhuma linha de dados encontrada na tabela.")
            sys.exit(1)
        try:
            # Extrai os dados da tabela
            dados = []
            for row in rows:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    timestamp = cols[0].text.strip()
                    telemetria = cols[1].text.strip()
                    dados.append({"timestamp": timestamp, "telemetria": telemetria})

            # Cria um DataFrame a partir dos dados extraídos
            df = pd.DataFrame(dados)
            if df.empty:
                raise ValueError("=> Nenhum dado foi extraído da tabela.")

            # Organização das pastas: os.path/data/sat_<id>/<ano-mês>/telemetry
            sat_folder = f"data/sat_{self.sat_id}/"
            year_month = self.time_init[:7]
            save_folder = os.path.join(sat_folder, year_month, 'telemetry')
            os.makedirs(save_folder, exist_ok=True)

            # Salva o DataFrame em um arquivo Excel: <daata_inicial>_to_<data_final>_sat-<id>-telemetry.xlsx
            xlsx_name = os.path.join(
                save_folder,
                f"{self.time_init}_to_{self.time_end}_sat-{self.sat_id}-telemetry.xlsx"
            )
            df.to_excel(xlsx_name, index=False)
            print(f"=> Dados encontrados e salvos com sucesso em:\n{xlsx_name}")
            print("===========================================================================================")
        except Exception as e:
            print(f"=> Erro ao processar os dados: {e}")
            sys.exit(1)
        try:
            # Exibe as primeiras linhas do DataFrame
            print("=> Exibindo as primeiras linhas do DataFrame:")
            print("===========================================================================================")
            print(df.head())
        except Exception as e:
            print(f"=> Erro ao exibir o DataFrame: {e}")
            sys.exit(1)


    def beacon_saver(self):
        """
        ===================================================================================================
        Coleta telemetrias salvas de beacons de satélites e as organiza em um arquivo JSON.
        O script pesquisa dados de excel salvos referentes ao intervalo de datas para busca, realiza a 
        decodificação dos beacons e salva os resultados em um arquivo JSON.
        ===================================================================================================
        """

        print("===========================================================================================")
        print(f"============         PROCESSANDO DADOS DE TELEMETRIA DO SATÉLITE {self.sat_id}            ============")
        print("===========================================================================================")
        # Procura arquivos de telemetria
        arquivos = self.search_files(self.args, 'telemetry', 'xlsx')
        if not arquivos:
            print("=> Nenhum arquivo encontrado para os parâmetros informados.")
            exit(1)
        
        # Processamento dos arquivos encontrados
        resultados_dict = {}
        time_init = datetime.combine(datetime.strptime(self.time_init, "%Y-%m-%d").date(), time.min)
        time_end = datetime.combine(datetime.strptime(self.time_end, "%Y-%m-%d").date(), time.max)

        # Inicializa o decodificador de beacons
        decoder = BeaconDecoder()
        print(f"===========================================================================================")
        print(f"=> Processando {len(arquivos)} arquivos entre {time_init} e {time_end}...")
        for arquivo in arquivos:
            try:
                df = pd.read_excel(arquivo)
                # print(f"Lendo arquivo: {arquivo}")
            except Exception as e:
                print(f"=> Erro ao ler {arquivo}: {e}")
                continue
            for _, row in df.iterrows():
                try:
                    timestamp = pd.to_datetime(row['timestamp'], dayfirst=True)
                    # print(f"Processando timestamp: {timestamp}")
                except Exception:
                    print(f"=> Erro ao converter timestamp: {row['timestamp']}")
                    continue
                if not (time_init <= timestamp <= time_end):
                    # print(f"Timestamp {timestamp} fora do intervalo {time_init} a {time_end}. Ignorando.")
                    continue
                frame = str(row['telemetria'])
                chave = (str(timestamp), frame)
                if chave in resultados_dict:
                    continue  # Dados são ignorados se já foram processados
                decoded = decoder.decode(frame)
                resultados_dict[chave] = {
                    "timestamp": str(timestamp),
                    "frame": frame,
                    "decoded": decoded
                }
        # Seleciona apenas os valores únicos
        resultados = list(resultados_dict.values())

        if not resultados:
            print("=> Nenhum frame encontrado no intervalo informado.")
            exit(1)
        self.save_json(self.args, resultados)

    def graph_builder(self):
        """
        =======================================================================================================
        Coleta dados de beacons de satélites salvos e gera gráficos a partir desses dados.
        O script pesquisa dados de JSON salvos referentes ao intervalo de datas para busca, gera gráficos
        e salva-os em arquivos PNG.
        =======================================================================================================
        """

        print("===========================================================================================")
        print(f"============                 GERANDO GRÁFICOS DO SATÉLITE {self.sat_id}                   ============")
        print("===========================================================================================")
        path_base = f"data/sat_{self.sat_id}/"

        # Procurar arquivos de status sat_stats/data/sat_19/2025-05/
        arquivos = self.search_files(self.args, 'status', 'json')
        print("===========================================================================================")
        if not arquivos:
            print("=> Nenhum arquivo encontrado para o satélite especificado.")
            exit(1)
        
        print(f"=> Arquivos encontrados:")
        for i, arq in enumerate(arquivos):
            print(f"{i}: {arq}")

        print("===========================================================================================")
        confirm = input("=> Deseja gerar gráficos para todos os arquivos? (s/n)")
        if confirm.lower() != 's':
            select_files = input("=> Informe os indices dos arquivos desejados, separados por vírgula: ")
            arquivos = [arquivos[int(i)] for i in select_files.split(',') if i.isdigit() and 0 <= int(i) < len(arquivos)]

        print("===========================================================================================")
        # === 1. Carregar dados dos arquivos JSON ===
        beacons = []
        for arq in arquivos:
            prefix = arq[27:55]
            print(f"=> Processando arquivo: {arq}")
            # Cria o diretório para os gráficos, se não existir
            path_name = f"{path_base}{prefix[:7]}/graphs/"
            os.makedirs(path_name, exist_ok=True)
            with open(arq, "r") as f:
                beacons.extend(json.load(f))


            # === 2. Filtrar e preparar dados de tipo 02 (UHF Stats) ===
            uhf_stats = [b for b in beacons if b["decoded"].get("type") == "02"]
            print(f"=> Número de beacons do tipo 02 (UHF Stats): {len(uhf_stats)}")
            print("===========================================================================================")

            if not uhf_stats:
                print("=> Nenhum dado do tipo 02 (UHF Stats) encontrado.")
                continue

            # Criar DataFrame
            df = pd.DataFrame([{
                "timestamp": pd.to_datetime(b["timestamp"]),
                "MCU_Temp": b["decoded"].get("MCU_Temp"),
                "Tx_Packets": b["decoded"].get("Tx_Packets"),
                "Rx_Packets": b["decoded"].get("Rx_Packets"),
                "RxPackets_CrcErr": b["decoded"].get("RxPackets_CrcErr"),
            } for b in uhf_stats])

            df["CRC_Error_Rate"] = 100 * df["RxPackets_CrcErr"] / df["Rx_Packets"]

            # Ordena o DataFrame por timestamp
            df = df.sort_values('timestamp').reset_index(drop=True)

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

            # Ordena o DataFrame por timestamp
            df_debug = df_debug.sort_values('timestamp').reset_index(drop=True)

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

            print(f"=> Gráficos salvos com sucesso em:\n{path_name}.")
            print("===========================================================================================")

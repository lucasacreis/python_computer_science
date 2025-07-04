from datetime import datetime, time
import pandas as pd
from utils import get_args, get_user_inputs, search_files, save_json
from beacon_reader import BeaconDecoder

"""
===================================================================================================
                Salvar dados de beacons de satélites EMMN INPE - Versão: 1.0
                Data: 2025-06-06 - por Lucas Reis                    
===================================================================================================
Este script coleta telemetrias salvas de beacons de satélites e as organiza em um arquivo JSON.
Ele permite que o usuário especifique o ID do satélite e o intervalo de datas para busca.
O script pesquisa dados de excel salvos referentes ao intervalo de datas para busca, realiza a 
decodificação dos beacons e salva os resultados em um arquivo JSON.
===================================================================================================
Uso:
python beacon_saver.py --sat_id <ID_DO_SATÉLITE> --time_init <DATA_INICIAL> --time_end <DATA_FINAL>
Ou, se os argumentos não forem passados, o usuário será solicitado a inseri-los interativamente.
===================================================================================================
"""

class BeaconSaver:
    def __init__(self, get_args, get_user_inputs):
        # Checagem de argumentos
        self.get_args = get_args
        # Se argumentos não foram passados, usa input interativo
        self.get_user_inputs = get_user_inputs

        self.sat_id = self.args.sat_id
        self.time_init = self.args.time_init
        self.time_end = self.args.time_end

    def run(self):
        # Procura arquivos de telemetria
        arquivos = search_files(self.args, 'telemetry', 'xlsx')
        if not arquivos:
            print("Nenhum arquivo encontrado para os parâmetros informados.")
            exit(1)
        
        # Processamento dos arquivos encontrados
        resultados_dict = {}
        time_init = datetime.combine(datetime.strptime(self.time_init, "%Y-%m-%d").date(), time.min)
        time_end = datetime.combine(datetime.strptime(self.time_end, "%Y-%m-%d").date(), time.max)

        # Inicializa o decodificador de beacons
        decoder = BeaconDecoder()
        print(f"Processando {len(arquivos)} arquivos entre {time_init} e {time_end}...")
        for arquivo in arquivos:
            try:
                df = pd.read_excel(arquivo)
                # print(f"Lendo arquivo: {arquivo}")
            except Exception as e:
                print(f"Erro ao ler {arquivo}: {e}")
                continue
            for _, row in df.iterrows():
                try:
                    timestamp = pd.to_datetime(row['timestamp'], dayfirst=True)
                    # print(f"Processando timestamp: {timestamp}")
                except Exception:
                    print(f"Erro ao converter timestamp: {row['timestamp']}")
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
            print("Nenhum frame encontrado no intervalo informado.")
            exit(1)
        save_json(self.args, resultados)


if __name__ == "__main__":
    BeaconSaver()

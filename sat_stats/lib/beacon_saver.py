import os
import json
from datetime import datetime, time
import pandas as pd
from utils import get_args, get_user_inputs, search_files
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

def save_json(sat_id, time_init, time_end, resultados):
    print(f"Salvando {len(resultados)} resultados de telemetria para o satélite {sat_id} de {time_init} a {time_end}...")
    sat_folder = f"sat_stats/data/sat_{sat_id}"
    year_month = time_init[:7]
    save_folder = os.path.join(sat_folder, year_month, 'status')
    os.makedirs(save_folder, exist_ok=True)
    nome_arquivo = f"stats_{sat_id}_{time_init}_{time_end}.json"
    caminho = os.path.join(save_folder, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"Resultados salvos em {caminho}")


if __name__ == "__main__":
    # Checagem de argumentos
    args = get_args()

    # Se argumentos não foram passados, usa input interativo
    args = get_user_inputs(args)
    time_init = args.time_init
    time_end = args.time_end

    # Procura arquivos de telemetria
    arquivos = search_files(args, 'telemetry', 'xlsx')
    if not arquivos:
        print("Nenhum arquivo encontrado para os parâmetros informados.")
        exit(1)
    
    # Processamento dos arquivos encontrados
    resultados_dict = {}
    time_init = datetime.combine(datetime.strptime(time_init, "%Y-%m-%d").date(), time.min)
    time_end = datetime.combine(datetime.strptime(time_end, "%Y-%m-%d").date(), time.max)
    
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
    save_json(args.sat_id, args.time_init, args.time_end, resultados)

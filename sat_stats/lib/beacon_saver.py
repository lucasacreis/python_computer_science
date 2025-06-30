import argparse
import os
import glob
import json
from datetime import datetime, time
import pandas as pd

from beacon_reader import BeaconDecoder

"""
Descrição...
Melhorar organização de arquivos salvos.
"""

def parse_args():
    parser = argparse.ArgumentParser(description="Decodifica e salva frames de satélite.")
    parser.add_argument('--sat_id', type=str, help='ID do satélite')
    parser.add_argument('--data_inicio', type=str, help='Data inicial (YYYY-MM-DD)')
    parser.add_argument('--data_fim', type=str, help='Data final (YYYY-MM-DD)')
    args = parser.parse_args()
    return args

def solicitar_dados_faltantes(args):
    if not args.sat_id:
        args.sat_id = input("Informe o ID do satélite: ")
    if not args.data_inicio:
        args.data_inicio = input("Informe a data inicial (YYYY-MM-DD): ")
    if not args.data_fim:
        args.data_fim = input("Informe a data final (YYYY-MM-DD): ")
    return args

def buscar_arquivos(sat_id, data_inicio, data_fim):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_base = os.path.join(base_dir, "data", f"sat_{sat_id}")
    data_ini = datetime.strptime(data_inicio, "%Y-%m-%d")
    data_fim = datetime.strptime(data_fim, "%Y-%m-%d")
    arquivos = []
    meses = set()
    atual = data_ini.replace(day=1)
    while atual <= data_fim:
        meses.add(atual.strftime("%Y-%m"))
        if atual.month == 12:
            atual = atual.replace(year=atual.year+1, month=1)
        else:
            atual = atual.replace(month=atual.month+1)
    # print(f"Buscando arquivos em: {pasta_base} para os meses: {', '.join(sorted(meses))}")
    for ano_mes in meses:
        pasta = os.path.join(pasta_base, ano_mes)
        print(f"Verificando pasta: {os.path.abspath(pasta)}")
        if os.path.exists(pasta):
            # print(f"Encontrando arquivos em: {pasta}")
            for arq in glob.glob(os.path.join(pasta, "*.xlsx")):
                # print(f"Arquivo encontrado: {arq}")
                arquivos.append(arq)
    return arquivos

def processar_arquivos(arquivos, data_inicio, data_fim):
    resultados_dict = {}
    data_ini = datetime.combine(datetime.strptime(data_inicio, "%Y-%m-%d").date(), time.min)
    data_fim = datetime.combine(datetime.strptime(data_fim, "%Y-%m-%d").date(), time.max)
    decoder = BeaconDecoder()
    print(f"Processando {len(arquivos)} arquivos entre {data_ini} e {data_fim}...")
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
            if not (data_ini <= timestamp <= data_fim):
                # print(f"Timestamp {timestamp} fora do intervalo {data_inicio} a {data_fim}. Ignorando.")
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
    # Retorna apenas os valores únicos
    return list(resultados_dict.values())

def salvar_json(sat_id, data_inicio, data_fim, resultados):
    print(f"Salvando {len(resultados)} resultados de telemetria para o satélite {sat_id} de {data_inicio} a {data_fim}...")
    pasta_saida = f"sat_stats/stats/sat_{sat_id}"
    os.makedirs(pasta_saida, exist_ok=True)
    nome_arquivo = f"stats_{sat_id}_{data_inicio}_{data_fim}.json"
    caminho = os.path.join(pasta_saida, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"Resultados salvos em {caminho}")

if __name__ == "__main__":
    args = parse_args()
    args = solicitar_dados_faltantes(args)
    arquivos = buscar_arquivos(args.sat_id, args.data_inicio, args.data_fim)
    if not arquivos:
        print("Nenhum arquivo encontrado para os parâmetros informados.")
        exit(1)
    resultados = processar_arquivos(arquivos, args.data_inicio, args.data_fim)
    if not resultados:
        print("Nenhum frame encontrado no intervalo informado.")
        exit(1)
    salvar_json(args.sat_id, args.data_inicio, args.data_fim, resultados)

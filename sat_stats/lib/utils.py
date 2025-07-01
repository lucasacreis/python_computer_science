import argparse
import pandas as pd
from datetime import datetime
import os
import glob

"""
===================================================================================================
                Funções utilitárias para processamento de dados de satélites.
===================================================================================================
"""

def get_args():
    # ArgumentParser para coletar argumentos da linha de comando - Id do satélite e intervalo de datas
    parser = argparse.ArgumentParser(description="Decodifica e salva frames de satélite.")
    parser.add_argument('--sat_id', type=str, help='ID do satélite')
    parser.add_argument('--time_init', type=str, help='Data inicial (YYYY-MM-DD)')
    parser.add_argument('--time_end', type=str, help='Data final (YYYY-MM-DD)')
    args = parser.parse_args()
    return args


def get_user_inputs(args):
    if not args.sat_id:
        while True:
            try:
                args.sat_id = input("Digite o ID do satélite: ")
                if not args.sat_id.isdigit():
                    raise ValueError("O ID do satélite deve ser um número inteiro.")
                args.sat_id = int(args.sat_id)
                break
            except ValueError as e:
                print(f"Erro: {e}. Por favor, tente novamente.")
                continue
    if not args.time_init:
        while True:
            try:
                args.time_init = input("Digite a data inicial (YYYY-MM-DD): ")
                pd.to_datetime(args.time_init, format='%Y-%m-%d')
                break
            except ValueError:
                print("Formato de data inválido. Por favor, use o formato YYYY-MM-DD.")
                continue
    if not args.time_end:
        while True:
            try:
                args.time_end = input("Informe a data final (YYYY-MM-DD): ")
                pd.to_datetime(args.time_end, format='%Y-%m-%d')
                break
            except ValueError:
                print("Formato de data inválido. Por favor, use o formato YYYY-MM-DD.")
                continue
    return args


def search_files(args, tipo, extensao):
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    pasta_base = f"sat_stats/data/sat_{args.sat_id}"
    data_ini = datetime.strptime(args.time_init, "%Y-%m-%d")
    time_end = datetime.strptime(args.time_end, "%Y-%m-%d")
    arquivos = []
    meses = set()
    atual = data_ini.replace(day=1)
    while atual <= time_end:
        meses.add(atual.strftime("%Y-%m"))
        if atual.month == 12:
            atual = atual.replace(year=atual.year+1, month=1)
        else:
            atual = atual.replace(month=atual.month+1)
    # print(f"Buscando arquivos em: {pasta_base} para os meses: {', '.join(sorted(meses))}")
    for ano_mes in meses:
        pasta = os.path.join(pasta_base, ano_mes, tipo)
        print(f"Verificando pasta: {os.path.abspath(pasta)}")
        if os.path.exists(pasta):
            # print(f"Encontrando arquivos em: {pasta}")
            for arq in glob.glob(os.path.join(pasta, f"*.{extensao}")):
                # print(f"Arquivo encontrado: {arq}")
                arquivos.append(arq)
    return arquivos

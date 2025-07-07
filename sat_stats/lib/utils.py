import argparse
import pandas as pd
from datetime import datetime
import os
import glob
import json

"""
===================================================================================================
                Funções utilitárias para processamento de dados de satélites.
===================================================================================================
"""
# --- Função para coletar argumentos da linha de comando ---
def get_args():
    try:
        # ArgumentParser para coletar argumentos da linha de comando - Id do satélite e intervalo de datas
        parser = argparse.ArgumentParser(description="Decodifica e salva frames de satélite.")
        parser.add_argument('--sat_id', type=str, help='ID do satélite')
        parser.add_argument('--time_init', type=str, help='Data inicial (YYYY-MM-DD)')
        parser.add_argument('--time_end', type=str, help='Data final (YYYY-MM-DD)')
        args = parser.parse_args()
    except argparse.ArgumentError as e:
        print(f"=> Erro ao processar os argumentos: {e}")
        print("=> Certifique-se de que os argumentos estão corretos.")
        exit(1)
    else:
        return args

# --- Função para obter entradas do usuário ---
def get_user_inputs(args):
    try:
        if not args.sat_id:
            while True:
                try:
                    args.sat_id = input("=> Digite o ID do satélite: ")
                    if not args.sat_id.isdigit():
                        raise ValueError("=> O ID do satélite deve ser um número inteiro.")
                    args.sat_id = int(args.sat_id)
                    break
                except ValueError as e:
                    print(f"=> Erro: {e}. Por favor, tente novamente.")
                    continue
        if not args.time_init:
            while True:
                try:
                    args.time_init = input("=> Digite a data inicial (YYYY-MM-DD): ")
                    pd.to_datetime(args.time_init, format='%Y-%m-%d')
                    break
                except ValueError:
                    print("=> Formato de data inválido. Por favor, use o formato YYYY-MM-DD.")
                    continue
        if not args.time_end:
            while True:
                try:
                    args.time_end = input("=> Informe a data final (YYYY-MM-DD): ")
                    pd.to_datetime(args.time_end, format='%Y-%m-%d')
                    break
                except ValueError:
                    print("=> Formato de data inválido. Por favor, use o formato YYYY-MM-DD.")
                    continue
    except Exception as e:
        print(f"=> Erro inesperado: {e}. Por favor, tente novamente.")
        exit(1)
    else:
        return args

# --- Função para buscar arquivos de telemetria .xlsx ou .json ---
def search_files(args, tipo, extensao):
    try:
        # base_dir = os.path.dirname(os.path.abspath(__file__))
        pasta_base = f"data/sat_{args.sat_id}"
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
            print(f"=> Verificando pasta:\n{os.path.abspath(pasta)}")
            if os.path.exists(pasta):
                # print(f"Encontrando arquivos em: {pasta}")
                for arq in glob.glob(os.path.join(pasta, f"*.{extensao}")):
                    # print(f"Arquivo encontrado: {arq}")
                    arquivos.append(arq)
    except Exception as e:
        print(f"=> Erro ao buscar arquivos: {e}")
        exit(1)
    else:
        return arquivos

# --- Função para salvar resultados em JSON ---
def save_json(args, resultados):
    sat_id = args.sat_id
    time_init = args.time_init
    time_end = args.time_end
    print("===========================================================================================")
    print(f"=> Salvando {len(resultados)} resultados de telemetria para o satélite {sat_id} de {time_init} a {time_end}...")
    sat_folder = f"data/sat_{sat_id}"
    year_month = time_init[:7]
    save_folder = os.path.join(sat_folder, year_month, 'status')
    os.makedirs(save_folder, exist_ok=True)
    nome_arquivo = f"{time_init}_{time_end}_sat-{sat_id}_status.json"
    caminho = os.path.join(save_folder, nome_arquivo)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    print(f"=> Resultados salvos em:\n{caminho}")

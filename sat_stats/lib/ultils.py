import argparse
import pandas as pd

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

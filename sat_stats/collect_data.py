import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import getpass
import argparse
import sys

"""
===================================================================================================
                Coleta dados de telemetria de satélites EMMN INPE - Versão: 1.0
                Data: 2025-06-06 - por Lucas Reis                    
===================================================================================================
Este script coleta dados de telemetria de satélites a partir do API station da EMMN INPE.
Ele permite que o usuário especifique o ID do satélite e o intervalo de datas para a coleta.
O script autentica o usuário, faz a requisição dos dados e salva os resultados em um arquivo Excel.
===================================================================================================
Uso:
python collect_data.py --sat_id <ID_DO_SATÉLITE> --time_init <DATA_INICIAL> --time_end <DATA_FINAL>
Ou, se os argumentos não forem passados, o usuário será solicitado a inseri-los interativamente.
===================================================================================================
"""

def get_args():
    # ArgumentParser para coletar argumentos da linha de comando - Id do satélite e intervalo de datas
    parser = argparse.ArgumentParser(description="Coleta dados de telemetria de satélites.")
    parser.add_argument('--sat_id', type=int, help='ID do satélite')
    parser.add_argument('--time_init', type=str, help='Data inicial (YYYY-MM-DD)')
    parser.add_argument('--time_end', type=str, help='Data final (YYYY-MM-DD)')
    args = parser.parse_args()
    return args

def get_user_inputs():
    while True:
        try:
            sat_id = input("Digite o ID do satélite: ")
            if not sat_id.isdigit():
                raise ValueError("O ID do satélite deve ser um número inteiro.")
            sat_id = int(sat_id)
            break
        except ValueError as e:
            print(f"Erro: {e}. Por favor, tente novamente.")
            continue

    while True:
        try:
            time_init = input("Digite a data inicial (YYYY-MM-DD): ")
            time_end = input("Digite a data final (YYYY-MM-DD): ")
            pd.to_datetime(time_init, format='%Y-%m-%d')
            pd.to_datetime(time_end, format='%Y-%m-%d')
            break
        except ValueError:
            print("Formato de data inválido. Por favor, use o formato YYYY-MM-DD.")
            continue
    return sat_id, time_init, time_end

def main():
    args = get_args()
    # Se argumentos não foram passados, usa input interativo
    if args.sat_id and args.time_init and args.time_end:
        sat_id = args.sat_id
        time_init = args.time_init
        time_end = args.time_end
        # Validação das datas
        try:
            pd.to_datetime(time_init, format='%Y-%m-%d')
            pd.to_datetime(time_end, format='%Y-%m-%d')
        except ValueError:
            print("Formato de data inválido. Por favor, use o formato YYYY-MM-DD.")
            sys.exit(1)
    else:
        # Coleta de dados interativamente caso falte algum argumento
        sat_id, time_init, time_end = get_user_inputs()

    url = f"http://station/satelites/Satellite/communications/{sat_id}/?time_init={time_init}&time_end={time_end}&tipo=telemetrias&qtd_linhas=50"
    usuario = input("Digite o nome de usuário: ")
    senha = getpass.getpass("Digite a senha: ")

    # Cria uma sessão autenticada
    try:
        session = requests.Session()
        login_url = "http://station/login/"
    except requests.RequestException as e:
        print(f"Erro ao criar sessão: {e}")
        sys.exit(1)
    try:
        # Obtém o token CSRF da página de login
        resp = session.get(login_url)
        resp.raise_for_status()
        resp = session.get(login_url)
        soup = BeautifulSoup(resp.text, 'html.parser')
        csrf_token = soup.find("input", attrs={"name": "csrfmiddlewaretoken"}).get("value")
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL de login: {e}")
        sys.exit(1)
    if not csrf_token:
        print("Token CSRF não encontrado na página de login.")
        sys.exit(1)
    try:
        # Envia os dados de login
        login_data = {
            "username": usuario,
            "password": senha,
            "csrfmiddlewaretoken": csrf_token
        }
        headers = {"Referer": login_url}
        session.post(login_url, data=login_data, headers=headers)
    except requests.RequestException as e:
        print(f"Erro ao enviar dados de login: {e}")
        sys.exit(1)
    if "Login" in session.get(login_url).text:
        print("Falha no login. Verifique suas credenciais.")
        sys.exit(1)
    try:
        # Acessa a URL de telemetria
        res = session.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')
        rows = soup.select("table tr")[1:]
    except requests.RequestException as e:
        print(f"Erro ao acessar a URL de telemetria: {e}")
        sys.exit(1)
    if not rows:
        print("Nenhuma linha de dados encontrada na tabela.")
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
            raise ValueError("Nenhum dado foi extraído da tabela.")

        # Organização das pastas: sat_stats/data/sat_<id>/<ano-mês>/
        sat_folder = f"sat_stats/data/sat_{sat_id}"
        year_month = time_init[:7]
        save_folder = os.path.join(sat_folder, year_month)
        os.makedirs(save_folder, exist_ok=True)

        # Salva o DataFrame em um arquivo Excel: <daata_inicial>_to_<data_final>_sat-<id>-telemetr.xlsx
        xlsx_name = os.path.join(
            save_folder,
            f"{time_init}_to_{time_end}_sat-{sat_id}-telemetr.xlsx"
        )
        df.to_excel(xlsx_name, index=False)
        print(f"Dados salvos com sucesso em {xlsx_name}")
    except Exception as e:
        print(f"Erro ao processar os dados: {e}")
        sys.exit(1)
    try:
        # Exibe as primeiras linhas do DataFrame
        print(df.head())
    except Exception as e:
        print(f"Erro ao exibir o DataFrame: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

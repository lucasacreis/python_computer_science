import os
import requests
import pandas as pd
from bs4 import BeautifulSoup
import getpass
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

class collect_data():
    def __init__(self, get_args, get_user_inputs):
        # Checagem de argumentos
        self.get_args = get_args
        # Se argumentos não foram passados, usa input interativo
        self.get_user_inputs = get_user_inputs

        self.sat_id = self.args.sat_id
        self.time_init = self.args.time_init
        self.time_end = self.args.time_end
        self.url = f"http://station/satelites/Satellite/communications/{self.sat_id}/?time_init={self.time_init}&time_end={self.time_end}&tipo=telemetrias&qtd_linhas=50"
        self.usuario = input("Digite o nome de usuário: ")
        self.senha = getpass.getpass("Digite a senha: ")

    def run(self):
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
                "username": self.usuario,
                "password": self.senha,
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
            res = session.get(self.url)
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

            # Organização das pastas: os.path/data/sat_<id>/<ano-mês>/telemetry
            sat_folder = f"sat_stats/data/sat_{self.sat_id}/"
            year_month = self.time_init[:7]
            save_folder = os.path.join(sat_folder, year_month, 'telemetry')
            os.makedirs(save_folder, exist_ok=True)

            # Salva o DataFrame em um arquivo Excel: <daata_inicial>_to_<data_final>_sat-<id>-telemetry.xlsx
            xlsx_name = os.path.join(
                save_folder,
                f"{self.time_init}_to_{self.time_end}_sat-{self.sat_id}-telemetry.xlsx"
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
    collect_data()

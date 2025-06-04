import requests
import pandas as pd
from bs4 import BeautifulSoup

while True:
    try:
        # Solicita ao usuário o id do satélite
        sat_id = input("Digite o ID do satélite: ")
        # Verifica se o ID é um número inteiro
        if not sat_id.isdigit():
            raise ValueError("O ID do satélite deve ser um número inteiro.")
        sat_id = int(sat_id)
        break
    except ValueError as e:
        print(f"Erro: {e}. Por favor, tente novamente.")
        continue

while True:
    try:
        # Solicita ao usuário as datas de início e fim
        time_init = input("Digite a data inicial (YYYY-MM-DD): ")
        time_end = input("Digite a data final (YYYY-MM-DD): ")
        # Verifica se as datas estão no formato correto
        pd.to_datetime(time_init, format='%Y-%m-%d')
        pd.to_datetime(time_end, format='%Y-%m-%d')
        break  # Sai do loop se as datas forem válidas
    except ValueError:
        print("Formato de data inválido. Por favor, use o formato YYYY-MM-DD.")
        continue

# Configurações
url = "http://station/satelites/Satellite/communications/"
url += str(sat_id) + "/?time_init="
url += time_init + "&time_end=" + time_end + "&tipo=telemetrias&qtd_linhas=50"
usuario = input("Digite o nome de usuário: ")
senha = input("Digite a senha: ")

# Cria uma sessão autenticada
try:
    session = requests.Session()
    login_url = "http://station/login/"
except requests.RequestException as e:
    print(f"Erro ao criar sessão: {e}")
    exit(1)
# Verifica se a URL de login está acessível
try:
    resp = session.get(login_url)
    resp.raise_for_status()  # Verifica se a requisição foi bem-sucedida
    # Etapa de login (supondo um formulário CSRF básico)
    # Primeiro, pega o token CSRF
    resp = session.get(login_url)
    soup = BeautifulSoup(resp.text, 'html.parser')
    csrf_token = soup.find("input", attrs={"name": "csrfmiddlewaretoken"}).get("value")
except requests.RequestException as e:
    print(f"Erro ao acessar a URL de login: {e}")
    exit(1)

try:
    # Verifica se o token CSRF foi encontrado
    if not csrf_token:
        raise ValueError("Token CSRF não encontrado na página de login.")
except ValueError as e:
    print(f"Erro: {e}")
    exit(1)

try:
    # Envia login
    login_data = {
        "username": usuario,
        "password": senha,
        "csrfmiddlewaretoken": csrf_token
    }
    headers = {"Referer": login_url}
    session.post(login_url, data=login_data, headers=headers)
except requests.RequestException as e:
    print(f"Erro ao enviar dados de login: {e}")
    exit(1)
# Verifica se o login foi bem-sucedido
try:
    if "Login" in session.get(login_url).text:
        raise ValueError("Falha no login. Verifique suas credenciais.")
except ValueError as e:
    print(f"Erro: {e}")
    exit(1)
# Se o login foi bem-sucedido, continua com a requisição
# Acessa a página com os dados de telemetria

try:
    res = session.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

    # Extrai os dados da tabela
    rows = soup.select("table tr")[1:]  # Ignora cabeçalho
except requests.RequestException as e:
    print(f"Erro ao acessar a URL de telemetria: {e}")
    exit(1)

try:
    if not rows:
        raise ValueError("Nenhuma linha de dados encontrada na tabela.")
except ValueError as e:
    print(f"Erro: {e}")
    exit(1)
# Processa os dados
try:
    dados = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 2:
            timestamp = cols[0].text.strip()
            telemetria = cols[1].text.strip()
            dados.append({"timestamp": timestamp, "telemetria": telemetria})

    # Salva em CSV
    df = pd.DataFrame(dados)
    if df.empty:
        raise ValueError("Nenhum dado foi extraído da tabela.")
    csv_name = f"sat_stats/data/{time_init}_to_{time_end}_sat-{sat_id}-telemetr.csv"
    df.to_csv(csv_name, index=False)

    print(f"Dados salvos com sucesso em {csv_name}")
except Exception as e:
    print(f"Erro ao processar os dados: {e}")
    exit(1)
# Exibe o DataFrame
try:
    print(df.head())
except Exception as e:
    print(f"Erro ao exibir o DataFrame: {e}")
    exit(1)

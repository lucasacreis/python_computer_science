from lib.classes import satellite_data
from lib.utils import get_args, get_user_inputs, search_files, save_json

"""
===================================================================================================
                Coleta dados de telemetria de satélites EMMN INPE - Versão: 1.0
                Data: 2025-07-04 - por Lucas Reis
===================================================================================================
Este script utiliza os métodos da biblioteca `satellite_data` para coletar e processar dados de 
telemetria de satélites.
Ele permite que o usuário especifique o ID do satélite e o intervalo de datas para a coleta.
Os dados de autenticação são solicitados ao usuário e armazenados em uma sessão.
collect_data: Coleta dados de telemetria de satélites a partir do API station da EMMN INPE.
beacon_saver: Salva dados de beacons de satélites EMMN INPE em um arquivo JSON.
graph_builder: Gera gráficos a partir dos dados de telemetria coletados.
===================================================================================================
Uso:
python sat_stats.py --sat_id <ID_DO_SATÉLITE> --time_init <DATA_INICIAL> --time_end <DATA_FINAL>
Ou, se os argumentos não forem passados, o usuário será solicitado a inseri-los interativamente.
===================================================================================================
"""

if __name__ == "__main__":
    # Definição de
    sat_stats = satellite_data(get_args=get_args, 
                               get_user_inputs=get_user_inputs, 
                               search_files=search_files, 
                               save_json=save_json)
    # Coleta dados de telemetria
    sat_stats.collect_data()
    print("===========================================================================================")

    # Salva dados de beacons
    sat_stats.beacon_saver()
    print("===========================================================================================")

    # Gera gráficos do satélite
    sat_stats.graph_builder()
    print("===========================================================================================")
    print("=> Processamento concluído com sucesso!")
    print("===========================================================================================")

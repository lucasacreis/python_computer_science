from lib.classes import satellite_data
from lib.utils import get_args, get_user_inputs, search_files, save_json


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

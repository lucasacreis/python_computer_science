# May 2025 - Computer Science - Python - Prof. Dr. Lazaro Camargo
# Pandas Dataframes - Exercices 1 to 14
# by Lucas Reis

import pandas as pd
import time

while True:
    try:
        n = int(input('Digite o número do exercício: '))
        if 1 <= n <= 14:
            print(f'Você escolheu o exercício {n}.')
            break
        else:
            raise ValueError('Número do exercício deve estar entre 1 e 14.')
    except ValueError as e:
        print(e)

match n:
    case 1:
        # Criar o dicionário medidas
        medidas = {
            'data': ['15/02/2021', '16/02/2021'],
            'temperatura': [20, 25],
            'estacao': ['JAC', 'SJC'],
            'umidade': [30, 40]
        }
        print('Criar um dicionário medidas com dados de temperatura, estação e umidade')
        print(f'Dicionário medidas: \n{medidas}')
        print()
        medidas_df = pd.DataFrame(medidas)
        print('Converter o dicionário medidas em um DataFrame')
        print(f'DataFrame medidas: \n{medidas_df}')
        print()

    case _:
        # Importando um arquivo do Excel
        vendas_df = pd.read_excel('pandas/dados/Vendas.xlsx')
        print('Importar o arquivo Vendas.xlsx')

        match n:
            case 2 | 3:
                # Exibir as primeiras linhas do DataFrame
                print('Exibir as 5 primeiras linhas do DataFrame Vendas:')
                print(vendas_df.head())
                print()
            case 4:
                # Exibir as 10 primeiras linhas do DataFrame
                print('Exibir as 10 primeiras linhas do DataFrame Vendas:')
                print(vendas_df.head(10))
                print()
            case 5:
                # Exibir tamanho do DataFrame
                print(f'Exibir tamanho do DataFrame: {vendas_df.shape}')
                print()
            case 6:
                # Exibir Descrição do DataFrame
                print('Exibir Descrição do DataFrame Vendas:')
                print(vendas_df.describe())
                print()
            case 7:
                # Exibir colunas 'Produto' e 'ID Loja'
                print('Exibir colunas "Produto" e "ID Loja":')
                print(vendas_df[['Produto', 'ID Loja']])
                print()
            case 8:
                # Selecionar uma linha específica
                print('Selecionar as linhas de 1 a 5 do DataFrame Vendas:')
                print(vendas_df.loc[1:5])
                print()
            case 9:
                # Selecionar linhas com base em uma condição
                print('Selecionar linhas onde o valor da coluna "ID Loja" é igual a "Norte Shopping":')
                print(vendas_df[vendas_df['ID Loja'] == 'Norte Shopping'])
                print()
            case 10 | 11 | 12 | 13 | 14:
                # Adicionar uma nova coluna 'Comissão'
                print('Adicionar uma nova coluna "Comissão" com valor 0.05:')
                vendas_df['Comissão'] = 0.05 * vendas_df['Valor Final']
                print(vendas_df.columns)
                print()

                # Adicionar uma nova coluna 'Imposto'
                print('Adicionar uma nova coluna "Imposto" com valor 0:')
                vendas_df.loc[:, 'Imposto'] = 0
                print(vendas_df)
                print()
                
                # Importar arquivo Excel e adicinar novos dados ao DataFrame
                print('Importar o arquivo "Vendas - Dez.xmlx" e adicionar novos dados ao DataFrame Vendas:')
                vendas_dez_df = pd.read_excel('pandas/dados/Vendas - Dez.xlsx')
                vendas_df = pd.concat([vendas_df, vendas_dez_df], ignore_index=True)
                print(vendas_df)
                print()
            
                # Excluir linha 0
                print('Excluir a linha 0 do DataFrame Vendas:')
                vendas_df = vendas_df.drop(0)
                print(vendas_df)
                print()

                # Tratamento de dados NaN
                print('Tratar dados NaN no DataFrame Vendas:')
                # Deletar linhas com NaN
                vendas_dropna_df = vendas_df.dropna()
                print('Linhas com NaN removidas:')
                print(vendas_dropna_df)
                time.sleep(3)
                # Preencher NaN com 0
                vendas_df['Imposto'] = vendas_df['Imposto'].fillna(0)
                print('Linhas com NaN preenchidas com 0:')
                print(vendas_df)
                time.sleep(3)
                # Preencher NaN com a média da coluna
                vendas_df['Comissão'] = vendas_df['Comissão'].fillna(vendas_df['Comissão'].mean())
                print('Linhas com NaN preenchidas com a média da coluna:')
                print(vendas_df)

print('Fim do programa.')

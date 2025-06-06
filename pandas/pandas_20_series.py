# May 2025 - Computer Science - Python - Prof. Dr. Lazaro Camargo
# Pandas Dataframes - Exercices 1 to 14
# by Lucas Reis

import pandas as pd
import time


def series(n):
    notas = pd.Series([2, 7, 5, 10, 6])
    print('Criar uma Series com notas de 5 alunos')
    print(f'Notas: \n{notas}')
    print()
    time.sleep(2)

    notas.index = ['Aluno 1', 'Aluno 2', 'Aluno 3', 'Aluno 4', 'Aluno 5']
    print('Alterar os índices para Aluno 1, Aluno 2, Aluno 3, Aluno 4, Aluno 5')
    print(f'Notas com novos índices: \n{notas}')
    print()
    time.sleep(2)

    print('Acessar a nota do Aluno 3')
    print(f'Nota do Aluno 3: {notas["Aluno 3"]}')
    print()
    time.sleep(2)

    print('Média das notas')
    print(f'Média: {notas.mean()}')
    print()
    time.sleep(2)

    print(f'Notas acima da média: \n{notas[notas > notas.mean()]}')
    print()
    time.sleep(2)

    print(f'Notas abaixo da média: \n{notas[notas < notas.mean()]}')
    print()


def dataframe(n):

    df = pd.DataFrame({'Aluno' : ["Joao", "Maria", "Julia","Pedro", "Ana"],
                       'Faltas': [3,4, 2, 1, 4],
                       'Prova': [2, 7, 5, 10, 6],
                       'Seminario': [8.5, 7.5, 9.0, 7.5, 8.0]})
    match n:
        case 0:
            print('Criar um DataFrame com notas de 5 alunos')
            print(f'DataFrame: \n{df}')
            print()

            # Tipos de dados
            print('Tipos de dados de cada coluna')
            print(f'Tipos de dados: \n{df.dtypes}')
            print()
            
        case 1:
            # Índice de colunas
            print('Acessar o índice das colunas')
            print(f'Índice das colunas: {df.columns}')
            print()
            
        case 2:
            # Acessar uma coluna
            print('Acessar a coluna "Prova"')
            print(f'Coluna Prova: \n{df["Prova"]}')
            print()
            
        case 3:
            # Criar dataframe com valores organizados
            print('Criar um DataFrame com valores organizados por maior nota de Seminário')
            df_organizado = df.sort_values(by='Seminario', ascending=False)
            print(f'DataFrame organizado: \n{df_organizado}')
            print()
            
        case 4:
            # Exibir apenas alunos com notas acima de 8 no seminário
            print('Exibir apenas alunos com notas acima de 8 no seminário')
            df_acima_8 = df[df['Seminario'] > 8]
            print(f'Alunos com notas acima de 8: \n{df_acima_8}')
            print()
            
        case 5:
            # Exibir apenas alunos com mais de 3 faltas e nota de prova menor que 5
            print('Exibir apenas alunos com mais de 3 faltas e nota de prova menor que 5')
            df_faltas_prova = df[(df['Faltas'] >= 3) & (df['Prova'] <= 5)]
            print(f'Alunos com mais de 3 faltas e nota de prova menor que 5: \n{df_faltas_prova}')
            print()
            
        case 6:
            # Ler arquivo CSV
            print('Ler arquivo CSV e exibir os dados')
            df_csv = pd.read_csv('pandas/dados/dados.csv')
            print(f'Dados do arquivo CSV: \n{df_csv}')
            print()
            

def main():
    while True:
        try:
            tipo = input('Digite 1 para Series ou 2 para DataFrame: ')
            if tipo == '1':
                print('Você escolheu Series.')
                break
            elif tipo == '2':
                print('Você escolheu DataFrame.')
                break
            else:
                raise ValueError('Opção inválida. Digite 1 ou 2.')
        except ValueError as e:
            print(e)

    while True:
        try:
            n = int(input('Digite o número do exercício: '))
            if tipo == '1' and 0 <= n <= 6:
                print(f'Você escolheu o exercício {n}.')
                series(n)
                break
            elif tipo == '2' and 0 <= n <= 6:
                print(f'Você escolheu o exercício {n}.')
                dataframe(n)
                break
            else:
                raise ValueError('Número do exercício inválido.')
        except ValueError as e:
            print(e)


main()
print('Fim do programa.')

# May 2025 - Computer Science - Python - Prof. Dr. Lazaro Camargo
# Numpy Functions - Exercices 1 to 18
# by Lucas Reis

import numpy as np

while True:
    try:
        n = int(input('Digite o número do exercício: '))
        if 1 <= n <= 18:
            print(f'Você escolheu o exercício {n}.')
            break
        else:
            raise ValueError('Número do exercício deve estar entre 1 e 18.')
    except ValueError as e:
        print(e)

match n:
    case 1 | 2 | 3:
        # Acesso a arquivos
        # Matriz identidade 2x2
        i2 = np.eye(2)
        # Salvar arquivo
        np.savetxt('numpy/data/identidade2x2.txt', i2)
        # Carregar arquivo
        z = np.loadtxt('numpy/data/identidade2x2.txt')
        # Exibir matriz identidade 2x2
        print(f'Matriz identidade 2x2:\n{i2}')
        print(f'Matriz identidade 2x2 carregada do arquivo:\n{z}')

    case 4:
        # Acesso a arquivos
        # Matriz identidade 5x5
        i5 = np.eye(5)
        # Salvar arquivo
        np.savetxt('numpy/data/identidade5x5.txt', i5, fmt='%.2f')
        # Carregar arquivo
        z = np.loadtxt('numpy/data/identidade5x5.txt')
        # Exibir matriz identidade 5x5
        print(f'Matriz identidade 5x5:\n{i5}')
        print(f'Matriz identidade 5x5 carregada do arquivo:\n{z}')

    case 5 | 6 | 7:
        # Abrir  arquivo .csv
        c, v = np.loadtxt('numpy/data/data.csv', delimiter=',', usecols=(6, 7), unpack=True)
        
        if 5 <= n <= 6:
            print(f'Coluna 6: {c} - tamanho: {c.size}')
            print(f'Coluna 7: {v} - tamanho: {v.size}')

        if n ==  7:
            # Calcular a média ponderada do preço de fechamento "c" e pelo volume negociado "v"
            media_ponderada = np.average(c, weights=v)
            print(f'Média ponderada do preço de fechamento: {media_ponderada:.2f}')

    case 10:
        # Calcular a média e a média ponderada no tempo do volume
        h, l = np.loadtxt('numpy/data/data.csv', delimiter=',', usecols=(4, 5), unpack=True)
        print(f'Máximo: {np.max(h):.2f}')
        print(f'Mínimo: {np.min(l):.2f}')
    case _:
        print('Exercício não implementado ou fora do intervalo especificado.')

print('Fim do programa.')

import numpy as np

while True:
    try:
        n = int(input('Digite o número do exercício: '))
        if 1 <= n <= 43:
            print(f'Você escolheu o exercício {n}.')
            break
        else:
            raise ValueError('Número do exercício deve estar entre 1 e 43.')
    except ValueError as e:
        print(e)

match n:
    case 1:
        # 1 Criar array
        a = np.arange(5)
        dt = a.dtype
        s = a.shape
        t = type(a)

        print('Criar um array com np.arange(5)')
        print(f'Array a: {a}')
        print(f'Tipo de dado: {dt}')
        print(f'Formato do array: {s}')
        print(f'Tipo do array: {t}')
        print()
        pass
    case 2:
        # 2 Criar array de 2 dimensões
        m = np.array([np.arange(10), np.arange(10)])
        print('Criar um array de 2 x 10')
        print(f'Array m: \n{m}')
        print(f'Formato do array: {m.shape}')
        print()
        pass
    case 3:
        # 3 Criar um array de 2 x 4 com tipo float
        a = np.array([1, 2, 3, 4], float)
        print('Criar um array de 2 x 4 com tipo float')
        print(f'Array a: {a}')
        print(f'Tipo do array: {type(a)}')
        print()
        pass
    case 4:
        # 4 Selecionando elementos de uma matriz
        m = np.array([[1, 2], [3, 4]])
        print('Selecionando elementos de uma matriz')
        print(f'Matriz m: \n{m}')
        print(f'Elemento m[0, 0]: {m[0, 0]}')
        print(f'Elemento m[0, 1]: {m[0, 1]}')
        print(f'Elemento m[1, 0]: {m[1, 0]}')
        print(f'Elemento m[1, 1]: {m[1, 1]}')
        print()
        pass
    case 5:
        # 5 Criar uma matriz 3 x 3 com quaisquer valores e selecionar elementos 3x2 e 3x3
        m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9.0]])
        print('Criar uma matriz 3 x 3 e selecionar elementos 3x2 e 3x3')
        print(f'Matriz m: \n{m}')
        print(f'Elemento m[2, 1]: {m[2, 1]}')  # 3x2
        print(f'Elemento m[2, 2]: {m[2, 2]}')  # 3x3
        print()
        pass
    case 6:
        # 6 Comandos para uso de funções de conversão de tipos
        print('Comandos para uso de funções de conversão de tipos')
        print(f'np.float64(42): {np.float64(42)}')
        print(f'np.int8(42.0): {np.int8(42.0)}')
        print(f'np.bool_(42): {np.bool_(42)}')
        print(f'np.bool_(42.0): {np.bool_(42.0)}')
        print(f'np.float64(True): {np.float64(True)}')
        print(f'np.bool_(0.0): {np.bool_(0.0)}')
        print()
        pass
    case 7:
        # 7 Criar um vetor com os elementos [33, 78, 43, 32, 87], utilizando o tipo int64 e calcular quantos bytes tem este vetor
        a = np.array([33, 78, 43, 32, 87], dtype=np.int64)
        print('Criar um vetor com elementos específicos e calcular bytes')
        print(f'Vetor a: {a}')
        print(f'Quantidade de bytes do vetor: {a.nbytes} bytes')
        print(f'Quantidade de bytes por elemento: {a.itemsize} bytes')
        print(f'Quantidade de elementos no vetor: {a.size}')
        print(f'Quantidade de dimensões do vetor: {a.ndim}')
        print(f'Formato do vetor: {a.shape}')
        print()
        pass
    case 8:
        # 8 Formatação de arrays
        a = np.arange(24)
        print('Formatação de arrays')
        print(f'Array a: {a}')
        b = a.reshape(2, 3, 4)
        print(f'Array b (reshape): \n{b}')
        print(f'Formato do array b: {b.shape}')
        print()
        pass
    case 9:
        # 9 Selecionar as células [0,0,0] e [1,2,2] e elementos do array b
        a = np.arange(24)
        b = a.reshape(2, 3, 4)
        print('Selecionar células específicas do array b')
        print(f'Array b: \n{b}')
        print(f'Elemento b[0, 0, 0]: {b[0, 0, 0]}')
        print(f'Elemento b[1, 2, 2]: {b[1, 2, 2]}')
        print(f'Elemento b[0, 1, 3]: {b[1, 0, 3]}')  # Elemento 15
        print(f'Elemento b[1, 2, 0]: {b[0, 1, 2]}')  # Elemento 6
        print()
        pass
    case 10:
        # 10 Fatiar células da matriz b
        a = np.arange(24)
        b = a.reshape(2, 3, 4)
        print('Fatiar células da matriz b')
        print(f'Array b: \n{b}')
        print(f'Fatia b[:, 0, 0]: \n{b[:, 0, 0]}')  # Fatiar o primeiro elemento de todos os blocos
        print(f'Fatia b[0]: \n{b[0]}')              # Fatiar o primeiro bloco
        print(f'Fatia b[0, ...]: \n{b[0, ...]}')    # Fatiar todas as linhas e colunas do segundo bloco
        print()
        pass
    case 11:
        # 11 Utilizando intervalos para fatiar
        a = np.arange(24)
        b = a.reshape(2, 3, 4)
        print('Utilizando intervalos para fatiar')
        print(f'Array b: \n{b}')
        print(f'Fatia b[0, 1, :]: {b[0, 1, :]}')  # Fatiar a segunda linha do primeiro bloco
        print(f'Fatia b[1, :, 2]: {b[1, :, 2]}')  # Fatiar a terceira coluna do segundo bloco
        print(f'Fatia b[:, 1, 2]: {b[:, 1, 2]}')  # Fatiar a terceira coluna de todos os blocos
        print(f'Fatia b[0, 1:3, 2:4]: \n{b[0, 1:3, 2:4]}')  # Fatiar linhas e colunas específicas
        print()
    case _:
        print('Exercício não implementado ou inválido.')
        pass

# Finalização do script
print('Fim do script. Obrigado por utilizar o programa!')

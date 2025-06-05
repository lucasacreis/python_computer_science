# May 2025 - Computer Science - Python - Prof. Dr. Lazaro Camargo
# Numpy Arrays - Exercices 1 to 69
# by Lucas Reis

import numpy as np

while True:
    try:
        n = int(input('Digite o número do exercício: '))
        if 1 <= n <= 69:
            print(f'Você escolheu o exercício {n}.')
            break
        else:
            raise ValueError('Número do exercício deve estar entre 1 e 69.')
    except ValueError as e:
        print(e)

match n:
    case 1:
        # Operações
        a = np.array([1, 2, 3], float)
        b = np.array([5, 2, 6], float)
        print('Operações com arrays')
        print(f'Array a: {a}')
        print(f'Array b: {b}')
        print(f'Soma: {a + b}')
        print(f'Subtração: {a - b}')
        print(f'Multiplicação: {a * b}')
        print(f'Divisão a/b: {a / b}')
        print(f'Divisão b/a: {b / a}')
        print(f'Resto da divisão a/b {a % b}')
        print(f'Resto da divisão b/a {b % a}')
        print(f'Potência a^b: {a ** b}')
        print(f'Potência b^a: {b ** a}')
    case 2:
        # Operações
        a = np.array([12, 33, 45, 9, 10])
        b = np.array([50, 20, 30, 40, 60])
        print('Operações com arrays')
        print(f'Array a: {a}')
        print(f'Array b: {b}')
        print(f'Soma: {a + b}')
        print(f'Subtração: {a - b}')
        print(f'Multiplicação: {a * b}')
        print(f'Divisão a/b: {a / b}')
        print(f'Divisão b/a: {b / a}')
        print(f'Resto da divisão a/b {a % b}')
        print(f'Resto da divisão b/a {b % a}')
        print(f'Potência a^b: {a ** b}')
        print(f'Potência b^a: {b ** a}')
    case 3:
        # Operações com arrays 2D
        a = np.array([[1, 2], [3, 4]], float)
        b = np.array([[5, 6], [7, 8]], float)
        print('Operações com arrays 2D')
        print(f'Array a: \n{a}')
        print(f'Array b: \n{b}')
        print(f'Soma: \n{a + b}')
        print(f'Subtração: \n{a - b}')
        print(f'Multiplicação: \n{a * b}')
        print(f'Divisão a/b: \n{a / b}')
        print(f'Divisão b/a: \n{b / a}')
        print(f'Resto da divisão a/b: \n{a % b}')
        print(f'Resto da divisão b/a: \n{b % a}')
        print(f'Potência a^b: \n{a ** b}')
        print(f'Potência b^a: \n{b ** a}')
    case 4:
        # Operações com arrays 2D
        a = np.array([[4, 7], [2, 6]])
        b = np.array([[3, 3.5], [3.2, 3.6]])
        print('Operações com arrays 2D')
        print(f'Array a: \n{a}')
        print(f'Array b: \n{b}')
        print(f'Soma: \n{a + b}')
        print(f'Subtração: \n{a - b}')
        print(f'Multiplicação: \n{a * b}')
        print(f'Divisão a/b: \n{a / b}')
        print(f'Divisão b/a: \n{b / a}')
    case 5:
        print('Operações com arrays de diferentes dimensões')
        a = np.array([1, 2, 3])
        b = np.array([4, 5])
        try:
            print(f'Soma: {a + b}')
        except ValueError as e:
            print(f'Erro ao somar arrays de diferentes dimensões: {e}')
    # # # #

    case 13:
        # Iteração com Arrays
        a = np.array([1, 2, 3, 4, 5])
        print('Iteração com Arrays')
        print('Elementos do array:')
        for i in a:
            print(i)
    case 14:
        # Iteração com Arrays 2D
        a = np.array([[1, 2], [3, 4], [5, 6]])
        print('Iteração com Arrays 2D')
        print('Elementos do array:')
        for i in a:
            print(i)
    case 15:
        # Multiplicação de elementos do array 2D
        a = np.array([[1, 2], [3, 4], [5, 6]])
        print('Multipla atribuição com Arrays 2D')
        print('Multiplicação dos elementos por linha:')
        for (x,y) in a:
            print(x*y)
    case 21:
        # Média
        a = np.array([[0, 2], [3, -1], [3, 5]], float)
        print('Cálculo da média de um array 2D')
        print(f'Array a: \n{a}')
        print(f'Média: {np.mean(a)}')
        print(f'Média por coluna: {np.mean(a, axis=0)}')
        print(f'Média por linha: {np.mean(a, axis=1)}')
    case 22:
        # Ordenar elementos do array
        a = np.array([6, 2, 5, -1, 0], float)
        print('Ordenação de elementos do array')
        print(f'Array original: {a}')
        print(f'Array ordenado: {np.sort(a)}')
    case 23:
        # Grampear valores dos elementos do array
        a = np.array([6, 2, 5, -1, 0], float)
        print('Grampear valores dos elementos do array')
        print(f'Array original: {a}')
        print(f'Array grampeado: {a.clip(0, 5)}')
    case 24:
        # Limpeza de dados repetidos do array
        a = np.array([1, 1, 4, 5, 5, 5, 7], float)
        print('Limpeza de dados repetidos do array')
        print(f'Array original: {a}')
        print(f'Array sem duplicatas: {np.unique(a)}')
    case 25:
        # Extrair a diagonal de uma matriz
        a = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]], float)
        print('Extração da diagonal de uma matriz')
        print(f'Matriz a: \n{a}')
        print(f'Diagonal: {np.diag(a)}')
    case 26:
        # Operações de comparações booleanas
        a = np.array([1, 3, 0], float)
        b = np.array([0, 3, 3], float)
        print('Operações de comparações booleanas')
        print(f'Array a: {a}')
        print(f'Array b: {b}')
        print(f'Igualdade: {a == b}')
        print(f'Menor igual: {a <= b}')
    case _:
        print('Exercício não implementado ou fora do intervalo especificado.')

print('Fim do programa.')
# Note: The code above is a partial implementation of the exercises.
# You can continue adding cases for exercises 27 to 69 as needed.

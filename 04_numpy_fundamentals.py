import numpy as np

#  1 Criar array
a = np.arange(5)
dt = a.dtype
s = a.shape
t = type(a)

print('Exercício 1: Criar um array com np.arange(5)')
print(f'Array a: {a}')
print(f'Tipo de dado: {dt}')
print(f'Formato do array: {s}')
print(f'Tipo do array: {t}')
print()

# 2 Criar array de 2 dimensões
m = np.array([np.arange(10), np.arange(10)])

print('\nExercício 2: Criar um array de 2 x 10')
print(f'Array m: \n{m}')
print(f'Formato do array: {m.shape}')
print()

# 3 Criar um array de 2 x 4 com tipo float
a = np.array([1, 2, 3, 4], float)
print('\nExercício 3: Criar um array de 2 x 4 com tipo float')
print(f'Array a: {a}')
print(f'Tipo do array: {type(a)}')
print()

# 4 Selecionando elementos de uma matriz

m = np.array([[1,2], [3,4]])
print('\nExercício 4: Selecionando elementos de uma matriz')
print(f'Matriz m: \n{m}')
print(f'Elemento m[0, 0]: {m[0, 0]}')
print(f'Elemento m[0, 1]: {m[0, 1]}')
print(f'Elemento m[1, 0]: {m[1, 0]}')
print(f'Elemento m[1, 1]: {m[1, 1]}')
print()

# 5 Criar uma matriz 3 x 3 com quaisquer valores e selecionar elementos 3x2 e 3x3

# Ao usar um elemento float, a matriz inteira será do tipo float
m = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9.0]])
print('\nExercício 5: Criar uma matriz 3 x 3 e selecionar elementos 3x2 e 3x3')
print(f'Matriz m: \n{m}')
print(f'Elemento m[2, 1]: {m[2, 1]}')  # 3x2
print(f'Elemento m[2, 2]: {m[2, 2]}')  # 3x3
print()

# 6 Comandos para uso de funções de conversão de tipos
print('Exercício 6: Comandos para uso de funções de conversão de tipos')
print(f'np.float64(42): {np.float64(42)}')
print(f'np.int8(42.0): {np.int8(42.0)}')
print(f'np.bool_(42): {np.bool_(42)}')
print(f'np.bool_(42.0): {np.bool_(42.0)}')
print(f'np.float64(True): {np.float64(True)}')
print(f'np.bool_(0.0): {np.bool_(0.0)}')
print()

# 7 Criar  um vetor com os elementos [33, 78, 43, 32, 87], utilizando o tipo int64 e
# calcule quantos bytes tem este vetor
a = np.array([33, 78, 43, 32, 87], dtype=np.int64)
print('Exercício 7: Criar um vetor com elementos específicos e calcular bytes')
print(f'Vetor a: {a}')
print(f'Quantidade de bytes do vetor: {a.nbytes} bytes')
print(f'Quantidade de bytes por elemento: {a.itemsize} bytes')
print(f'Quantidade de elementos no vetor: {a.size}')
print(f'Quantidade de dimensões do vetor: {a.ndim}')
print(f'Formato do vetor: {a.shape}')
print()

# 8 Formatação de arrays
a = np.arange(24)
print('Exercício 8: Formatação de arrays')
print(f'Array a: {a}')
b = a.reshape(2, 3, 4)
print(f'Array b (reshape): \n{b}')
print(f'Formato do array b: {b.shape}')
print()

# 9 Selecionar as celulas [0, 0, 0] e [1, 2, 2] e elementos 15 e 6 do array b
print('Exercício 9: Selecionar células específicas do array b')
print(f'Array b: \n{b}')
print(f'Elemento b[0, 0, 0]: {b[0, 0, 0]}')
print(f'Elemento b[1, 2, 2]: {b[1, 2, 2]}')
print(f'Elemento b[0, 1, 3]: {b[1, 0, 3]}')  # Elemento 15
print(f'Elemento b[1, 2, 0]: {b[0, 1, 2]}')  # Elemento 6
print()

# 10 Fatiar celulas da matriz b
print('Exercício 10: Fatiar células da matriz b')
print(f'Array b: \n{b}')
print(f'Fatia b[:, 0, 0]: \n{b[:, 0, 0]}')  # Fatiar a primeiro elementos de todos os blocos
print(f'Fatia b[0]: \n{b[0]}')              # Fatiar o primeiro bloco
print(f'Fatia b[0, ...]: \n{b[0, ...]}')    # Fatiar todas as linhas e colunas dosegundo bloco
print()

# 11 Utilizando intervalos para fatiar
print('Exercício 11: Utilizando intervalos para fatiar')
print(f'Array b: \n{b}')

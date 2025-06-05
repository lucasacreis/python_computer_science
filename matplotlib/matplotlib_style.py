import numpy as np
import matplotlib.pyplot as plt

while True:
    try:
        n = int(input('Digite o número do exercício: '))
        if 0 <= n <= 17:
            print(f'Você escolheu o exercício {n}.')
            break
        else:
            raise ValueError('Número do exercício deve estar entre 0 e 17.')
    except ValueError as e:
        print(e)

match n:
    case 1:
        # 1 Plotar uma linha simples
        y = np.arange(1, 3)
        plt.plot(y, 'y')
        plt.plot(y+1, 'm')
        plt.plot(y+2, 'c')

    case 3:
        # 3 Plotar uma linha simples com marcadores
        y = np.arange(1, 3)
        plt.plot(y, '--', y+1, '-.', y+2, ':')

plt.show()

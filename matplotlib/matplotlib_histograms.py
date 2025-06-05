import numpy as np
import matplotlib.pyplot as plt

while True:
    try:
        n = int(input('Digite o número do exercício: '))
        if 0 <= n <= 7:
            print(f'Você escolheu o exercício {n}.')
            break
        else:
            raise ValueError('Número do exercício deve estar entre 0 e 7.')
    except ValueError as e:
        print(e)

y = np.random.randn(1000)

match n:
    case 1:
        plt.hist(y, edgecolor='black')

    case 2:
        plt.hist(y, bins=25, edgecolor='black')

plt.title('Histograma de 1000 valores aleatórios')
plt.show()

import numpy as np
import matplotlib.pyplot as plt

# 1 Criar array
x = np.linspace(-np.pi, np.pi, 256)

c = np.cos(x)
s = np.sin(x)

print('Exercício 1: Criar um array com np.linspace(-np.pi, np.pi, 256)')
plt.plot(x, c, label='cos(x)')
plt.plot(x, s, label='sin(x)')
plt.title('Gráfico de cos(x) e sin(x)')
plt.xlabel('x')
plt.ylabel('y')
plt.legend()
plt.grid()
plt.show()

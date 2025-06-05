import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as animation

# Criando uma figura e eixos
fig, ax = plt.subplots(figsize=(7, 4))
# Generando os valores de x
x = np.arange(0, 2*np.pi, 0.01)
# Plotando a curva do seno, inicial
line, = ax.plot(x, np.sin(x))
ax.legend([r'$\sin(x)$'])

# Funcao para atualizar o grafico para cada quadro da animacao
def update(frame):
    line.set_ydata(np.sin(x + frame / 10))
    # ax.set_xlim(left=0, right=frame)
    return line

# criando o objeto FuncAnimation
ani = animation.FuncAnimation(fig=fig, func=update, frames=60, interval=100)
# Salvar a animação como um arquivo GIF
ani.save('matplotlib/figures/animation.gif', writer='imagemagick')
# Exibir a animação
plt.show()

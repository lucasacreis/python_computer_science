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
    case 0:
        # 0 Plotar funções seno e cosseno
        x = np.linspace(-np.pi, np.pi, 256)

        c = np.cos(x)
        s = np.sin(x)

        print('Criar um array com np.linspace(-np.pi, np.pi, 256)')
        plt.plot(x, c, label='cos(x)')
        plt.plot(x, s, label='sin(x)')
        plt.title('Gráfico de cos(x) e sin(x)')

    case 1:
        plt.plot([1, 3, 2, 4])
        plt.title('Exercicio 1')

    case 2:
        x = range(6)
        plt.plot(x, [xi**2 for xi in x])
        plt.title('Exercicio 2')

    case 3:
        x = np.arange(0.0, 6.0, 0.01)
        plt.plot(x, [x**2 for x in x])
        plt.title('Exercicio 3')

    case 4:
        x = range(1, 5)
        plt.plot(x, [xi*1.5 for xi in x])
        plt.plot(x, [xi*3.0 for xi in x])
        plt.plot(x, [xi/3.0 for xi in x])
        plt.title('Exercicio 4')

    case 5:
        x = range(1, 5)
        plt.plot(x, [xi*1.5 for xi in x],
                 x, [xi*3.0 for xi in x],
                 x, [xi/3.0 for xi in x])
        plt.title('Exercicio 5')
    
    case 6:
        x = np.arange(1,5)
        plt.plot(x, x*1.5, x, x*3.0, x, x/3.0)
        plt.title('Exercicio 6')
    
    case 7:
        x = np.arange(1,5)
        plt.plot(x, x*1.5, x, x*3.0, x, x/3.0)
        plt.title('Exercicio 7')
        plt.grid(True)
    
    case 8:
        x = np.arange(1,5)
        plt.plot(x, x*1.5, x, x*3.0, x, x/3.0)
        plt.title('Exercicio 8')
        plt.axis([0, 5, -1, 13])
        plt.grid(True)
    
    case 9:
        x = np.arange(1,5)
        plt.plot(x, x*1.5, x, x*3.0, x, x/3.0)
        plt.title('Exercicio 8')
        plt.axis([0, 5, -1, 13])
        plt.grid(True)
        plt.xlim(1, 4)
        plt.ylim(0, 12)

    case 10:
        plt.plot([1, 3, 2, 4], label='Linha 1')
        plt.title('Exercicio 10')
        plt.xlabel('Eixo X')
        plt.ylabel('Eixo Y')
        plt.legend(loc='upper left')

    case 11 | 12 | 13:
        # Exemplo completo
        x = np.arange(1, 5)
        plt.plot(x, x*1.5, label='Normal')
        plt.plot(x, x*3.0, label='Rápido')
        plt.plot(x, x/3.0, label='Devagar')
        plt.grid(True)
        plt.title('Exemplo Completo (11, 12, 13)')
        plt.xlabel('amostras')
        plt.ylabel('valores medidos')
        plt.legend(loc='upper left')
    
    case 14:
        # Salvar gráfico em arquivo
        plt.plot([1, 3, 2, 4], label='Linha 1')
        plt.title('Exercicio 14')
        plt.savefig('matplotlib/figures/figure.png')

    case 15 | 16:
        # Efeito semelhante ao comando hold on do Matlab
        x = np.linspace(0, 2 * np.pi, 100)
        y1 = np.sin(x)
        y2 = np.cos(x)
        plt.plot(x, y1, label='Seno')
        plt.plot(x, y2, label='Cosseno')
        plt.title('Exercicio 15')
        plt.xlabel('Ângulo (radianos)')
        plt.ylabel('Valor')
        plt.legend()
        plt.show()

        print('Feche o gráfico para continuar...')

        plt.figure()  # Cria uma nova figura
        plt.plot(x, y1, label='Seno')
        plt.legend()
        plt.title('Exercicio 16')
        plt.xlabel('Ângulo (radianos)')
        plt.ylabel('Valor')
        plt.grid(True)
        plt.show()

        print('Feche o gráfico para continuar...')
        plt.clf()  # Limpa a figura atual
        plt.plot(x, y2, label='Cosseno')
        plt.legend()
        plt.title('Exercicio 16')
        plt.xlabel('Ângulo (radianos)')
        plt.ylabel('Valor')
        plt.grid(True)

    case _:
        print(f'Exercício {n} não implementado.')

try:
    plt.show()
except Exception as e:
    print(f'Erro ao exibir o gráfico: {e}')

# End of the code

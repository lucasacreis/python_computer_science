import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

while True:
    try:
        n = int(input('Digite o número do exercício: '))
        if 0 <= n <= 1:
            print(f'Você escolheu o exercício {n}.')
            break
        else:
            raise ValueError('Número do exercício deve estar entre 0 e 1.')
    except ValueError as e:
        print(e)

sns.set_theme(style="dark")

match n:
    case 0:
        # Simulate data from a bivariate Gaussian
        n = 10000
        mean = [0, 0]
        cov = [(2, .4), (.4, .2)]
        rng = np.random.RandomState(0)
        x, y = rng.multivariate_normal(mean, cov, n).T

        # Draw a combo histogram and scatterplot with density contours
        f, ax = plt.subplots(figsize=(6, 6))
        sns.scatterplot(x=x, y=y, s=5, color=".15")
        sns.histplot(x=x, y=y, bins=50, pthresh=.1, cmap="mako")
        sns.kdeplot(x=x, y=y, levels=5, color="w", linewidths=1)
    case 1:
        sns.set_context("paper")
        sns.set_style("whitegrid")
        x = np.arange(1, 10)
        y = np.log(x)
        plt.plot(x, y)

# Show the plot
plt.show()

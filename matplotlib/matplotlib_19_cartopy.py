import cartopy.crs as crs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt

# Inicializa a figura
figure = plt.figure(figsize=(8,6))
# utiliza projeção Mercator
ax = figure.add_subplot(1,1,1, projection=crs.Mercator())
# adiciona recurso no mapa
ax.stock_img()

plt.show()

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from fitter import Fitter
from scipy.stats import chi2


# Lecutura del archivo de datos
ruta_datos = "data/workstation1.csv"
data = pd.read_csv(ruta_datos, header=None).rename(columns={0: "Tiempos de proceso"})

# Se muestran los datos en un histograma
sns.set_style("white")
sns.set_context("paper", font_scale=2)
sns.displot(data=data, x="Tiempos de proceso", kind="hist", bins=10, aspect=1.5)
plt.show()

# Preparación de los datos
tiempos = data["Tiempos de proceso"].values

# Ajustar la distribución.
f = Fitter(tiempos)
f.fit()
print(f.summary())

# Obtener parametros
print(f.get_best(method="sumsquare_error"))

# Sabiendo que la distribución de los datos es una distribución triangular (50, 60, 65)
# Hacemos el test de ajuste.
# Dividimos los datos en 10 intervalos y registramos su frecuencia absoluta
a = 50
b = 65
c = 60
k = 10
d = (b - a) / k
h = dict()
for i in np.linspace(a, b, k + 1):
    h[i] = len(
        data[(data["Tiempos de proceso"] >= i) & (data["Tiempos de proceso"] < i + d)]
    )


# Se calcula la probabilidad teórica
def funcion_distribucion_triang(x, a, b, c):
    if x <= a:
        return 0
    elif a < x <= c:
        return (x - a) ** 2 / ((b - a) * (c - a))
    elif c < x < b:
        return 1 - (b - x) ** 2 / ((b - a) * (b - c))º
    elif x >= b:
        return 1


p = dict()
for i in np.linspace(a, b, k + 1):
    p[i] = funcion_distribucion_triang(i + d, a, b, c) - funcion_distribucion_triang(
        i, a, b, c
    )

# Preparar diccionario:
data2 = {k: {"h": v, "p": p[k]} for k, v in h.items()}
# Calculamos el valor del test chi-cuadrado
n = len(data)
chi2exp = sum((d["h"] - n * d["p"]) ** 2 / n * d["p"] for d in data2.values())
chi2 = chi2.ppf(0.95, k - 1)

if chi2exp > chi2:
    print("Se rechaza la hipótesis nula")
else:
    print("No hay evidencia estadística para rechazar la hipótesis nula")

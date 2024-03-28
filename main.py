import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import ajustar_distribucion


# Lecutura del archivo de datos
ruta_datos = "data/workstation1.csv"
data = pd.read_csv(ruta_datos, header=None).rename(columns={0: "Tiempos de proceso"})

ad = ajustar_distribucion(data)

# Se muestran los datos en un histograma
sns.set_style("white")
sns.set_context("paper", font_scale=2)
sns.displot(data=data, x="Tiempos de proceso", kind="hist", bins=10, aspect=1.5)
plt.show()

# Ajuste con libreria estandar:
ad.libreria_estandar()

# Sabiendo que la distribución de los datos es una distribución triangular (50, 60, 65)
# Hacemos el test de ajuste.
ad.

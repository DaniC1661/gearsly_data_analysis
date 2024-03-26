import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from fitter import Fitter


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

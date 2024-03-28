import numpy as np
from fitter import Fitter
from scipy.stats import chi2


class AjustarDistribucion:
    def __init__(self, df):
        self.data = df

    def libreria_estandar(self):
        # Preparación de los datos
        tiempos = self.data["Tiempos de proceso"].values

        # Ajustar la distribución.
        f = Fitter(tiempos)
        f.fit()
        print(f.summary())

        # Obtener parametros
        print(f.get_best(method="sumsquare_error"))

    def test_ajuste_triang(self):
        # Constantes de esta distribucion
        A = 50
        B = 65
        C = 60
        k = 10
        d = (B - A) / k

        # Dividimos los datos en 10 intervalos y registramos su frecuencia absoluta
        h = dict()
        for i in np.linspace(A, B, k + 1):
            h[i] = len(
                self.data[
                    (self.data["Tiempos de proceso"] >= i)
                    & (self.data["Tiempos de proceso"] < i + d)
                ]
            )

        # Se calcula la probabilidad teórica
        def funcion_distribucion_triang(x, A, B, C):
            if x <= A:
                return 0
            elif A < x <= C:
                return (x - A) ** 2 / ((B - A) * (C - A))
            elif C < x < B:
                return 1 - (B - x) ** 2 / ((B - A) * (B - C))
            elif x >= B:
                return 1

        p = dict()
        for i in np.linspace(A, B, k + 1):
            p[i] = funcion_distribucion_triang(
                i + d, A, B, C
            ) - funcion_distribucion_triang(i, A, B, C)

        # Preparar diccionario:
        data2 = {k: {"h": v, "p": p[k]} for k, v in h.items()}
        # Calculamos el valor del test chi-cuadrado
        n = len(self.data)
        chi2exp = sum((d["h"] - n * d["p"]) ** 2 / n * d["p"] for d in data2.values())
        chi2 = chi2.ppf(0.95, k - 1)

        if chi2exp > chi2:
            print("Se rechaza la hipótesis nula")
        else:
            print("No hay evidencia estadística para rechazar la hipótesis nula")

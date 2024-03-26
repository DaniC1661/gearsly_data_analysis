import numpy as np
import matplotlib.pyplot as plt

from scipy import stats


class DataAnalyzer:
    def __init__(self, data):
        self.data = data

    def realizar_analisis(self):
        self._test_independencia()
        self._estadisticas_descriptivas()
        self._representar_graficos()
        self._ajuste_normal()

    def _test_independencia(self):
        corr = self.data["Valor"].corr(self.data["NObs"])
        print("Coeficiente de correlación: " + str(corr))

        pares = list(zip(self.data["Valor"], self.data["Valor"][1:]))

        x = [par[0] for par in pares]
        y = [par[1] for par in pares]

        plt.figure(figsize=(8, 6))
        plt.plot(x, y, "o")  # Marcador de puntos
        plt.xlabel("X(i)")
        plt.ylabel("X(i+1)")
        plt.title("Plot de datos en pares (X(i), X(i+1))")
        plt.grid(True)
        plt.show()

    def _estadisticas_descriptivas(self):
        print(self.data["Valor"].describe())

    def _representar_graficos(self):
        plt.hist(x=self.data["Valor"], bins=20, color="#3182bd", alpha=0.5)
        plt.plot(
            self.data["Valor"],
            np.full_like(self.data["Valor"], -0.01),
            "|k",
            markeredgewidth=1,
        )
        plt.title("Distribución empírica de los datos")
        plt.xlabel("Tiempos")
        plt.ylabel("Recuento")
        plt.show()

    def _ajuste_normal(self):
        datos = self.data["Valor"]

        distribucion = stats.norm
        parametros = distribucion.fit(data=datos)
        datos_obs = np.array(self.data["Valor"])
        datos_esp = np.random.normal(
            loc=parametros[0], scale=parametros[1], size=len(datos_obs)
        )
        datos_unidos = np.vstack((datos_obs, datos_esp))
        chi2_stat, p_val, dof, expected = stats.chi2_contingency(datos_unidos)
        print("P-valor del test de la normal: " + str(p_val))

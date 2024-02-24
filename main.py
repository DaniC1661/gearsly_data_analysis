
import pandas as pd
from data_analyzer import DataAnalyzer

if __name__ == "__main__":

    # Lecutura del archivo de datos
    ruta_datos = "data/workstation1.csv"
    df = pd.read_csv(ruta_datos, header=None).rename(columns={0: "Valor"})

    df["NObs"] = range(1, len(df) + 1)
    data = df[["NObs", "Valor"]]

    # Análisis con liberias estandar
    analysis_sl = DataAnalyzer(data)
    analysis_sl.realizar_analisis()

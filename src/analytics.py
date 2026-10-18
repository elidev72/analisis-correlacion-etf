import numpy as np
import pandas as pd
from scipy import stats
from icecream import ic

def calcular_estadisticas(df: pd.DataFrame) -> dict:
    """
    Calcula las métricas estadísticas exigidas por la cátedra para el análisis 
    de regresión y correlación entre los rendimientos de VOO y AVUV:
    
    1. Coeficiente de Correlación de Pearson (r).
    2. Parámetros de la Regresión Lineal Simple (Pendiente y Ordenada al origen).
    3. Coeficiente de Determinación (R^2) y su significado porcentual.
    """
    ic("Iniciando cálculos estadísticos con scipy...")

    # Definimos las variables:
    # x = Variable independiente (ej. Rendimiento de VOO)
    # y = Variable dependiente (ej. Rendimiento de AVUV)
    x = df['ret_voo']
    y = df['ret_avuv']

    # linregress calcula automáticamente la regresión lineal y el coeficiente de Pearson
    # Retorna: pendiente (slope), intercepto (intercept), r_value (Pearson r), p_value y error estándar
    slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)

    # Coeficiente de Determinación (R^2) se obtiene elevando al cuadrado el coeficiente de Pearson
    r_squared = r_value ** 2

    # Empaquetamos todos los resultados en un diccionario estructurado
    resultados = {
        "pearson_r": r_value,
        "r_squared": r_squared,
        "r_squared_porcentaje": r_squared * 100,
        "pendiente": slope,
        "intercepto": intercept,
        "p_value": p_value,
        "ecuacion_recta": f"y = {slope:.4f}x + {intercept:.4f}"
    }

    ic("Resultados estadísticos calculados con éxito:", resultados)
    return resultados

import streamlit as st
from icecream import ic

from src.database import obtener_datos_financieros
from src.analytics import calcular_estadisticas
from src.ui import render_header_y_teoria, render_kpis, render_grafico_y_analisis, render_tabla_datos, aplicar_estilos_impresion

# Configuración de página de Streamlit
st.set_page_config(
    page_title="Análisis VOO vs AVUV | Regresión y Correlación",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def cargar_y_procesar_datos():
    ic("Cargando pipeline completo desde app.py...")
    df = obtener_datos_financieros()
    stats = calcular_estadisticas(df)
    return df, stats

if __name__ == "__main__":
    ic.disable()
    aplicar_estilos_impresion()
    
    df, stats = cargar_y_procesar_datos()
    
    render_header_y_teoria()
    render_kpis(stats)
    render_grafico_y_analisis(df, stats)
    render_tabla_datos(df)

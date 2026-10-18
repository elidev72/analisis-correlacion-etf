import pandas as pd
import streamlit as st
from src.plotting import crear_grafico_dispersion

def render_header_y_teoria():
    """Renderiza el encabezado y el marco teórico exigido por la cátedra."""
    st.title("📈 Análisis de Regresión y Correlación")
    st.markdown("##### Estudio cualitativo y cuantitativo: VOO (S&P 500) vs. AVUV (US Small Cap Value)")

    with st.expander("📚 Marco Teórico: Correlación vs. Regresión", expanded=False):
        col_t1, col_t2 = st.columns(2)
        with col_t1:
            st.markdown("### 🔗 Correlación")
            st.markdown("""
            * **Concepto:** Mide el grado de asociación o fuerza de relación lineal entre dos variables.
            * **Simetría:** Es simétrica.
            * **Causa-Efecto:** No implica causalidad.
            * **Medida:** Coeficiente de Pearson ($r$).
            """)
        with col_t2:
            st.markdown("### 📐 Regresión Lineal")
            st.markdown(r"""
            * **Concepto:** Modela la dependencia de una variable respecto de otra ($\hat{y} = \beta_0 + \beta_1 x$).
            * **Asimetría:** Distingue entre variable independiente ($X$) y dependiente ($Y$).
            * **Predicción:** Permite estimar valores de $Y$.
            """)
    st.divider()

def render_kpis(stats: dict):
    """Renderiza los indicadores clave (KPIs)."""
    st.subheader("📊 Coeficientes e Indicadores del Modelo")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Pearson (r)", f"{stats['pearson_r']:.4f}")
        st.caption("Asociación lineal positiva fuerte.")
    with col2:
        st.metric("Determinación (R²)", f"{stats['r_squared_porcentaje']:.2f}%")
        st.caption(f"El {stats['r_squared_porcentaje']:.1f}% de la varianza se explica.")
    with col3:
        st.metric("Pendiente (β₁)", f"{stats['pendiente']:.4f}")
        st.caption("Sensibilidad ante cambios en VOO.")
    with col4:
        st.metric("Intercepto (β₀)", f"{stats['intercepto']:.4f}")
        st.caption("Rendimiento base esperado.")
    st.divider()

def render_grafico_y_analisis(df, stats: dict):
    """Renderiza el gráfico de Plotly y la interpretación."""
    st.subheader("📉 Diagrama de Dispersión y Ajuste del Modelo")
    col_grafico, col_info = st.columns([3, 1.2])

    with col_grafico:
        fig = crear_grafico_dispersion(df, stats)
        st.plotly_chart(fig, width='stretch')

    with col_info:
        st.markdown("### 📌 Ecuación de la Recta")
        st.code(stats['ecuacion_recta'], language="text")
        st.markdown("### 💡 Interpretación")
        st.markdown(f"""
        1. **Pearson ($r$):** `{stats['pearson_r']:.4f}` (Correlación fuerte).
        2. **$R^2$:** Explica el `{stats['r_squared_porcentaje']:.1f}%` de los movimientos.
        3. **Pendiente ($\beta_1$):** `{stats['pendiente']:.4f}`.
        """)
    st.divider()

def render_tabla_datos(df):
    """Renderiza la tabla de datos histórica."""
    with st.expander("🔍 Ver Tabla de Datos Históricos"):
        st.dataframe(
            df.style.format({
                "precio_voo": "${:.2f}",
                "precio_avuv": "${:.2f}",
                "ret_voo": lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A (Base)",
                "ret_avuv": lambda x: f"{x:.2f}%" if pd.notna(x) else "N/A (Base)"
            }),
            width='stretch'
        )

def aplicar_estilos_impresion():
    """
    Inyecta CSS personalizado para optimizar la app tanto para la visualización web
    como para cuando se utilice la función de impresión (Print a PDF) para la cátedra.
    """
    st.markdown("""
        <style>
        /* Estilos generales para la vista web */
        .stApp {
            background-color: #0F172A;
            color: #F1F5F9;
        }

        /* CONFIGURACIÓN EXCLUSIVA PARA IMPRESIÓN (Print / Guardar como PDF) */
        @media print {
            /* Oculta elementos innecesarios de la interfaz de Streamlit */
            header, footer, [data-testid="stHeader"], .stActionButton {
                display: none !important;
            }
            
            /* Cambia el fondo a blanco y texto oscuro para que se lea perfecto en papel/PDF */
            .stApp {
                background-color: #FFFFFF !important;
                color: #000000 !important;
            }
            
            /* Asegura que las tarjetas y gráficos no se corten abruptamente entre páginas */
            div[data-testid="stMetric"], .stPlotlyChart, div[data-testid="stVerticalBlock"] {
                break-inside: avoid;
                page-break-inside: avoid;
            }
            
            /* Remueve sombras y ajusta bordes para impresión limpia */
            div[data-testid="stMetric"] {
                border: 1px solid #CCCCCC !important;
                background-color: #F9FAFB !important;
            }
        }
        </style>
    """,
    unsafe_allow_html=True)

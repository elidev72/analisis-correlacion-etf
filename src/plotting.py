import numpy as np
import pandas as pd
import plotly.graph_objects as go
from icecream import ic

def crear_grafico_dispersion(df: pd.DataFrame, stats: dict) -> go.Figure:
    """
    Genera un diagrama de dispersión interactivo con la línea de regresión
    lineal superpuesta utilizando Plotly.
    """
    ic("Generando diagrama de dispersión con Plotly...")

    x = df['ret_voo']
    y = df['ret_avuv']

    # 1. Crear la figura base de Plotly
    fig = go.Figure()

    # 2. Agregar los puntos del scatter plot (Rendimientos Mensuales)
    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode='markers',
            name='Rendimientos Mensuales',
            text=df['fecha'],  # Hover muestra la fecha de cada punto
            hovertemplate='<b>Fecha:</b> %{text}<br>' +
                          '<b>VOO:</b> %{x:.2f}%<br>' +
                          '<b>AVUV:</b> %{y:.2f}%<extra></extra>',
            marker=dict(
                size=9,
                color='#00D4FF',
                opacity=0.8,
                line=dict(width=1, color='#FFFFFF')
            )
        )
    )

    # 3. Generar valores para la recta de regresión
    x_line = np.linspace(x.min(), x.max(), 100)
    y_line = stats['pendiente'] * x_line + stats['intercepto']

    # 4. Agregar la recta de regresión lineal
    fig.add_trace(
        go.Scatter(
            x=x_line,
            y=y_line,
            mode='lines',
            name=f"Regresión: {stats['ecuacion_recta']}",
            line=dict(color='#FF4B4B', width=3, dash='dash')
        )
    )

    # 5. Configurar el diseño visual (Layout)
    fig.update_layout(
        title=dict(
            text="<b>Diagrama de Dispersión y Recta de Regresión</b><br><sup>Rendimiento Mensual %: VOO vs AVUV</sup>",
            x=0.05,
            y=0.95
        ),
        xaxis=dict(
            title="Rendimiento Mensual VOO (%) [Variable X]",
            zeroline=True,
            zerolinecolor='#888888',
            gridcolor='#333333'
        ),
        yaxis=dict(
            title="Rendimiento Mensual AVUV (%) [Variable Y]",
            zeroline=True,
            zerolinecolor='#888888',
            gridcolor='#333333'
        ),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor='rgba(0,0,0,0.5)'
        ),
        template="plotly_dark",
        margin=dict(l=40, r=40, t=80, b=40),
        hovermode="closest"
    )

    ic("Gráfico generado con éxito.")
    return fig

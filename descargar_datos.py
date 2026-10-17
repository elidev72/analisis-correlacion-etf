import os
import yfinance as yf
from icecream import ic

def descargar_y_congelar_datos():
    """
    Descarga datos históricos de VOO y AVUV desde Yahoo Finance,
    procesa las columnas para asegurar coherencia y congela los CSVs en /data.
    """
    # 1. Nos aseguramos de que exista el directorio data/
    os.makedirs("data", exist_ok=True)
    ic("Directorio 'data/' verificado/creado.")

    tickers = ["VOO", "AVUV"]
    ic("Iniciando descarga de datos para:", tickers)

    # 2. Descargamos 5 años de datos históricos con frecuencia mensual ('1mo')
    datos = yf.download(
        tickers, 
        period="5y", 
        interval="1mo", 
        group_by="ticker", 
        auto_adjust=True
    )

    for ticker in tickers:
        ic(f"Procesando ticker: {ticker}")
        
        # Extraemos el DataFrame específico del ticker
        df_ticker = datos[ticker].copy()
        
        # Eliminamos filas que no tengan precio de cierre (meses no cerrados)
        df_ticker = df_ticker.dropna(subset=["Close"])
        
        # Reseteamos el índice para que 'Date' pase a ser una columna normal
        df_ticker = df_ticker.reset_index()

        # Nos quedamos con Date y Cierre
        df_ticker = df_ticker[["Date", "Close"]]
        
        # Formateamos la fecha a formato ISO YYYY-MM-DD sin hora
        df_ticker["Date"] = df_ticker["Date"].dt.strftime("%Y-%m-%d")

        # 3. Guardamos en CSV dentro de data/
        ruta_csv = os.path.join("data", f"{ticker.lower()}.csv")
        df_ticker.to_csv(ruta_csv, index=False)
        
        ic(f"Archivo guardado exitosamente en: {ruta_csv}")
        ic(df_ticker.head())

    print("✅ ¡Proceso completado! Los datos han sido congelados correctamente en la carpeta 'data/'.")

if __name__ == "__main__":
    descargar_y_congelar_datos()

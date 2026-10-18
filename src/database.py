import duckdb
import pandas as pd
from icecream import ic

def obtener_datos_financieros() -> pd.DataFrame:
    """
    Se conecta a DuckDB, lee los CSV estáticos de VOO y AVUV,
    realiza el JOIN por fecha y calcula los rendimientos mensuales.
    """
    ic("Iniciando conexión con DuckDB y lectura de datos...")

    # Creamos una conexión en memoria a DuckDB
    con = duckdb.connect(database=':memory:', read_only=False)

    # Consulta SQL optimizada para leer los CSV, unirlos por fecha 
    # y ordenar cronológicamente
    query = """
    WITH voo AS (
        SELECT CAST(Date AS DATE) as fecha, Close as precio_voo
        FROM read_csv_auto('data/voo.csv')
    ),
    avuv AS (
        SELECT CAST(Date AS DATE) as fecha, Close as precio_avuv
        FROM read_csv_auto('data/avuv.csv')
    )
    SELECT 
        v.fecha,
        v.precio_voo,
        a.precio_avuv,
        -- Calculamos el rendimiento porcentual mensual ((Precio_actual - Precio_anterior) / Precio_anterior) * 100
        ((v.precio_voo - LAG(v.precio_voo) OVER (ORDER BY v.fecha)) / LAG(v.precio_voo) OVER (ORDER BY v.fecha)) * 100 as ret_voo,
        ((a.precio_avuv - LAG(a.precio_avuv) OVER (ORDER BY a.fecha)) / LAG(a.precio_avuv) OVER (ORDER BY a.fecha)) * 100 as ret_avuv
    FROM voo v
    JOIN avuv a ON v.fecha = a.fecha
    ORDER BY v.fecha ASC;
    """

    # Ejecutamos la query y transformamos el resultado directamente a un DataFrame de Pandas
    df = con.execute(query).df()
    
    # Limpiamos el primer registro que tendrá valores nulos por el uso de LAG()
    df = df.dropna().reset_index(drop=True)

    ic("Datos procesados correctamente con DuckDB:", df.head())
    
    # Cerramos la conexión a DuckDB
    con.close()
    
    return df

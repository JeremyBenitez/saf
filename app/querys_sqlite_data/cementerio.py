import time
from datetime import datetime, timedelta
import sqlite3
import pyodbc
from pathlib import Path


fecha = datetime.now()
fecha_diaria = fecha.date()

fecha_hace_1Day = fecha_diaria - timedelta(days=1)

def get_db_connection():
    """Crear conexión a la base de datos"""
    conn_str = (
        "DRIVER={SQL Server};"
        "SERVER=ELTIO-CENTRAL;"
        "DATABASE=VAD10;"
        "UID=sa;"
        "PASSWORD=;"
        "Trusted_Connection=no;"
    )
    
    return pyodbc.connect(conn_str)




base_dir  = Path().resolve()

db_path_bd1 = base_dir / "BBDDs" / "BBDD-Cementerio.db"

def get_db():
    conexion = sqlite3.connect(str(base_dir))
    return conexion







class cementerio:
  
    def ventas_cementerio(self,fi,fo):
        self.coneccion = get_db()
        self.cursor = self.coneccion.cursor()        
        self.cursor.execute("""SELECT 
                SUM(V_USD) AS total_usd,
                SUM(V_BS) AS total_bs,
                SUM(V_CSH) AS total_csh,
                SUM(V_EFEC) AS total_efec,
                n_trasacciones
            FROM (
                SELECT V_USD, V_BS, V_CSH, V_EFEC, n_trasacciones, FECHA FROM VENTAS
                
            ) AS todas_las_tablas
            WHERE FECHA BETWEEN ? AND ? """,(fi,fo))
        self.data = self.cursor.fetchall()
        return self.data


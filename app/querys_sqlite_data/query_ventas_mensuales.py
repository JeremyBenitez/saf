import pyodbc
import sqlite3
from pathlib import Path



base_dir  = Path().resolve()
db_path = base_dir / "BBDDs" / "BDTiendas.db"

def get_db():
    conexion = sqlite3.connect(str(db_path))
    return conexion



class Meses:
    def __init__(self, tienda):
        self.tienda = tienda
    
    def consulta(self,fi, fo,):
        conection = get_db()
        pointer = conection.cursor()
        pointer.execute(f"""
                        SELECT 
        SUM(V_USD) AS total_usd,
        SUM(V_BS) AS total_bs,
        SUM(V_CSH) AS total_csh,
        SUM(V_EFEC) AS total_efec,
        n_trasacciones
    FROM (
        SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA,n_trasacciones FROM {self.tienda}
        
    ) AS todas_las_tablas
    WHERE FECHA BETWEEN ? AND ?
    """,(fi, fo))
        data = pointer.fetchall()
        conection.close()
        return data



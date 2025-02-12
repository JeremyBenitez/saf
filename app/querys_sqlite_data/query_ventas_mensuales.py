import pyodbc
import sqlite3


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


"""class meses:
    def consulta_table_ventas(self, mes):
            conection = get_db_connection()
            pointer = conection.cursor()
            pointer.execute("SELECT * FROM ResumenMensualVentas WHERE Mes = ?",(mes,))
            data = pointer.fetchall()
            conection.close()
            return data
"""




class Meses:
    def __init__(self, tienda):
        self.tienda = tienda
    
    def consulta(self,fi, fo,):
        conection = sqlite3.connect('BDTiendas.db')
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

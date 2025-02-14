
import pyodbc
import sqlite3

from.conexion_sqlite import get_db

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

def consulta_table_ventas():
    conection = get_db_connection()
    pointer = conection.cursor()
    pointer.execute("SELECT * FROM ResumenMensualVentas WHERE Mes = 2")
    data = pointer.fetchall()
    conection.close()
    return data[1][3],data[1][2] #rettorno de BS y USD general

def consulta_table_Efectivo():
    conection = get_db_connection()
    pointer = conection.cursor()
    pointer.execute("SELECT * FROM ResumenMensualVentasEfectivo WHERE Mes = 2")
    data = pointer.fetchall()
    conection.close()
    return data[0][3]


def consulta_table_cashea():
    conection = get_db_connection()
    pointer = conection.cursor()
    pointer.execute("SELECT * FROM ResumenMensualVentasCSH WHERE Mes = 2")
    data = pointer.fetchall()
    conection.close()
    return data[0][3]




class index:

    def valores(self, tabla):
        self.conexion = get_db()
        pointer = self.conexion.cursor()
        pointer.execute(f"SELECT * FROM {tabla} ")
        colums = [colum[0] for colum in pointer.description]
        rows = pointer.fetchall()
        self.data = [dict(zip(colums,row))for  row in rows]
        self.conexion.close()
        return  self.data




if __name__ == "__main__":
    
    pass
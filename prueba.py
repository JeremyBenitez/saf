import pyodbc
import time
from datetime import datetime, timedelta

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


def diario_cashea(ndb,fi,dpo,dpto): #Venta diaria por tiende metodo cashea
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute(' sp_ObtenerArticulosConUnionesDinamico  @c_CodDeposito = ? , @f_FechaInicio = ?, @BaseDatos = ?, @c_Departamento = ?',ndb, fi, dpo,dpto)
        data = cursor.fetchall()
        conetion.close()
        return data

a = diario_cashea('010103','2024-01-02','VAD10_KAPITANA','HOGAR')
for i in a:
      
    print(i)

#CODIGO ARTICULO , ARTICULO, DEPARTAMENTO, PISO DE VENTA, STOCK_ACTUAL,VENTAS_30DIAS, VENTAS_60_DIAS, VENTAS_90DIAS,
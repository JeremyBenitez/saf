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


def inventario_dinamico(ndb,fi,dpo,dpto): #Venta diaria por tiende metodo cashea
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute(' sp_ObtenerArticulosConUnionesDinamico   @c_CodDeposito = ? , @f_FechaInicio = ?, @BaseDatos = ?, @c_Departamento = ?',ndb, fi, dpo,dpto)
        data = cursor.fetchall()
        conetion.close()
        return data




depositos = ['020303','030103','020203','020503','050103',
          '020703','020103','010303','020403','010103',
          '030203','040103','040203','010203','020603'
                                       ]
nombre_tiendas = ['BABILON','BARALT','CABIMAS','CABUDARE','CAGUA','CATIA','CRUZ VERDE','GUACARA',
              'GUANARE','KAPITANA','MATURIN','PROPATRIA','UPATA','VALENCIA','VALERA']

def bases_datos():
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('SELECT * FROM ServidorBaseDatos')
        data = cursor.fetchall()
        conetion.close()
        valores = []
        for bd , tienda, dpto  in zip(data, nombre_tiendas, depositos):
            valores.append((bd,tienda,dpto))
        return valores



def departamentos():
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute('SELECT * FROM MA_DEPARTAMENTOS')
    data = pointer.fetchall()
    coneccion.close()
    return data

def grupos(codigo):
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute("SELECT * FROM MA_GRUPOS WHERE c_departamento = ?",(codigo,))
    data = pointer.fetchall()
    coneccion.close()
    return data


"""
EXEC sp_ObtenerArticulosConUnionesDinamico 
    @c_CodDeposito = '010103',
    @f_FechaInicio = '2024-11-01',
    @BaseDatos = 'VAD10_KAPITANA',
    @c_Departamento = 'CP';
"""
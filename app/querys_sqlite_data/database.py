
from flask import Flask, request
import os
import pyodbc
from datetime import datetime, timedelta
import time

#Cargar variables de entorno

fecha = datetime.now()
fecha_diaria = fecha.date()

"""fecha_inicio =  datetime.strptime(fi,'%Y-%m-%d')
fecha_final =  datetime.strptime(fo,'%Y-%m-%d')"""
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

#VAlORES DE TIENDA KAPITANA


def tasa(fi,fo):
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute('ObtenerHistoricoMonedasUSD @FechaInicio = ?, @FechaFin = ?',fi,fo)
    data = pointer.fetchall()
    coneccion.close()
    return data



def general_usd(fi,fo):
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute('TotalVentasenUSDxGeneral  @FechaInicio = ?, @FechaFin = ?',fi,fo)
    data = pointer.fetchall()
    coneccion.close()
    return data [0][0]


def general_bs(fi,fo):
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute('TotalVentasenBSxGeneral   @FechaInicio = ?, @FechaFin = ?',fi,fo)
    data = pointer.fetchall()
    coneccion.close()
    return data [0][0]

def general_csh(fi,fo):
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute('TotalVentasenUSDxGeneralCSH  @FechaInicio = ?, @FechaFin = ?',fi,fo)
    data = pointer.fetchall()
    coneccion.close()
    return data [0][0]

def general_efe(fi,fo):
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute('TotalVentasenUSDxGeneralEfectivo  @FechaInicio = ?, @FechaFin = ?',fi,fo)
    data = pointer.fetchall()
    coneccion.close()
    return data [0][0]

def busqueda_marca(fi, fo, marca):
    coneccion = get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute('TotalVentasenUSDxMARCASGENERAL @FechaInicio = ?, @FechaFin = ? , @C_MARCA = ?', fi, fo, marca)
    data = pointer.fetchall()
    coneccion.close()

    if data:
        # Extraemos los dos valores de la primera (y única) fila
        tgeneral = data[0][0]  # Primer valor de la tupla
        txtiendas = data[0][1]  # Segundo valor de la tupla
        return tgeneral, txtiendas
    else:
        return None, None  # Si no hay datos, devolvemos None
 
def busqueda_marca_bs(fi,fo,marca):
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute('TotalVentasenBsxMARCASGENERAL @FechaInicio = ?, @FechaFin = ? , @C_MARCA = ?',fi,fo,marca)
    data = pointer.fetchall()
    coneccion.close()
    return data [0][0]

def busqueda_marca_x_tieda(fi,fo,marca):
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute(' TotalVentasenUSDxMARCASGENERALxTIENDAS @FechaInicio = ?, @FechaFin = ? , @C_MARCA = ?',fi,fo,marca)
    data = pointer.fetchall()
    coneccion.close()
    return data




def departamentos():
    coneccion =  get_db_connection()
    pointer = coneccion.cursor()
    pointer.execute('SELECT * FROM MA_DEPARTAMENTOS')
    data = pointer.fetchall()
    coneccion.close()
    return data



#BBROSE

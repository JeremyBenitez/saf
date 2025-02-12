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

fecha = datetime.now()
fecha_diaria = fecha.date()
fecha_hace_1Day = fecha_diaria - timedelta(days=1)

class ventas_x_tiendas:
    def __init__(self,fi,fo,store):
        self.fecha_ini = datetime.strptime(fi,'%Y-%m-%d')
        self.fecha_out = datetime.strptime(fo,'%Y-%m-%d')
        self.tienda = store
    def diario_cashea(self): #Venta diaria por tiende metodo cashea
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenUSDxTiendaCSH @FechaInicio = ? , @FechaFin = ?,@c_Localidad = ?',self.fecha_ini, self.fecha_out,self.tienda)
        data = cursor.fetchall()
        conetion.close()
        return data[0][0]

    def diaro_bs(self):
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenBsxTiendas @FechaInicio = ? , @FechaFin = ?,@c_Localidad = ?',self.fecha_ini, self.fecha_out,self.tienda)
        data = cursor.fetchall()
        conetion.close()
        return data[0][1]

    def diario_efectivo_usd(self):
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenUSDxTiendaEfectivo @FechaInicio = ? , @FechaFin = ?,@c_Localidad = ?',self.fecha_ini, self.fecha_out,self.tienda)
        data = cursor.fetchall()
        conetion.close()
        return data[0][0]

    def diario_usd(self):
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenUSDxTiendas @FechaInicio = ? , @FechaFin = ?,@c_Localidad = ?',self.fecha_ini, self.fecha_out,self.tienda)
        data = cursor.fetchall()
        venta = data[0][1]
        transacciones = data[0][0]
        conetion.close()    
        return venta,transacciones 

    

v_bs = ventas_x_tiendas(str(fecha_diaria),str(fecha_diaria),'0401')
ventas_bs_propatria = v_bs.diaro_bs()    

v_csh=ventas_x_tiendas(str(fecha_diaria),str(fecha_diaria),'0401')
ventas_csh_propatria = v_csh.diario_cashea()

v_usd=ventas_x_tiendas(str(fecha_diaria),str(fecha_diaria),'0401')
ventas_usd_propatria,transacciones = v_usd.diario_usd()

v_usd_efe=ventas_x_tiendas(str(fecha_diaria),str(fecha_diaria),'0401')
ventas_efe_propatria = v_usd_efe.diario_efectivo_usd()
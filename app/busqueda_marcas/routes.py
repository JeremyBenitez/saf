from flask import Blueprint, render_template, request,redirect,session,flash,url_for, jsonify
from collections import defaultdict
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime,timedelta
import pandas as pd
from ..querys_sqlite_data.database import departamentos, get_db_connection
import requests
from .tiendas import tiendas_completas, tiendas_simplificadas
marcas_bp = Blueprint('marcas', __name__)


@marcas_bp.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response



#nueva implmentacion
@marcas_bp.route('/marcasdetalles',methods=['GET', 'POST'])
def tiendasxmarcadetalles():
    try:
        
        data = request.json
        parametro_marca = f'%{data['marca']}%'
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("sp_reportes_ventas_productos @FechaInicio = ?, @FechaFin = ? , @Filtro  = ? "
                       ,(data['FechaInicio'],data['FechaFin'],parametro_marca))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        ventas = []
        unidades = []
        for suma_tienda in data:
            ventas.append(suma_tienda['total_USD'])
            unidades.append(suma_tienda['cantidad'])
        total_usd = sum(ventas)
        total_cantidades = sum(unidades)
        return jsonify({"Total_USD":total_usd, "cantidades":total_cantidades})
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@marcas_bp.route('/marcasdetallesbs',methods=['GET', 'POST'])
def marcasbs():
    try:
        
        data = request.json
        parametro_marca = f'%{data['marca']}%'
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("sp_reportes_ventas_productos_VES @FechaInicio = ?, @FechaFin = ? , @Filtro  = ? "
                       ,(data['FechaInicio'],data['FechaFin'],parametro_marca))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        total_bs = []
   
        for i in data:
            total_bs.append(i['total'])
  
        suma_total_bs = sum(total_bs)


        return jsonify({"Total_BS":suma_total_bs})
    except Exception as e:
        return jsonify({"error": str(e)}), 500






@marcas_bp.route('/marcasdetallesxtiendas',methods=['GET', 'POST'])
def tiendasxmarcadetalle_tiendas():
    try:
        data = request.json
        parametro_marca = f'%{data['marca']}%'
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("sp_reportes_ventas_productos @FechaInicio = ?, @FechaFin = ? , @Filtro  = ? "
                       ,(data['FechaInicio'],data['FechaFin'],parametro_marca))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        suma_por_tienda = defaultdict(lambda: {"total_USD": 0.0, "cantidad": 0.0})

        mapa_tiendas = dict(zip(tiendas_completas, tiendas_simplificadas))

        for registro in data:
            tienda_completa = registro["Tienda"]
            tienda_simplificada = mapa_tiendas.get(tienda_completa, tienda_completa)  
            suma_por_tienda[tienda_simplificada]["total_USD"] += registro.get("total_USD", 0.0)
            suma_por_tienda[tienda_simplificada]["cantidad"] += registro.get("cantidad", 0.0)
        return jsonify(suma_por_tienda)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




#//////////////////////////////////////////////////////////////////////








@marcas_bp.route('/ventasdepartamentos',methods=['GET', 'POST'])
def veentas_departamento_genral():
    try:
        data = request.json
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("sp_ReporteDepartamento_GENERAL @FechaInicio = ?, @FechaFin = ? , @Departamento  = ? "
                       ,(data['FechaInicio'],data['FechaFin'],data['c_departamento']))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500







@marcas_bp.route('/', methods=['GET', 'POST'])
def departamentos_lista():
    
    departamentos_select = departamentos()
    return render_template('marcas.html',
                            departamentos_select = departamentos_select                   
                           )
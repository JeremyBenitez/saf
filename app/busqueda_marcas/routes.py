from flask import Blueprint, render_template, request,redirect,session,flash,url_for, jsonify
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime,timedelta
import pandas as pd
from ..querys_sqlite_data.database import departamentos, get_db_connection
import requests

marcas_bp = Blueprint('marcas', __name__)


@marcas_bp.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response




@marcas_bp.route('/marcasusd',methods=['GET', 'POST'])
def marcas_USD():
    try:
        data = request.json
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("TotalVentasenUSDxMARCASGENERAL @FechaInicio = ?, @FechaFin = ? , @C_MARCA = ? "
                       ,(data['FechaInicio'],data['FechaFin'],data['marca']))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@marcas_bp.route('/marcasbs',methods=['GET', 'POST'])
def marcas_bs():
    try:
        data = request.json
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("TotalVentasenBsxMARCASGENERAL @FechaInicio = ?, @FechaFin = ? , @C_MARCA = ? "
                       ,(data['FechaInicio'],data['FechaFin'],data['marca']))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@marcas_bp.route('/apigeneral/', methods=['GET', 'POST'])
def apigeneral():
    try:
        # Datos enviados desde el cliente
        data = request.json
        fecha_inicio = data.get("FechaInicio")
        fecha_fin = data.get("FechaFin")
        marca = data.get('marca')
        payload = {
            "FechaInicio": fecha_inicio,
            "FechaFin": fecha_fin,
            "marca": marca
        }
        # Base URL para las otras APIs
        base_url = "http://192.168.2.103:5000"  
        
        # Endpoints a llamar
        endpoints = {
            "MarcaUSD": f"{base_url}/marcas/marcasusd",
            "MarcaBs": f"{base_url}/marcas/marcasbs",
            
           
        }


        results = {}
        headers = {"Content-Type": "application/json"}  # Encabezado común

        for key, url in endpoints.items():
            response = requests.post(url, json=payload, headers=headers)
            
            # Verificar si la respuesta fue exitosa
            if response.status_code == 200:
                results[key] = response.json()
            else:
                results[key] = {"error": f"Error al llamar {key}", "status": response.status_code}

        # Respuesta combinada
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@marcas_bp.route('/tiendas',methods=['GET', 'POST'])
def tiendasxmarca():
    try:
        data = request.json
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("TotalVentasenUSDxMARCASGENERALxTIENDAS @FechaInicio = ?, @FechaFin = ? , @C_MARCA = ? "
                       ,(data['FechaInicio'],data['FechaFin'],data['marca']))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



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
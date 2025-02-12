import sqlite3
from flask import Blueprint, render_template, request,redirect,session,flash, jsonify
import bcrypt
from ..querys_sqlite_data.cementerio import get_db_connection
import requests

appi = Blueprint('appi', __name__)



@appi.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response



# Función para leer el archivo Excel existente
def conexion():
    conn = sqlite3.connect('DBD1.db')
    conn.row_factory = sqlite3.Row
    return conn

@appi.route('/', methods=['POST'])
def insertar_usuario():
    data = request.json
    conn = conexion()
    cursor = conn.cursor()
    password_hashear = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
    cursor.execute("INSERT INTO USUARIOS (nombre_apellido,username, password,email,role_id) VALUES (?,?,?,?,?)", 
                   (data['nombre_apellido'].upper(),data['username'].upper(), password_hashear,data['email'], data['role_id']))
    conn.commit()
    conn.close()
    return jsonify(data)

@appi.route('/inserinventario', methods=['POST'])
def insertar_data_inventario():
    data = request.json
    conn = conexion()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO inventario_general (C_DEPOSITO,N_DEPOSITO, C_ARTICULO,N_ARTICULO,CANTIDAD,COSTO,PRECIO,DEPARTAMENTO,GRUPO,SUB_GRUPO) VALUES (?,?,?,?,?,?,?,?,?,?)", 
                   (data['C_DEPOSITO'],data['N_DEPOSITO'].upper(), data['C_ARTICULO'],data['N_ARTICULO'], data['CANTIDAD'], data['COSTO'], data['PRECIO'], data['DEPARTAMENTO'], data['GRUPO'], data['SUB_GRUPO']))
    conn.commit()
    conn.close()
    return jsonify(data)




@appi.route('/cementerio', methods=['POST'])
def tienda_cementerio_usd():
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('sp_ObtenerResumenPagosUSD_MultiDB_Externos  @FechaInicio = ? , @FechaFin = ?,@NumeroSucursal  = ?',(data['FechaInicio'], data['FechaFin'], data['sucursal']))
                    
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
@appi.route('/cementeriobs', methods=['POST'])
def tienda_cementerio_bs():
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenBsxTiendas_Externos  @FechaInicio = ? , @FechaFin = ?, @c_Localidad = ?',(data['FechaInicio'], data['FechaFin'],data['sucursal']))
                    
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    



@appi.route('/cementerioefec', methods=['POST'])
def tienda_cementerio_efct():
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenUSDxTiendaEfectivo_Externos  @FechaInicio = ? , @FechaFin = ?, @c_Localidad = ?',(data['FechaInicio'], data['FechaFin'],data['sucursal']))
                    
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
    
    
@appi.route('/apigeneral', methods=['GET', 'POST'])
def apigeneral():
    try:
        # Datos enviados desde el cliente
        data = request.json
        fecha_inicio = data.get("FechaInicio")
        fecha_fin = data.get("FechaFin")
        sucursal = data.get("sucursal")
        payload = {
            "FechaInicio": fecha_inicio,
            "FechaFin": fecha_fin,
            "sucursal":sucursal
        }
        # Base URL para las otras APIs
        base_url = "http://192.168.2.103:5000"  
        
        # Endpoints a llamar
        endpoints = {
            "usd": f"{base_url}/crear/cementerio",
            "bsTienda": f"{base_url}/crear/cementeriobs",
            "efectivo": f"{base_url}/crear/cementerioefec",
      
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

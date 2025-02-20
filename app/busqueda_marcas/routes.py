from flask import Blueprint, render_template, request,redirect,session,flash,url_for, jsonify
from collections import defaultdict
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime,timedelta
import pandas as pd
from ..querys_sqlite_data.database import departamentos, get_db_connection
import requests
from .tiendas import tiendas_completas, tiendas_simplificadas
from concurrent.futures import ThreadPoolExecutor, as_completed
import os
import json


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







#//////NUEVA IMPLEMENTACION DE SP DE DEPARTAMENTOS

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
        total = []
        for i in data:
            valor = int(i['TOTALUSD'])
            total.append(valor)
        return jsonify({"Total_ventas_departamento":sum(total)})
    except Exception as e:
        return jsonify({"error": str(e)}), 500







@marcas_bp.route('/ventasdepartamentosmultidb',methods=['GET', 'POST'])
def veentas_departamentomultidb():
    try:
        json = request.json
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("sp_ConsultaInventarioMultiDB2  @FechaInicio  = ?, @FechaFin = ?"
                       ,(json['FechaInicio'],json['FechaFin']))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        
        suma_por_tienda = defaultdict(lambda: {"total_USD": 0.0, "cantidad": 0.0})

        # Mapeo de tiendas
        mapa_tiendas = dict(zip(tiendas_completas, tiendas_simplificadas))
        filtro = json['filtro']

        total_usd = 0.0
        total_cantidad = 0.0

        for registro in data:
            # Verificar si el registro cumple con el filtro por 'c_Departamento'
            if registro.get("c_Departamento") == filtro:
                tienda_completa = registro["BaseDatos"]
                tienda_simplificada = mapa_tiendas.get(tienda_completa, tienda_completa)

                # Convertir 'total' de forma segura a float
                try:
                    valor_flotante = float(registro.get("total", 0.0))
                except (ValueError, TypeError):
                    valor_flotante = 0.0

                # Convertir 'cantidad' de forma segura a float
                try:
                    cantidad_flotante = float(registro.get("cantidad", 0.0))
                except (ValueError, TypeError):
                    cantidad_flotante = 0.0

                # Sumar al total por tienda
                suma_por_tienda[tienda_simplificada]["total_USD"] += valor_flotante
                suma_por_tienda[tienda_simplificada]["cantidad"] += cantidad_flotante

                # Sumar al total general
                total_usd += valor_flotante
                total_cantidad += cantidad_flotante

        # Convertir a un diccionario normal para que jsonify funcione correctamente
        suma_por_tienda = dict(suma_por_tienda)

        return jsonify({
            "filtro": filtro,
            "valores_tiendas": suma_por_tienda,
            "total_usd": total_usd,
            "total_cantidad": total_cantidad
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500







#valor en BS
@marcas_bp.route('/ventasdepartamentosmultidb_bs',methods=['GET', 'POST'])
def veentas_departamentomultidb_bs():
    try:
        json = request.json
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("sp_ConsultaInventarioMultiDB2VES  @FechaInicio  = ?, @FechaFin = ?"
                       ,(json['FechaInicio'],json['FechaFin']))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        
        suma_por_tienda = defaultdict(lambda: {"total_BS": 0.0})

        # Mapeo de tiendas
        mapa_tiendas = dict(zip(tiendas_completas, tiendas_simplificadas))
        filtro = json['filtro']

        total_bs = 0.0

        for registro in data:
            # Verificar si el registro cumple con el filtro por 'c_Departamento'
            if registro.get("c_Departamento") == filtro:
                tienda_completa = registro["BaseDatos"]
                tienda_simplificada = mapa_tiendas.get(tienda_completa, tienda_completa)

                # Convertir 'total' de forma segura a float
                try:
                    valor_flotante = float(registro.get("total", 0.0))
                except (ValueError, TypeError):
                    valor_flotante = 0.0

                # Sumar al total por tienda
                suma_por_tienda[tienda_simplificada]["total_BS"] += valor_flotante

                # Sumar al total general
                total_bs += valor_flotante


        return jsonify({
            "filtro": filtro,
            "total_bs": total_bs,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500




CACHE_FILE = "cache.json"

def load_cache():
    """Carga el contenido del archivo de caché si existe."""
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_cache(data):
    """Guarda los datos en el archivo de caché."""
    with open(CACHE_FILE, "w") as f:
        json.dump(data, f)



@marcas_bp.route('/consulta_general', methods=['GET', 'POST'])
def consulta_general():
    try:
        # Datos enviados desde el cliente
        data = request.json
        fecha_inicio = data.get("FechaInicio")
        fecha_fin = data.get("FechaFin")
        filtro = data.get("filtro")
        payload = {
            "FechaInicio": fecha_inicio,
            "FechaFin": fecha_fin,
            "filtro": filtro
        }

        # Generar clave única para la caché (basada en la consulta)
        cache_key = f"{fecha_inicio}_{fecha_fin}_{filtro}"

        # Cargar la caché existente
        cache = load_cache()

        # Verificar si la consulta ya está en la caché
        if cache_key in cache:
            return jsonify(cache[cache_key])

        # Base URL para las otras APIs
        base_url = "http://10.21.5.99:5000"

        # Endpoints a llamar
        endpoints = {
            "usd": f"{base_url}/marcas/ventasdepartamentosmultidb",
            "bsTienda": f"{base_url}/marcas/ventasdepartamentosmultidb_bs",
        }

        results = {}
        headers = {"Content-Type": "application/json"}  # Encabezado común

        # Definir una función para realizar la solicitud
        def fetch_data(key, url):
            try:
                response = requests.post(url, json=payload, headers=headers)
                if response.status_code == 200:
                    return key, response.json()
                else:
                    return key, {"error": f"Error al llamar {key}", "status": response.status_code}
            except Exception as e:
                return key, {"error": str(e)}

        # Ejecutar las solicitudes en paralelo
        with ThreadPoolExecutor() as executor:
            futures = [executor.submit(fetch_data, key, url) for key, url in endpoints.items()]

            for future in as_completed(futures):
                key, result = future.result()
                results[key] = result

        # Almacenar el resultado en la caché
        cache[cache_key] = results
        save_cache(cache)

        # Respuesta combinada
        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)}), 500





#/////////////////////////////\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

@marcas_bp.route('/', methods=['GET', 'POST'])
def departamentos_lista():
    
    departamentos_select = departamentos()
    return render_template('marcas.html',
                            departamentos_select = departamentos_select                   
                           )
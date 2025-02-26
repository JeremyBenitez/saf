from flask import Blueprint, render_template, request,redirect,session,flash,url_for, jsonify
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime,timedelta
import pandas as pd
from ..querys_sqlite_data.database import  get_db_connection
from .tiendas import tiendas_completas, tiendas_simplificadas
from collections import defaultdict
import os
import json
import requests
from .meses import mes_fin, mes_init



tendecias_bp = Blueprint('tendencias', __name__)



@tendecias_bp.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response


@tendecias_bp.route('/',methods=['GET', 'POST'])
def tendencias():
  
   
    return render_template('tendencias.html')




CACHE_FILE = "cashe_tendencias.json"

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


@tendecias_bp.route('/tendencia',methods=['GET', 'POST'])
def producto_en_tendencia():
    try:
        json_data = request.json
        filtro = json_data['filtro']
        cache_key = f"{json_data['FechaInicio']}_{json_data['FechaFin']}_{filtro}"
        
        # Cargar caché
        cache = load_cache()
        if cache is None:
            cache = {}  # Asegurar que cache siempre es un diccionario válido
        
        # Verificar si la consulta ya está en caché
        if cache_key in cache:
            print("Cache hit:", cache_key)  # Debugging
            return jsonify(cache[cache_key])
        
        print("Cache miss, generando datos...")  # Debugging

        # Si no está en caché, realizar la consulta a la BD
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("sp_ConsultaInventarioMultiDB2  @FechaInicio  = ?, @FechaFin = ?", 
                       (json_data['FechaInicio'], json_data['FechaFin']))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()

        # Procesamiento de datos
        suma_por_tienda = defaultdict(lambda: {"total_USD": 0.0, "cantidad": 0.0, "producto_mas_vendido": {"nombre": None, "cantidad": 0, "codigo": None}})
        mapa_tiendas = dict(zip(tiendas_completas, tiendas_simplificadas))
        total_usd = 0.0
        total_cantidad = 0.0

        productos_por_tienda = defaultdict(lambda: defaultdict(lambda: {"cantidad": 0.0, "codigo": "N/A"}))
        
        for registro in data:
            if registro.get("c_Departamento") == filtro:
                tienda_completa = registro["BaseDatos"]
                tienda_simplificada = mapa_tiendas.get(tienda_completa, tienda_completa)
                
                valor_flotante = float(registro.get("total", 0.0)) if registro.get("total") else 0.0
                cantidad_flotante = float(registro.get("cantidad", 0.0)) if registro.get("cantidad") else 0.0
                
                producto = registro.get("c_Descri", "Desconocido")
                codigo_articulo = registro.get("cod_principal", "N/A")
                
                suma_por_tienda[tienda_simplificada]["total_USD"] += valor_flotante
                suma_por_tienda[tienda_simplificada]["cantidad"] += cantidad_flotante
                productos_por_tienda[tienda_simplificada][producto]["cantidad"] += cantidad_flotante
                productos_por_tienda[tienda_simplificada][producto]['codigo'] = codigo_articulo
                
                total_usd += valor_flotante
                total_cantidad += cantidad_flotante
        
        for tienda, productos in productos_por_tienda.items():
            if productos:
                producto_mas_vendido = max(productos, key=lambda p: productos[p]["cantidad"])
                suma_por_tienda[tienda]["producto_mas_vendido"] = {
                    "nombre": producto_mas_vendido,
                    "codigo": productos[producto_mas_vendido]["codigo"],
                    "cantidad": productos[producto_mas_vendido]["cantidad"]
                }

        resultado = {
            "filtro": filtro,
            "valores_tiendas": dict(suma_por_tienda),
            "total_usd": total_usd,
            "total_cantidad": total_cantidad
        }
        
        # Guardar en caché
        cache[cache_key] = resultado
        save_cache(cache)

        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@tendecias_bp.route('/detalles/<dpto>', methods=['GET', 'POST'])
def departamentos(dpto):
    json_data = request.get_json()

    fechaini = mes_init[1]
    fechFin = mes_fin[1]
    
    # Verifica que el JSON sea válido y contenga las claves necesarias

    cache_key = f"{fechaini}_{fechFin}_{dpto}"

    cache = load_cache() or {}  

    if cache_key in cache:
        return jsonify(cache[cache_key])  

    return jsonify({"error": "Datos no encontrados en caché"}), 404








@tendecias_bp.route('/api/cantidad', methods=['GET', 'POST'])
def cantidad_depatos():
    dpto = ['AC','AU','BE','CI','CO','CP','CZ','DP','FE','FR','HG','IN','JG','OF','PE','Pl','RP','TG']
    try:
        payload = {
            "FechaInicio": "2025-02-01",
            "FechaFin": "2025-02-28",
        }
        headers = {"Content-Type": "application/json"}  # Encabezado común
        resultado = []
        for i in dpto:
            url = f'http://10.21.5.23:5000/tendencias/detalles/{i}'
            response = requests.post(url, json=payload, headers=headers)
            
            if response.status_code in [200,201]:
                resultado.append(response.json())
        dpto = []
        cantidades = []
        for i in range(0, len(resultado)):
            dpto.append(resultado[i]['filtro'])
            cantidades.append(resultado[i]['total_cantidad'])
        diccionario = [dict(zip(dpto,cantidades))]
        return jsonify(diccionario)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
        


"""


"""
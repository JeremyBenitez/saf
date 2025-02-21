from flask import Blueprint, render_template, request,redirect,session,flash,url_for, jsonify
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime,timedelta
import pandas as pd
from ..querys_sqlite_data.database import  get_db_connection
from .tiendas import tiendas_completas, tiendas_simplificadas
from collections import defaultdict


tendecias_bp = Blueprint('tendencias', __name__)

@tendecias_bp.route('/',methods=['GET', 'POST'])
def tendencias():
  
   
    return render_template('tendencias.html')



@tendecias_bp.route('/tendencia',methods=['GET', 'POST'])
def producto_en_tendencia():
    try:
        json_data = request.json
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("sp_ConsultaInventarioMultiDB2  @FechaInicio  = ?, @FechaFin = ?", 
                       (json_data['FechaInicio'], json_data['FechaFin']))              
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]
        conexion.close()
        
        suma_por_tienda = defaultdict(lambda: {"total_USD": 0.0, "cantidad": 0.0, "producto_mas_vendido": {"nombre": None, "cantidad": 0}})
        mapa_tiendas = dict(zip(tiendas_completas, tiendas_simplificadas))
        filtro = json_data['filtro']
        total_usd = 0.0
        total_cantidad = 0.0
        
        productos_por_tienda = defaultdict(lambda: defaultdict(float))
        
        for registro in data:
            if registro.get("c_Departamento") == filtro:
                tienda_completa = registro["BaseDatos"]
                tienda_simplificada = mapa_tiendas.get(tienda_completa, tienda_completa)
                
                try:
                    valor_flotante = float(registro.get("total", 0.0))
                except (ValueError, TypeError):
                    valor_flotante = 0.0
                
                try:
                    cantidad_flotante = float(registro.get("cantidad", 0.0))
                except (ValueError, TypeError):
                    cantidad_flotante = 0.0
                
                producto = registro.get("cod_principal", "Desconocido")
                
                suma_por_tienda[tienda_simplificada]["total_USD"] += valor_flotante
                suma_por_tienda[tienda_simplificada]["cantidad"] += cantidad_flotante
                productos_por_tienda[tienda_simplificada][producto] += cantidad_flotante
                
                total_usd += valor_flotante
                total_cantidad += cantidad_flotante
        
        for tienda, productos in productos_por_tienda.items():
            if productos:
                producto_mas_vendido = max(productos, key=productos.get)
                suma_por_tienda[tienda]["producto_mas_vendido"] = {
                    "nombre": producto_mas_vendido,
                    "cantidad": productos[producto_mas_vendido]
                }
        
        return jsonify({
            "filtro": filtro,
            "valores_tiendas": dict(suma_por_tienda),
            "total_usd": total_usd,
            "total_cantidad": total_cantidad
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

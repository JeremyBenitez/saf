from flask import Blueprint, render_template, request,redirect,session,flash,url_for, jsonify
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime,timedelta
import pandas as pd
from ..querys_sqlite_data.query_inventario import bases_datos, departamentos, get_db_connection

inventario_bp = Blueprint('inventario', __name__)

@inventario_bp.route('/grupos/',methods=['GET', 'POST'])
def grupos():
    try:
        c_departamento = None
        datos = request.json

        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM MA_GRUPOS WHERE c_departamento = ?", 
                       (datos['codigo'],))
        columns = [column[0] for column in cursor.description]

        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conexion.close()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@inventario_bp.route('/resinventario',methods=['GET', 'POST'])
def resultado():
     try:
        datos = request.json
        conexion = get_db_connection()
        cursor = conexion.cursor()
        cursor.execute("sp_ObtenerArticulosConUnionesDinamico   @c_CodDeposito = ? , @f_FechaInicio = ?, @BaseDatos = ?, @c_Departamento = ?", 
                       (datos['c_CodDeposito'],datos['f_FechaInicio'],datos['BaseDatos'],datos['c_Departamento']))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conexion.close()

        return jsonify(data)

     except Exception as e:
        return jsonify({"error": str(e)}), 500


@inventario_bp.route('/',methods=['GET', 'POST'])
def inventario():
     
     bbdds = bases_datos()
     deptos = departamentos()
     
     return render_template('inventario.html', bases = bbdds,
                            deptos = deptos)


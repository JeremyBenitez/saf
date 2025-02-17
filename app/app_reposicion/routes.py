from flask import Blueprint, render_template,request,jsonify
from ..querys_sqlite_data.database import get_db_connection
import sqlite3
app_reposicion = Blueprint('app_reposicion', __name__)

@app_reposicion.route('/') 
def index():

    return render_template('reposicion.html')




@app_reposicion.route('/analisis', methods=['GET', 'POST'])
def analisis():
    try:
        data = request.json
        conexion = get_db_connection()
        pointer = conexion.cursor()
        pointer.execute("sp_AnalisisInventario @FechaInicio = ? , @FechaFin = ?, @CodArticulo = ?",(data["fecha_init"],data["fecha_end"], data['codigo_articulo']))
        rows = pointer.fetchall()     
        columns = [column[0] for column in pointer.description]
        data = [dict(zip(columns, row)) for row in rows]
        
        conexion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

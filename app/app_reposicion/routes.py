from flask import Blueprint, render_template,request,jsonify
from ..querys_sqlite_data.database import get_db_connection

app_reposicion = Blueprint('app_reposicion', __name__)

@app_reposicion.route('/') 
def index():

    return render_template('reposicion.html')

@app_reposicion.route('/repo', methods=['GET'])
def buscar():
    try:
        # Obtener los parámetros de la solicitud
        codigo = request.args.get('codigo')  
        fecha_ini = request.args.get('fecha_ini')
        fecha_fin = request.args.get('fecha_fin')
        
        # Validar si se enviaron todos los parámetros necesarios
        if not (codigo and fecha_ini and fecha_fin):
            return jsonify({'error': 'Faltan Datos para la Búsqueda'}), 400
        
        # Conexión a la base de datos
        db = get_db_connection()
        cursor = db.cursor()

        # Ejecutar el procedimiento almacenado con los parámetros
        query = '[dbo].[sp_AnalisisInventario] @FechaInicio = ?, @FechaFin = ?, @CodArticulo = ?'
        cursor.execute(query, (fecha_ini, fecha_fin, codigo))
        #cursor.execute(query, ('2024-12-24','2024-12-24','RPCA01100048'))

        # Obtener los nombres de las columnas de la consulta
        columns = [column[0] for column in cursor.description]
        
        # Obtener todas las filas y mapearlas a un diccionario
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        # Cerrar la conexión a la base de datos
        db.close()
        
        # Si hay datos, devolver el JSON
        if data:
            return jsonify(data)
        else:
            return jsonify({'error': 'Datos no encontrados'}), 404
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


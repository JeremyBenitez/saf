from flask import Blueprint, render_template,request,jsonify
from ..querys_sqlite_data.database import get_db_connection

app_ajustes = Blueprint('app_ajustes', __name__)

@app_ajustes.route('/') 
def index():

    return render_template('ajustes.html')


@app_ajustes.route('/aju', methods=['GET'])
def buscar_ajustes():
    try:
        # Obtener los parámetros de la solicitud
        tienda = request.args.get('tienda')  
        fecha_ini = request.args.get('fecha_ini')
        fecha_fin = request.args.get('fecha_fin')
        
        # Validar si se enviaron todos los parámetros necesarios
        if not (tienda and fecha_ini and fecha_fin):
            return jsonify({'error': 'Faltan Datos para la Búsqueda'}), 400
        
        # Conexión a la base de datos
        db = get_db_connection()
        cursor = db.cursor()

        # Ejecutar el procedimiento almacenado con los parámetros
        query = 'sp_Cabecera_ma_inventario @FechaInicio = ?, @FechaFin = ?, @DBName = ?'
        cursor.execute(query, (fecha_ini, fecha_fin, tienda))

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
    
@app_ajustes.route('/detalles', methods=['GET'])
def buscar_detalles():
    try:
        # Obtener los parámetros de la solicitud
        fecha_ini = request.args.get('fecha_ini')
        fecha_fin = request.args.get('fecha_fin')
        tienda = request.args.get('tienda')  
        documento = request.args.get('documento')

        # Validar si se enviaron todos los parámetros necesarios
        if not (tienda and fecha_ini and fecha_fin and documento):
            return jsonify({'error': 'Faltan Datos para la Búsqueda'}), 400
        
        # Conexión a la base de datos
        db = get_db_connection()
        cursor = db.cursor()

        # Ejecutar el procedimiento almacenado con los parámetros
        query = 'sp_ConsultaTRInventarioAJU @FechaInicio = ?, @FechaFin = ?, @DBName = ?, @Documento = ?'
        cursor.execute(query, (fecha_ini, fecha_fin, tienda, documento))

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
    

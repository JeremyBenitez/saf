from flask import Blueprint, render_template, request,redirect,session,flash,url_for,jsonify
from ..querys_sqlite_data.conexion_sqlite import consulta_ventas
from datetime import datetime,timedelta
from ..querys_sqlite_data.database import get_db_connection
import sqlite3
import requests
from ..querys_sqlite_data.database import general_usd, general_efe,general_csh,general_bs


fechas_bp = Blueprint('fechas', __name__)

@fechas_bp.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response





@fechas_bp.route('/usd/<tienda>', methods=['GET', 'POST'])
def tiendas(tienda):
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
         # Lista de tiendas
        cursor.execute('sp_ObtenerResumenPagosUSD_MultiDB @FechaInicio = ? , @FechaFin = ?,@NumeroSucursal = ?',(data['fecha_ini'],data['fecha_fin'],tienda))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fechas_bp.route('/transacciones/<tienda>', methods=['GET', 'POST'])
def transacciones(tienda):
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
         # Lista de tiendas
        cursor.execute('TotalVentasenUSDxTiendas @FechaInicio = ? , @FechaFin = ?,@c_Localidad = ?',(data['FechaInicio'],data['FechaFin'],tienda))
        rows = cursor.fetchall()
        if rows:
            n_transacciones = rows[0][0]
        else:
            n_transacciones = 0

        conetion.close()
        return jsonify([{"n_transacciones": n_transacciones}])
    except Exception as e:
        return jsonify({"error": str(e)}), 500






@fechas_bp.route('/posEfe/<tienda>', methods=['GET', 'POST'])
def tienda_Efectiva_POS(tienda):
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('sp_ObtenerResumenPagosUSD_MultiDB  @FechaInicio = ? , @FechaFin = ?,@NumeroSucursal  = ?',(data['FechaInicio'], data['FechaFin'], tienda))
                    
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@fechas_bp.route('/bsTienda/<tienda>', methods=['GET', 'POST'])
def tiendasBS(tienda):
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenBsxTiendas  @FechaInicio = ? , @FechaFin = ?,@c_Localidad  = ?',(data['FechaInicio'], data['FechaFin'], tienda))
                    
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@fechas_bp.route('/cshtienda/<tienda>', methods=['GET', 'POST'])
def tiendasCSH(tienda):
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenUSDxTiendaCSH  @FechaInicio = ? , @FechaFin = ?,@c_Localidad  = ?',(data['FechaInicio'], data['FechaFin'], tienda))
                    
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@fechas_bp.route('/cshgeneral', methods=['GET', 'POST'])
def tiendasgeneral():
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenUSDxGeneralCSHISTORICO  @FechaInicio = ? , @FechaFin = ?',(data['FechaInicio'], data['FechaFin']))
                    
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@fechas_bp.route('/efectivo/<tienda>', methods=['GET', 'POST'])
def tiendasEFE(tienda):
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
        cursor.execute('TotalVentasenUSDxTiendaEfectivo  @FechaInicio = ? , @FechaFin = ?,@c_Localidad  = ?',(data['FechaInicio'], data['FechaFin'], tienda))
                    
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500





@fechas_bp.route('/apigeneral/<tienda>', methods=['GET', 'POST'])
def apigeneral(tienda):
    try:
        # Datos enviados desde el cliente
        data = request.json
        fecha_inicio = data.get("FechaInicio")
        fecha_fin = data.get("FechaFin")
        payload = {
            "FechaInicio": fecha_inicio,
            "FechaFin": fecha_fin
        }
        # Base URL para las otras APIs
        base_url = "http://192.168.2.103:5000"  
        
        # Endpoints a llamar
        endpoints = {
            "posEfe": f"{base_url}/fechas/posEfe/{tienda}",
            "bsTienda": f"{base_url}/fechas/bsTienda/{tienda}",
            "cshTienda": f"{base_url}/fechas/cshtienda/{tienda}",
            "efectivo": f"{base_url}/fechas/efectivo/{tienda}",
            "transacciones":f"{base_url}/fechas/transacciones/{tienda}"
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






@fechas_bp.route('/usdxtiendas/<tienda>', methods=['GET', 'POST'])
def usdxTiendas(tienda):
    try:
        data = request.json
        conexion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\BDTiendas.db")
        pointer = conexion.cursor()
        pointer.execute(f"""
                        SELECT 
        SUM(V_USD) AS total_usd,
        SUM(V_BS) AS total_bs,
        SUM(V_CSH) AS total_csh,
        SUM(V_EFEC) AS total_efec,
        n_trasacciones
    FROM (
        SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA,n_trasacciones FROM {tienda}
        
    ) AS todas_las_tablas
    WHERE FECHA BETWEEN ? AND ?
    """,(data["fecha_init"],data["fecha_end"]))
        rows = pointer.fetchall()     
        columns = [column[0] for column in pointer.description]
        data = [dict(zip(columns, row)) for row in rows]
        
        conexion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500





    
    
@fechas_bp.route('/generalEfePos', methods=['GET', 'POST'])
def efectividadPos():
    try:
        data = request.json
        conetion = get_db_connection()
        cursor = conetion.cursor()
        
        cursor.execute('sp_ObtenerResumenPagosUSD_MultiDB_GENERAL @FechaInicio = ? , @FechaFin = ?',(data['fecha_ini'],data['fecha_fin']))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@fechas_bp.route('/consultassp', methods=['GET', 'POST'])
def consulta_sp():
    try:
        data = request.json
        conetion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\BD2024.db")
        cursor = conetion.cursor()
        
        cursor.execute("""
                       SELECT 
    SUM(V_USD) AS total_usd,
    SUM(V_BS) AS total_bs,
    SUM(V_CSH) AS total_csh,
    SUM(V_EFEC) AS total_efec
FROM (
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM BABILON
    UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM BARALT
    UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CABUDARE
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CAGUA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CABIMAS
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CATIA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CRUZVERDE
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM GUACARA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM GUANARE
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM KAPITANA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM MATURIN
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM PROPATRIA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM UPATA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM VALENCIA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM VALERA
) AS todas_las_tablas
WHERE FECHA BETWEEN ? AND ?;""",(data['fecha_ini'],data['fecha_fin']))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@fechas_bp.route('/usdxtiendas2024/<tabla>', methods=['GET', 'POST'])
def usdxTiendas2024(tabla):
    try:
        data = request.json
        conexion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\BD2024.db")
        pointer = conexion.cursor()
        pointer.execute(f"""
                        SELECT 
        SUM(V_USD) AS total_usd,
        SUM(V_BS) AS total_bs,
        SUM(V_CSH) AS total_csh,
        SUM(V_EFEC) AS total_efec
        
    FROM (
        SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM {tabla}
        
    ) AS todas_las_tablas
    WHERE FECHA BETWEEN ? AND ?
    """,(data["fecha_init"],data["fecha_end"]))
        rows = pointer.fetchall()     
        columns = [column[0] for column in pointer.description]
        data = [dict(zip(columns, row)) for row in rows]
        
        conexion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




    
    
@fechas_bp.route('/', methods=['GET', 'POST'])
def fechas():
    usd = 0
    bs = 0
    csh = 0
    efectivo = 0
    rango_de_busqueda = [(0,0,0,0)]
    start_date = None
    end_date = None
    if request.method == "POST":
        date_init = request.form.get('startDate')
        date_end = request.form.get('endDate')
        if date_init and date_end:
            start_date = date_init
            end_date = date_end
            rango_de_busqueda = consulta_ventas(str(start_date),str(end_date))
            
    # Formatear las fechas de start_date y end_date a DD-MM-YYYY
    if rango_de_busqueda[0][0] is None:
        usd = 0
    else:
        usd = rango_de_busqueda[0][0]
        
    if rango_de_busqueda[0][1] is None:
        bs = 0
    else:
        bs = rango_de_busqueda[0][1]
    
    if rango_de_busqueda[0][2] is None:
        csh = 0
    else:
        csh = rango_de_busqueda[0][2]
    
    if rango_de_busqueda[0][3] is None:
        efectivo = 0
    else:
        efectivo = rango_de_busqueda[0][3]
    """ if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').strftime('%d-%m-%Y')
    if end_date:
        end_date = datetime.strptime(end_date, '%Y-%m-%d').strftime('%d-%m-%Y')"""
    return render_template('fechas.html', 
                           anterior_usd=usd,
                           bolivares=bs,
                           cashea=csh,
                           efectivo=efectivo,
                           start_date=start_date,  # Fecha de inicio formateada
                           end_date=end_date)  # Fecha de fin formateada

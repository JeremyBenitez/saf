from flask import Blueprint, render_template,request,jsonify
import sqlite3
app_resumen = Blueprint('app_resumen', __name__)

@app_resumen.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    return response




@app_resumen.route('/tiendas', methods=['GET', 'POST'])
def ventas():
    try:
        data = request.json
        conetion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\DBD1.db")
        cursor = conetion.cursor()
        cursor.execute("SELECT V_USD, MES FROM ventas_mensuales_2024 WHERE TIENDA = ?",(data['tienda'],))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app_resumen.route('/totales/<mes>', methods=['GET', 'POST'])
def ventas_tiendas(mes):
    try:
        data = request.json
        conetion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\DBD1.db")
        cursor = conetion.cursor()
        cursor.execute("SELECT sum(V_USD) FROM ventas_mensuales_2024 where mes = ? ",(mes,))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500



@app_resumen.route('/tioi/<mes>', methods=['GET', 'POST'])
def ventas_tiendas_tioi(mes):
    try:
        data = request.json
        conetion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\DBD1.db")
        cursor = conetion.cursor()
        cursor.execute("""
                    SELECT SUM(V_USD) 
                    FROM ventas_mensuales_2024 
                    WHERE TIENDA IN ('Kapitana', 'Valencia', 'Guacara','Cagua') AND MES = ?; """,(mes,))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app_resumen.route('/tioii/<mes>', methods=['GET', 'POST'])
def ventas_tiendas_tioii(mes):
    try:
        data = request.json
        conetion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\DBD1.db")
        cursor = conetion.cursor()
        cursor.execute("""
                    SELECT SUM(V_USD) 
                    FROM ventas_mensuales_2024 
                    WHERE TIENDA IN ('Cruz verde', 'Cabimas', 'Babilon','Guanare','Cabudare','Valera','Catia') AND MES = ?; """,(mes,))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app_resumen.route('/tioiv/<mes>', methods=['GET', 'POST'])
def ventas_tiendas_tioiv(mes):
    try:
        data = request.json
        conetion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\DBD1.db")
        cursor = conetion.cursor()
        cursor.execute("""
                    SELECT SUM(V_USD) 
                    FROM ventas_mensuales_2024 
                    WHERE TIENDA IN ('Propatria','Baralt','Maturin','Upata') AND MES = ?; """,(mes,))
        columns = [column[0] for column in cursor.description]
        rows = cursor.fetchall()
        data = [dict(zip(columns, row)) for row in rows]

        conetion.close()
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app_resumen.route('/') 
def index():
    def usd():
        conexion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\DBD1.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT SUM(V_USD) FROM ventas_mensuales_2024")
        data = cursor.fetchone()
        conexion.close()
        return data
    data = usd()
    
    def bs():
        conexion = sqlite3.connect(r"C:\Users\Windows 11\Desktop\SAF-DASHBOARD\BBDDs\DBD1.db")
        cursor = conexion.cursor()
        cursor.execute("SELECT SUM(V_BS) FROM ventas_mensuales_2024")
        data = cursor.fetchone()
        conexion.close()
        return data
    
    data_bs = bs()
    return render_template('resumen.html', data = data[0], data_bs = data_bs[0])
from flask import Blueprint, render_template, request,redirect,session,flash,url_for, jsonify
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime,timedelta
import pandas as pd
from calendar import monthrange

from ..querys_sqlite_data import conexion_sqlite

"hola"

fecha = datetime.now()
fecha_diaria = fecha.date()

index_bp = Blueprint('index', __name__)

@index_bp.route('/',methods=['GET', 'POST'])
def index():
    hoy = datetime.today()
    año_actual = hoy.year
    mes_actual = hoy.month
    ventas_mensuales = []
    nombres_meses = []

    def ultimo_dia_mes(año, mes):
        return str(monthrange(año, mes)[1])
    
    meses = {
        'Enero': ('2025-01-01', f'2025-01-{ultimo_dia_mes(2025, 1)}'),
        'Febrero': ('2025-02-01', f'2025-02-{ultimo_dia_mes(2025, 2)}'),
        'Marzo': ('2025-03-01', f'2025-03-{ultimo_dia_mes(2025, 3)}'),
        'Abril': ('2025-04-01', f'2025-04-{ultimo_dia_mes(2025, 4)}'),
        'Mayo': ('2025-05-01', f'2025-05-{ultimo_dia_mes(2025, 5)}'),
        'Junio': ('2025-06-01', f'2025-06-{ultimo_dia_mes(2025, 6)}'),
        'Julio': ('2025-07-01', f'2025-07-{ultimo_dia_mes(2025, 7)}'),
        'Agosto': ('2025-08-01', f'2025-08-{ultimo_dia_mes(2025, 8)}'),
        'Septiembre': ('2025-09-01', f'2025-09-{ultimo_dia_mes(2025, 9)}'),
        'Octubre': ('2025-10-01', f'2025-10-{ultimo_dia_mes(2025, 10)}'),
        'Noviembre': ('2025-11-01', f'2025-11-{ultimo_dia_mes(2025, 11)}'),
        'Diciembre': ('2025-12-01', f'2025-12-{ultimo_dia_mes(2025, 12)}')
    }
    
    try:
        for mes, (inicio, fin) in meses.items():

            mes_numero = int(fin.split("-")[1])
           
            if año_actual > 2025 or (año_actual == 2025 and mes_numero < mes_actual):

                resultado = conexion_sqlite.consulta_ventas(inicio, fin)
                if resultado and len(resultado) > 0:
                    ventas_mensuales.append(resultado[0][0])
                    nombres_meses.append(mes)
                else:
                    print(f"No hay datos para {mes}")

        grafico_mensuales = ventas_mensuales
    
    except Exception as e:
        print(f"Error al procesar los datos: {str(e)}")

    # enero = conexion_sqlite.consulta_ventas('2025-01-02','2025-01-31')
    # febrero = conexion_sqlite.consulta_ventas('2025-02-01','2025-02-31')
    # marzo = conexion_sqlite.consulta_ventas('2025-03-01','2025-03-31')
    # abril = conexion_sqlite.consulta_ventas('2025-04-01','2025-04-31')
    # mayo = conexion_sqlite.consulta_ventas('2025-05-01','2025-05-31')
    # junio = conexion_sqlite.consulta_ventas('2025-06-01','2025-06-31')
    # julio = conexion_sqlite.consulta_ventas('2025-07-01','2025-07-31')
    # agosto = conexion_sqlite.consulta_ventas('2025-08-01','2025-08-31')
    # septiembre = conexion_sqlite.consulta_ventas('2025-09-01','2025-09-31')
    # octubre = conexion_sqlite.consulta_ventas('2025-10-01','2025-10-31')
    # noviembre = conexion_sqlite.consulta_ventas('2025-11-01','2025-11-31')
    # diciembre = conexion_sqlite.consulta_ventas('2025-12-01','2025-12-31')

    grafico_tiendas = conexion_sqlite.index()
    babilon = grafico_tiendas.valores('BABILON')
    baralt = grafico_tiendas.valores('BARALT')        
    cabudare = grafico_tiendas.valores('CABUDARE')    
    cagua = grafico_tiendas.valores('CAGUA')
    cabimas = grafico_tiendas.valores('CABIMAS')      
    catia = grafico_tiendas.valores('CATIA')
    cruz_verde = grafico_tiendas.valores('CRUZ_VERDE')
    guacara = grafico_tiendas.valores('GUACARA')      
    guanare = grafico_tiendas.valores('GUANARE')      
    kapitana = grafico_tiendas.valores('KAPITANA')    
    maturin = grafico_tiendas.valores('MATURIN')      
    propatria = grafico_tiendas.valores('PROPATRIA')  
    upata = grafico_tiendas.valores('UPATA')
    valencia = grafico_tiendas.valores('VALENCIA')    
    valera = grafico_tiendas.valores('VALERA') 

    ventas = conexion_sqlite.consulta_ventas(str(fecha_diaria), str(fecha_diaria))

    grafico_usd = [babilon]
    # grafico_mensuales = [enero[0][0], febrero[0][0], marzo[0][0], abril[0][0], mayo[0][0], junio[0][0], julio[0][0], agosto[0][0], septiembre[0][0], octubre[0][0], noviembre[0][0], diciembre[0][0]]
    if 'username' in session:

            return render_template('index.html',
                                username = session.get('username'),


                                total_ventas = ventas[0][0],
                                total_bs = ventas[0][1],
                                cashea_total = ventas[0][2],
                                efectivo_total = ventas[0][3],
                                tasa_dia = 2020,
                                grafico_tiendas = [babilon[-1][0],
                                                    baralt[-1][0],
                                                    cabudare[-1][0],
                                                    cagua[-1][0],
                                                    cabimas[-1][0],
                                                    catia[-1][0],
                                                    cruz_verde[-1][0],
                                                    guacara[-1][0],
                                                    guanare[-1][0],
                                                    kapitana[-1][0],
                                                    maturin[-1][0],
                                                    propatria[-1][0],
                                                    upata[-1][0],
                                                    valencia[-1][0],
                                                    valera[-1][0]],


                                grafico_trans = [babilon[-1][1],
                                                    baralt[-1][1],
                                                    cabudare[-1][1],
                                                    cagua[-1][1],
                                                    cabimas[-1][1],
                                                    catia[-1][1],
                                                    cruz_verde[-1][1],
                                                    guacara[-1][1],
                                                    guanare[-1][1],
                                                    kapitana[-1][1],
                                                    maturin[-1][1],
                                                    propatria[-1][1],
                                                    upata[-1][1],
                                                    valencia[-1][1],
                                                    valera[-1][1]],
                                grafico_mensuales = grafico_mensuales,

                                )
        
    else:
        flash('Debes iniciar sesión para acceder a esta página')
        return redirect(url_for('loggin.loggin'))
    
    


@index_bp.route('/frontd',methods=['GET', 'POST'])
def index2():
    try:

        ventas = conexion_sqlite.consulta_ventas(str(fecha_diaria), str(fecha_diaria))

        grafico_tiendas = conexion_sqlite.index()
        babilon = grafico_tiendas.valores('BABILON')
        baralt = grafico_tiendas.valores('BARALT')        
        cabudare = grafico_tiendas.valores('CABUDARE')    
        cagua = grafico_tiendas.valores('CAGUA')
        cabimas = grafico_tiendas.valores('CABIMAS')      
        catia = grafico_tiendas.valores('CATIA')
        cruz_verde = grafico_tiendas.valores('CRUZ_VERDE')
        guacara = grafico_tiendas.valores('GUACARA')      
        guanare = grafico_tiendas.valores('GUANARE')      
        kapitana = grafico_tiendas.valores('KAPITANA')    
        maturin = grafico_tiendas.valores('MATURIN')      
        propatria = grafico_tiendas.valores('PROPATRIA')  
        upata = grafico_tiendas.valores('UPATA')
        valencia = grafico_tiendas.valores('VALENCIA')    
        valera = grafico_tiendas.valores('VALERA') 


        valores = {"grafico_tienda":{
                "BABILON":babilon[-1][0],
                "BARALT":baralt[-1][0],
                "CABUDARE":cabudare[-1][0],
                "CAGUA":cagua[-1][0],
                "CABIMAS":cabimas[-1][0],
                "CATIA": catia[-1][0],
                "CRUZ_VERDE":cruz_verde[-1][0],
                "GUACARA":guacara[-1][0],
                "GUANARE":guanare[-1][0],
                "KAPITANA":kapitana[-1][0],
                "MATURIN":maturin[-1][0],
                "PROPATRIA": propatria[-1][0],
                "UPATA": upata[-1][0],
                "VALENCIA": valencia[-1][0],
                "VALERA": valera[-1][0]
        }, "ventas_generales":{
            "USD":ventas[0][0],
            "BS": ventas[0][1],
            "CASHEA":ventas[0][2],
            "EFECTIVO":ventas[0][3]
            
            
        }
                   }
        return jsonify(valores)
    except  Exception as e:
        return jsonify({"error": str(e)}), 500

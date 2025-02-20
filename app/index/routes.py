from flask import Blueprint, render_template, request,redirect,session,flash,url_for, jsonify
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime,timedelta
import pandas as pd
from ..querys_sqlite_data import database


from ..querys_sqlite_data import conexion_sqlite



fecha = datetime.now()
fecha_diaria = fecha.date()

index_bp = Blueprint('index', __name__)

@index_bp.route('/',methods=['GET', 'POST'])
def index():
    enero = conexion_sqlite.consulta_ventas('2025-01-02','2025-01-31')

    
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

    ta = database.tasa(str(fecha_diaria),str(fecha_diaria))
    if ta == []:
        ta = database.tasa('2025-01-03','2025-01-03')
    
    grafico_mensuales = [enero[0][0]]
    if 'username' in session:

            return render_template('index.html',
                                username = session.get('username'),


                                total_ventas = ventas[0][0],
                                total_bs = ventas[0][1],
                                cashea_total = ventas[0][2],
                                efectivo_total = ventas[0][3],
                                tasa_dia = ta[0][6],
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

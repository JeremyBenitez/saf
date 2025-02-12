from flask import Blueprint, render_template
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime, timedelta
from ..querys_sqlite_data import cementerio
import calendar


tiendas_bp = Blueprint('tiendas', __name__)

fecha = datetime.now()
fecha_diaria = fecha.date()

fecha_hace_1Day = fecha_diaria - timedelta(days=1)
fecha_hace_2Day = fecha_diaria - timedelta(days=2)
fecha_hace_3Day = fecha_diaria - timedelta(days=3)
fecha_hace_4Day = fecha_diaria - timedelta(days=4)
fecha_hace_5Day = fecha_diaria - timedelta(days=5)
fecha_hace_6Day = fecha_diaria - timedelta(days=6)

ventasxtiendas = conexion_sqlite.index()

fechas = conexion_sqlite.consulta_fechas_prueba()


def semanas_del_mes(año, mes):
    semanas = calendar.monthcalendar(año, mes)
    return semanas

@tiendas_bp.route('/kapitana') 
def kapitana():
    contex = "Kapitana"
    kapitana = ventasxtiendas.tiendas(contex)
    
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    


    return render_template("tiendas.html", ventas_usd = kapitana[-1][1] ,
                                            ventas_bs =kapitana[-1][2] ,
                                            ventas_csh = kapitana[-1][3],
                                            venta_efe = kapitana[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)


@tiendas_bp.route('/baralt')
def baralt():
    contex = "Baralt"
    baralt = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    
    return render_template("tiendas.html", ventas_usd = baralt[-1][1] ,
                                            ventas_bs =baralt[-1][2] ,
                                            ventas_csh = baralt[-1][3],
                                            venta_efe = baralt[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)


@tiendas_bp.route('/cruzverde')
def cruz_verde():
    contex = "cruz_verde"
    cruz_verde = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    return render_template("tiendas.html",ventas_usd = cruz_verde[-1][1] ,
                                            ventas_bs =cruz_verde[-1][2] ,
                                            ventas_csh = cruz_verde[-1][3],
                                            venta_efe = cruz_verde[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)


@tiendas_bp.route('/catia')
def catia():
    contex = "catia"
    catia = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    return render_template("tiendas.html",ventas_usd = catia[-1][1] ,
                                            ventas_bs =catia[-1][2] ,
                                            ventas_csh = catia[-1][3],
                                            venta_efe = catia[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0
                           )
@tiendas_bp.route('/propatria')
def propatria():
    contex = "propatria"
    propatria = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    return render_template("tiendas.html",ventas_usd = propatria[-1][1] ,
                                            ventas_bs =propatria[-1][2] ,
                                            ventas_csh = propatria[-1][3],
                                            venta_efe = propatria[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)


@tiendas_bp.route('/guanare')
def guanare():
    contex = "guanare"
    guanare = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    return render_template("tiendas.html",ventas_usd = guanare[-1][1] ,
                                            ventas_bs =guanare[-1][2] ,
                                            ventas_csh = guanare[-1][3],
                                            venta_efe = guanare[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)
    

    
@tiendas_bp.route('/cagua')
def cagua():
    contex = "cagua"
    cagua = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    return render_template("tiendas.html",ventas_usd = cagua[-1][1] ,
                                            ventas_bs =cagua[-1][2] ,
                                            ventas_csh = cagua[-1][3],
                                            venta_efe = cagua[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)


@tiendas_bp.route('/barquisimeto')
def barquisimeto():
    contex = "babilon"
    barquisimeto = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    return render_template("tiendas.html",ventas_usd = barquisimeto[-1][1] ,
                                            ventas_bs =barquisimeto[-1][2] ,
                                            ventas_csh = barquisimeto[-1][3],
                                            venta_efe = barquisimeto[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)




@tiendas_bp.route('/guacara')
def guacara():
    contex = "guacara"
    guacara = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    return render_template("tiendas.html",ventas_usd = guacara[-1][1] ,
                                            ventas_bs =guacara[-1][2] ,
                                            ventas_csh = guacara[-1][3],
                                            venta_efe = guacara[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)
@tiendas_bp.route('/cabudare')
def cabudare():
    contex = "cabudare"
    cabudare = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    return render_template("tiendas.html",ventas_usd = cabudare[-1][1] ,
                                            ventas_bs =cabudare[-1][2] ,
                                            ventas_csh = cabudare[-1][3],
                                            venta_efe = cabudare[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)

@tiendas_bp.route('/upata')
def upata():
    contex = "upata"
    upata = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])
    return render_template("tiendas.html",ventas_usd = upata[-1][1] ,
                                            ventas_bs =upata[-1][2] ,
                                            ventas_csh = upata[-1][3],
                                            venta_efe = upata[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)


@tiendas_bp.route('/cabimas')
def cabimas():
    contex = "cabimas"
    cabimas = ventasxtiendas.tiendas(contex)

    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])

    return render_template("tiendas.html",ventas_usd = cabimas[-1][1] ,
                                            ventas_bs =cabimas[-1][2] ,
                                            ventas_csh = cabimas[-1][3],
                                            venta_efe = cabimas[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)


@tiendas_bp.route('/maturin')
def maturin():
    contex = "maturin"
    maturin = ventasxtiendas.tiendas(contex)

    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])

    return render_template("tiendas.html",ventas_usd = maturin[-1][1] ,
                                            ventas_bs =maturin[-1][2] ,
                                            ventas_csh = maturin[-1][3],
                                            venta_efe = maturin[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)

@tiendas_bp.route('/valera')
def valera():
    contex = "valera"
    valera = ventasxtiendas.tiendas(contex)

    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])

    return render_template("tiendas.html",ventas_usd = valera[-1][1] ,
                                            ventas_bs =valera[-1][2] ,
                                            ventas_csh = valera[-1][3],
                                            venta_efe = valera[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)



@tiendas_bp.route('/valencia')
def valencia():
    contex = "valencia"
    valencia = ventasxtiendas.tiendas(contex)

    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    daily_sales = [grafico_x_dia[-1]['V_USD']]
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,grafico_x_dia[5]['V_USD'])

    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,grafico_x_dia[4]['V_USD'])

    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,grafico_x_dia[3]['V_USD'])

    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,grafico_x_dia[2]['V_USD'])

    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,grafico_x_dia[1]['V_USD'])

    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,grafico_x_dia[0]['V_USD'])

    return render_template("tiendas.html",ventas_usd = valencia[-1][1] ,
                                            ventas_bs =valencia[-1][2] ,
                                            ventas_csh = valencia[-1][3],
                                            venta_efe = valencia[-1][4],
                                            daily_sales = daily_sales,
                                            weekly_sales = 0, 
                                            monthly_sales = 0)


@tiendas_bp.route('/cementerio')
def tiendacementerio():
    contex = "Tienda Cementerio"
    
    
    ventas = cementerio.cementerio()
    venta= ventas.ventas_cementerio(str(fecha_diaria),str(fecha_diaria))

    venta_1 = ventas.ventas_cementerio(str(fecha_hace_1Day),str(fecha_hace_1Day))
    venta_2 = ventas.ventas_cementerio(str(fecha_hace_2Day),str(fecha_hace_2Day))
    venta_3 = ventas.ventas_cementerio(str(fecha_hace_3Day),str(fecha_hace_3Day))
    venta_4 = ventas.ventas_cementerio(str(fecha_hace_4Day),str(fecha_hace_4Day))
    venta_5 = ventas.ventas_cementerio(str(fecha_hace_5Day),str(fecha_hace_5Day))
    venta_6 = ventas.ventas_cementerio(str(fecha_hace_6Day),str(fecha_hace_6Day))
    
    fechas = conexion_sqlite.consulta_fechas_prueba()
    
    daily_sales = [venta[0][0]]
    
    if str(fecha_diaria) >= fechas[0][1]:
        daily_sales.insert(0,venta_1[0][0])
        
    if str(fecha_diaria) >= fechas[0][2]:
        daily_sales.insert(0,venta_2[0][0])
        
    if str(fecha_diaria) >= fechas[0][3]:
        daily_sales.insert(0,venta_3[0][0])
        
    if str(fecha_diaria) >= fechas[0][4]:
        daily_sales.insert(0,venta_4[0][0])
        
    if str(fecha_diaria) >= fechas[0][5]:
        daily_sales.insert(0,venta_5[0][0])
    
    if str(fecha_diaria) >= fechas[0][6]:
        daily_sales.insert(0,venta_6[0][0])
        
    venta_semanas = cementerio.cementerio()
    s1 = venta_semanas.ventas_cementerio('2025-01-02','2025-01-05') 
    s2 = venta_semanas.ventas_cementerio('2025-01-06','2025-01-12') 
    s3 = venta_semanas.ventas_cementerio('2025-01-13','2025-01-19') 
    
    
    
    weekly_sales = []
    suma_bs_semana = 0 
    suma_efectivo_semanal = 0
    suma_semanal = 0
    
    return render_template("tiendas.html",
                           ventas_usd_mensuales = 00,
                           ventas_bs_mensuales =00,
                           ventas_csh_mensuales = 0,
                           ventas_efectivo_mensuales =0 ,
                           venta_efe = 0,
                           ventas_csh = 0,
                           ventas_bs = venta[0][1],
                           ventas_usd = venta[0][0],
                           daily_sales = daily_sales,
                           weekly_sales = weekly_sales,
                           monthly_sales = 0,
                           muestra_ventas = suma_semanal,
                           semana_bs = suma_bs_semana,
                           semana_csh = 0,
                           semana_efe = suma_efectivo_semanal,
                           text=contex)
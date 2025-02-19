from flask import Blueprint, render_template
from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime, timedelta
from ..querys_sqlite_data import cementerio
from .semanas import semanas_variadas,año,meses
from .meses import mes_init,mes_fin


tiendas_bp = Blueprint('tiendas', __name__)

fecha = datetime.now()
fecha_diaria = fecha.date()

mes_date = fecha.date().month
mes_actual = f'{mes_date:02d}'

fecha_hace_1Day = fecha_diaria - timedelta(days=1)
fecha_hace_2Day = fecha_diaria - timedelta(days=2)
fecha_hace_3Day = fecha_diaria - timedelta(days=3)
fecha_hace_4Day = fecha_diaria - timedelta(days=4)
fecha_hace_5Day = fecha_diaria - timedelta(days=5)
fecha_hace_6Day = fecha_diaria - timedelta(days=6)

ventasxtiendas = conexion_sqlite.index()

fechas = conexion_sqlite.consulta_fechas_prueba()


@tiendas_bp.route('/kapitana') 
def kapitana():
    contex = "Kapitana"
    kapitana = ventasxtiendas.tiendas(contex)
    
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])


    #SECCION DE SEMANAS
    
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente

# Crear listas para cada tipo de dato (USD, CSH, BS, EFEC) usando comprensión de listas
    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}

    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]

    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]
    
    
    #SECCION MENSUAL////////////////////
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))

    return render_template("tiendas.html", ventas_usd = kapitana[-1][1] ,
                                            ventas_bs =kapitana[-1][2] ,
                                            ventas_csh = kapitana[-1][3],
                                            venta_efe = kapitana[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual) ,
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/baralt')
def baralt():
    contex = "Baralt"
    baralt = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html", ventas_usd = baralt[-1][1] ,
                                            ventas_bs =baralt[-1][2] ,
                                            ventas_csh = baralt[-1][3],
                                            venta_efe = baralt[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/cruzverde')
def cruz_verde():
    contex = "cruz_verde"
    cruz_verde = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = cruz_verde[-1][1] ,
                                            ventas_bs =cruz_verde[-1][2] ,
                                            ventas_csh = cruz_verde[-1][3],
                                            venta_efe = cruz_verde[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/catia')
def catia():
    contex = "catia"
    catia = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = catia[-1][1] ,
                                            ventas_bs =catia[-1][2] ,
                                            ventas_csh = catia[-1][3],
                                            venta_efe = catia[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)
@tiendas_bp.route('/propatria')
def propatria():
    contex = "propatria"
    propatria = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = propatria[-1][1] ,
                                            ventas_bs =propatria[-1][2] ,
                                            ventas_csh = propatria[-1][3],
                                            venta_efe = propatria[-1][4],
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/guanare')
def guanare():
    contex = "guanare"
    guanare = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = guanare[-1][1] ,
                                            ventas_bs =guanare[-1][2] ,
                                            ventas_csh = guanare[-1][3],
                                            venta_efe = guanare[-1][4],
                                             
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)
    

    
@tiendas_bp.route('/cagua')
def cagua():
    contex = "cagua"
    cagua = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = cagua[-1][1] ,
                                            ventas_bs =cagua[-1][2] ,
                                            ventas_csh = cagua[-1][3],
                                            venta_efe = cagua[-1][4],
                                             
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/barquisimeto')
def barquisimeto():
    contex = "babilon"
    barquisimeto = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = barquisimeto[-1][1] ,
                                            ventas_bs =barquisimeto[-1][2] ,
                                            ventas_csh = barquisimeto[-1][3],
                                            venta_efe = barquisimeto[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)




@tiendas_bp.route('/guacara')
def guacara():
    contex = "guacara"
    guacara = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = guacara[-1][1] ,
                                            ventas_bs =guacara[-1][2] ,
                                            ventas_csh = guacara[-1][3],
                                            venta_efe = guacara[-1][4],
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)
@tiendas_bp.route('/cabudare')
def cabudare():
    contex = "cabudare"
    cabudare = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = cabudare[-1][1] ,
                                            ventas_bs =cabudare[-1][2] ,
                                            ventas_csh = cabudare[-1][3],
                                            venta_efe = cabudare[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)

@tiendas_bp.route('/upata')
def upata():
    contex = "upata"
    upata = ventasxtiendas.tiendas(contex)
    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = upata[-1][1] ,
                                            ventas_bs =upata[-1][2] ,
                                            ventas_csh = upata[-1][3],
                                            venta_efe = upata[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/cabimas')
def cabimas():
    contex = "cabimas"
    cabimas = ventasxtiendas.tiendas(contex)

    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))



    return render_template("tiendas.html",ventas_usd = cabimas[-1][1] ,
                                            ventas_bs =cabimas[-1][2] ,
                                            ventas_csh = cabimas[-1][3],
                                            venta_efe = cabimas[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/maturin')
def maturin():
    contex = "maturin"
    maturin = ventasxtiendas.tiendas(contex)

    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))



    return render_template("tiendas.html",ventas_usd = maturin[-1][1] ,
                                            ventas_bs =maturin[-1][2] ,
                                            ventas_csh = maturin[-1][3],
                                            venta_efe = maturin[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)

@tiendas_bp.route('/valera')
def valera():
    contex = "valera"
    valera = ventasxtiendas.tiendas(contex)

    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))



    return render_template("tiendas.html",ventas_usd = valera[-1][1] ,
                                            ventas_bs =valera[-1][2] ,
                                            ventas_csh = valera[-1][3],
                                            venta_efe = valera[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)



@tiendas_bp.route('/valencia')
def valencia():
    contex = "valencia"
    valencia = ventasxtiendas.tiendas(contex)

    grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

   #GRAFICOS DIARIOS 
    daily_sales = [grafico_x_dia[-1]['V_USD']]
    # Iterar sobre los índices y fechas
    for i in range(6, 0, -1):  # Iterar del índice 6 al 1 (de forma descendente)
        if str(fecha_diaria) >= fechas[0][i]:
            daily_sales.insert(0, grafico_x_dia[i - 1]['V_USD'])
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
        (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
        for semana in range(5)
    ]

    # Iterar sobre los datos en grafico_mensuales
    for j in grafico_mensuales:
        fecha_actual = j['FECHA']

        # Comparar la fecha con los rangos de semanas
        for i, (inicio, fin) in enumerate(rango_semanas, 1):
            if inicio <= fecha_actual <= fin:
                semanas[i].append((j['V_USD'], j['V_CSH'], j['V_BS'], j['V_EFEC']))
                break  # Romper el bucle una vez que se encuentra la semana correspondiente


    usds_semanal = {semana: [response[0] for response in semanas[semana]] for semana in range(1, 6)}
    csh_semanal = {semana: [response[1] for response in semanas[semana]] for semana in range(1, 6)}
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


    suma_semanal_csh =[sum(csh_semanal[1]), sum(csh_semanal[2]),sum(csh_semanal[3]),sum(csh_semanal[4]),sum(csh_semanal[5])]
    suma_semanal_bs = [sum(bs_semanal[1]), sum(bs_semanal[2]),sum(bs_semanal[3]),sum(bs_semanal[4]),sum(bs_semanal[5])]
    suma_semanal_efectivo = [sum(efe_semanal[1]), sum(efe_semanal[2]),sum(efe_semanal[3]),sum(efe_semanal[4]),sum(efe_semanal[5])]

    
    
    #SECCION MENSUAL
    
    meses = {month: [] for month in range(1, 13)}  # Diccionario de meses (1 a 12)

    for valores in grafico_mensuales:
        # Convertir la fecha a un objeto datetime
        fecha = datetime.strptime(valores['FECHA'], '%Y-%m-%d')
        # Obtener el número de mes correspondiente
        mes = fecha.month
        # Agregar los valores al mes correspondiente en el diccionario
        meses[mes].append((valores['V_USD'], valores['V_CSH'], valores['V_BS'], valores['V_EFEC']))

    # Crear listas para cada mes (USD, CSH, BS, EFEC) usando comprensión de listas
    usds = {month: [tupla[0] for tupla in meses[month]] for month in range(1, 13)}
    csh = {month: [tupla[1] for tupla in meses[month]] for month in range(1, 13)}
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2])]
    bs_mensual = [sum(bs[1]) + sum(bs[2])]
    csh_mensual = [sum(csh[1]) + sum(csh[2])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = valencia[-1][1] ,
                                            ventas_bs =valencia[-1][2] ,
                                            ventas_csh = valencia[-1][3],
                                            venta_efe = valencia[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                            suma_semanal_csh = sum(suma_semanal_csh),
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh =sum(csh_mensual),
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = daily_sales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


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
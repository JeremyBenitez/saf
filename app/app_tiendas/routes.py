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

tienda_cementerio = cementerio.index()

@tiendas_bp.route('/kapitana') 
def kapitana():
    contex = "Kapitana"
    kapitana = ventasxtiendas.tiendas(contex)
    

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día


    #SECCION DE SEMANAS
    
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/baralt')
def baralt():
    contex = "Baralt"
    baralt = ventasxtiendas.tiendas(contex)

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/cruzverde')
def cruz_verde():
    contex = "cruz_verde"
    cruz_verde = ventasxtiendas.tiendas(contex)

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/catia')
def catia():
    contex = "catia"
    catia = ventasxtiendas.tiendas(contex)

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)
@tiendas_bp.route('/propatria')
def propatria():
    contex = "propatria"
    propatria = ventasxtiendas.tiendas(contex)


    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/guanare')
def guanare():
    contex = "guanare"
    guanare = ventasxtiendas.tiendas(contex)

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)
    

    
@tiendas_bp.route('/cagua')
def cagua():
    contex = "cagua"
    cagua = ventasxtiendas.tiendas(contex)

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/barquisimeto')
def barquisimeto():
    contex = "babilon"
    barquisimeto = ventasxtiendas.tiendas(contex)

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)




@tiendas_bp.route('/guacara')
def guacara():
    contex = "guacara"
    guacara = ventasxtiendas.tiendas(contex)

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)
@tiendas_bp.route('/cabudare')
def cabudare():
    contex = "cabudare"
    cabudare = ventasxtiendas.tiendas(contex)

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)

@tiendas_bp.route('/upata')
def upata():
    contex = "upata"
    upata = ventasxtiendas.tiendas(contex)

    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/cabimas')
def cabimas():
    contex = "cabimas"
    cabimas = ventasxtiendas.tiendas(contex)


    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/maturin')
def maturin():
    contex = "maturin"
    maturin = ventasxtiendas.tiendas(contex)


    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)

@tiendas_bp.route('/valera')
def valera():
    contex = "valera"
    valera = ventasxtiendas.tiendas(contex)


    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)



@tiendas_bp.route('/valencia')
def valencia():
    contex = "valencia"
    valencia = ventasxtiendas.tiendas(contex)


    grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    csh_mensual = [sum(csh[1]) + sum(csh[2])+ sum(csh[3])+ sum(csh[4])+ sum(csh[5])+ sum(csh[6])+ sum(csh[7])+ sum(csh[8])+ sum(csh[9])+ sum(csh[10])+ sum(csh[11])+ sum(csh[12])]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
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
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)


@tiendas_bp.route('/cementerio')
def tiendacementerio():
    contex = "VENTAS"
    cementerio = tienda_cementerio.tiendas(contex)


    grafico_mensuales = tienda_cementerio.tienda_times(contex,mes_init[0],mes_fin[11])

# Obtener la fecha actual y calcular el inicio y fin de la semana
    fecha_sistema = datetime.now().date()  # Fecha del día actual
    inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
    fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

    # Lista para el rango de fechas de la semana (de lunes a domingo)
    fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

    # Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
    ventas_semanales = [None] * 7

    # Llenar las ventas semanales con los datos disponibles
    for registro in grafico_mensuales:
        fecha = registro['FECHA']
        if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
            indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
            ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día
    
    

    #SECCION DE SEMANAS
    semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
    rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
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
    bs_semanal = {semana: [response[2] for response in semanas[semana]] for semana in range(1, 6)}
    efe_semanal = {semana: [response[3] for response in semanas[semana]] for semana in range(1, 6)}
    
    #LISTA GRAFICO SEMANAL
    weekly_sales = [sum(usds_semanal[1]), sum(usds_semanal[2]), sum(usds_semanal[3]),sum(usds_semanal[4]),sum(usds_semanal[5])]


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
    bs = {month: [tupla[2] for tupla in meses[month]] for month in range(1, 13)}
    efe = {month: [tupla[3] for tupla in meses[month]] for month in range(1, 13)}

    usd_mensual = [sum(usds[1])+ sum(usds[2]) + sum(usds[3])+ sum(usds[4])+ sum(usds[5])+ sum(usds[6])+ sum(usds[7])+ sum(usds[8])+ sum(usds[8])+ sum(usds[10])+ sum(usds[11])+ sum(usds[12])]
    bs_mensual = [sum(bs[1]) + sum(bs[2]) + sum(bs[3])+ sum(bs[4])+ sum(bs[5])+ sum(bs[6])+ sum(bs[7])+ sum(bs[8])+ sum(bs[9])+ sum(bs[10])+ sum(bs[11])+ sum(bs[12]) ]
    efect_mensual = [sum(efe[1]) + sum(efe[2])+ sum(efe[3])+ sum(efe[4])+ sum(efe[5])+ sum(efe[6])+ sum(efe[7])+ sum(efe[8])+ sum(efe[9])+ sum(efe[10])+ sum(efe[11])+ sum(efe[12])]
    
    #LISTA DEL GRAFICO MENSUAL
    monthly_sales = []

    for i in range(1, 13):
        if str(fecha_diaria) >= mes_fin[i - 1]:
            monthly_sales.append(sum(usds[i]))


    return render_template("tiendas.html",ventas_usd = cementerio[-1][1] ,
                                            ventas_csh = 00,
                                            ventas_bs =cementerio[-1][2] ,
                                            venta_efe = cementerio[-1][4],
                                            
                                            suma_semanal = sum(weekly_sales),
                                             suma_semanal_csh = 00,
                                            suma_semanal_bs = sum(suma_semanal_bs),
                                            suma_semanal_efectivo = sum(suma_semanal_efectivo),
                                            
                                            suma_mensual=sum(usd_mensual),
                                            suma_mensual_bs =sum(bs_mensual),
                                            suma_mensual_csh = 00,
                                            suma_mensual_efec =sum(efect_mensual),
                                            
                                            
                                            daily_sales = ventas_semanales,
                                            weekly_sales = weekly_sales, 
                                            monthly_sales = monthly_sales)
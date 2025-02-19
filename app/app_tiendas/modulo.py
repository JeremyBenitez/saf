from ..querys_sqlite_data import conexion_sqlite
from datetime import datetime, timedelta
from ..querys_sqlite_data import cementerio
from .semanas import semanas_variadas,año,meses
from .meses import mes_init,mes_fin



fecha = datetime.now()
fecha_diaria = fecha.date()

mes_date = fecha.date().month
mes_actual = f'{mes_date:02d}'


fecha_hace_6Day = fecha_diaria - timedelta(days=6)

ventasxtiendas = conexion_sqlite.index()

fechas = conexion_sqlite.consulta_fechas_prueba()



contex = "Kapitana"


kapitana = ventasxtiendas.tiendas(contex)
    
grafico_x_dia = ventasxtiendas.tienda_times(contex,str(fecha_hace_6Day),str(fecha_diaria))

grafico_mensuales = ventasxtiendas.tienda_times(contex,mes_init[0],mes_fin[11])

valores_enero = ventasxtiendas.tienda_times(contex, mes_init[0], mes_fin[1])
    
        
    
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
    
    
    
valor_mensual = []
lista_cashea_mensual = []
lista_bs_mensual = []
lista_efe_mensual = []
for i in grafico_mensuales:
        valor_mensual.append(i['V_USD'])
        lista_cashea_mensual.append(i['V_CSH'])
        lista_bs_mensual.append(i['V_BS'])
        lista_efe_mensual.append(i['V_EFEC'])
        
        
semana1 = []
semana2 = []
semana3= []
semana4 = []
semana5 =[]
lista_cashea_semanal = []
lista_bs_semanal = []
lista_efe_semanal = []
valor_semanal = []
for j in grafico_mensuales:
        if j['FECHA'] >= f'{año}-{mes_actual}-{semanas_variadas[0][0]:02d}' and j['FECHA'] <= f'{año}-{mes_actual}-{semanas_variadas[0][-1]:02d}':
            semana1.append(j['V_USD'])
        elif j['FECHA'] >= f'{año}-{mes_actual}-{semanas_variadas[1][0]:02d}' and j['FECHA'] <= f'{año}-{mes_actual}-{semanas_variadas[1][-1]:02d}':
            semana2.append(j['V_USD'])
        elif j['FECHA'] >= f'{año}-{mes_actual}-{semanas_variadas[2][0]:02d}' and j['FECHA'] <= f'{año}-{mes_actual}-{semanas_variadas[2][-1]:02d}':
            semana3.append(j['V_USD'])
        elif j['FECHA'] >= f'{año}-{mes_actual}-{semanas_variadas[3][0]:02d}' and j['FECHA'] <= f'{año}-{mes_actual}-{semanas_variadas[3][-1]:02d}':
            semana4.append(j['V_USD'])
        elif j['FECHA'] >= f'{año}-{mes_actual}-{semanas_variadas[4][0]:02d}' and j['FECHA'] <= f'{año}-{mes_actual}-{semanas_variadas[4][-1]:02d}':
            semana5.append(j['V_USD'])    

valor_semanal.append((semana1))
valor_semanal.append((semana2))
valor_semanal.append((semana3))
valor_semanal.append((semana4))
valor_semanal.append((semana5))
weekly_sales = [sum(valor_semanal[0]), sum(valor_semanal[1]), sum(valor_semanal[2]),sum(valor_semanal[3]),sum(valor_semanal[4])]

monthly_sales = []

    
    
lista_cashea = []
lista_bs = []
lista_efe = []
for k in grafico_mensuales:
    lista_cashea.append(k['V_CSH'])
    lista_bs.append(k['V_BS'])
    lista_efe.append(k['V_EFEC'])
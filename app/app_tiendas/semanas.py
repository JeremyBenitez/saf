import calendar
from datetime import datetime

fecha = datetime.now()
mes_date = fecha.date().month
mes_actual = f'{mes_date:02d}'


def semanas_del_mes(año, mes):
    semanas = calendar.monthcalendar(año, mes)
    return semanas

año = 2025
mes = [1,2,3,4,5,6,7,8,9,10,11,12]

semanas = []
meses = []
for i in mes:
    meses.append(i)
    count_semanas = semanas_del_mes(año,i)
    semanas.append(count_semanas)


def conat(a):
    if str(mes_actual) == f'{meses[a]:02d}':
        semanas_activas = semanas[a]
    else:
        semanas_activas = []
    
    return semanas_activas

semanas_variadas = conat(int(mes_date) - 1)


print(semanas_variadas)
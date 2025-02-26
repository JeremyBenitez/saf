import calendar

data = [
  {
    'ID': 45,
    'V_USD': 10534.43484560979,
    'V_BS': 610681.1879999983,
    'V_CSH': 2317.0434707607383,
    'V_EFEC': 3142.1682663446613,
    'n_trasacciones': 2219,
    'FECHA': '2025-02-01'
  },
  {
    'ID': 46,
    'V_USD': 6121.123298257719,
    'V_BS': 354841.5175999989,
    'V_CSH': 1392.0605485596,
    'V_EFEC': 2563.0892254614455,
    'n_trasacciones': 1308,
    'FECHA': '2025-02-02'
  },
  {
    'ID': 47,
    'V_USD': 4651.414209445582,
    'V_BS': 271828.6464000005,
    'V_CSH': 796.7973990417522,
    'V_EFEC': 2040.4914647501714,
    'n_trasacciones': 1181,
    'FECHA': '2025-02-03'
  },
  {
    'ID': 48,
    'V_USD': 4494.783416467373,
    'V_BS': 263124.6211999995,
    'V_CSH': 811.3587290741374,
    'V_EFEC': 1779.4137615305776,
    'n_trasacciones': 1080,
    'FECHA': '2025-02-04'
  },
  {
    'ID': 49,
    'V_USD': 6051.362469807802,
    'V_BS': 355759.59960000095,
    'V_CSH': 1013.6535125021261,
    'V_EFEC': 1814.9992379656403,
    'n_trasacciones': 1394,
    'FECHA': '2025-02-05'
  },
  {
    'ID': 50,
    'V_USD': 4702.625368314836,
    'V_BS': 279618.1044000006,
    'V_CSH': 594.6671712075346,
    'V_EFEC': 1866.2197040026913,
    'n_trasacciones': 1151,
    'FECHA': '2025-02-06'
  },
  {
    'ID': 51,
    'V_USD': 6623.570681742607,
    'V_BS': 398341.54080000316,
    'V_CSH': 1415.105254406385,
    'V_EFEC': 2214.328593282341,
    'n_trasacciones': 1440,
    'FECHA': '2025-02-07'
  },
  {
    'ID': 52,
    'V_USD': 8518.556827402741,
    'V_BS': 512306.00760000624,
    'V_CSH': 1776.1119055537083,
    'V_EFEC': 3395.262447622215,
    'n_trasacciones': 1673,
    'FECHA': '2025-02-08'
  },
  {
    'ID': 53,
    'V_USD': 7159.361449950118,
    'V_BS': 430563.9976000046,
    'V_CSH': 1783.4900232790158,
    'V_EFEC': 2867.7566943797797,
    'n_trasacciones': 1376,
    'FECHA': '2025-02-09'
  },
  {
    'ID': 54,
    'V_USD': 4383.178836748177,
    'V_BS': 265269.9831999994,
    'V_CSH': 754.4201916721744,
    'V_EFEC': 1776.4778189028425,
    'n_trasacciones': 855,
    'FECHA': '2025-02-10'
  },
  {
    'ID': 55,
    'V_USD': 5186.940000000002,
    'V_BS': 314017.3475999994,
    'V_CSH': 1120.740171787248,
    'V_EFEC': 1759.2581830194918,
    'n_trasacciones': 1019,
    'FECHA': '2025-02-11'
  },
  {
    'ID': 56,
    'V_USD': 4438.381622153037,
    'V_BS': 270874.43040000094,
    'V_CSH': 854.7489759134854,
    'V_EFEC': 1441.0350188431923,
    'n_trasacciones': 911,
    'FECHA': '2025-02-12'
  },
  {
    'ID': 57,
    'V_USD': 7338.946568867159,
    'V_BS': 450244.37199999695,
    'V_CSH': 1648.9753871230648,
    'V_EFEC': 2573.6277881010597,
    'n_trasacciones': 1629,
    'FECHA': '2025-02-13'
  },
  {
    'ID': 58,
    'V_USD': 9605.737644775156,
    'V_BS': 593826.7012,
    'V_CSH': 2464.295535425429,
    'V_EFEC': 3011.1092267874474,
    'n_trasacciones': 1784,
    'FECHA': '2025-02-14'
  },
  {
    'ID': 59,
    'V_USD': 11817.553665480425,
    'V_BS': 730561.1675999997,
    'V_CSH': 2967.8610482044633,
    'V_EFEC': 2805.942542866386,
    'n_trasacciones': 2446,
    'FECHA': '2025-02-15'
  },
  {
    'ID': 60,
    'V_USD': 7292.615833063729,
    'V_BS': 450829.5108000008,
    'V_CSH': 1905.3861209964414,
    'V_EFEC': 1556.9406535101912,
    'n_trasacciones': 1488,
    'FECHA': '2025-02-16'
  },
  {
    'ID': 61,
    'V_USD': 6181.534035766075,
    'V_BS': 383687.81760000135,
    'V_CSH': 1241.7193491219596,
    'V_EFEC': 2173.9769292734013,
    'n_trasacciones': 1392,
    'FECHA': '2025-02-17'
  },
  {
    'ID': 62,
    'V_USD': 4915.53138164251,
    'V_BS': 305254.4987999987,
    'V_CSH': 931.6504025764895,
    'V_EFEC': 1259.775342995169,
    'n_trasacciones': 1242,
    'FECHA': '2025-02-18'
  },
  {
    'ID': 63,
    'V_USD': 5684.839684786108,
    'V_BS': 353483.33159999986,
    'V_CSH': 949.3454486973301,
    'V_EFEC': 1889.8025667417176,
    'n_trasacciones': 1318,
    'FECHA': '2025-02-19'
  },
  {
    'ID': 64,
    'V_USD': 5887.036000639895,
    'V_BS': 367998.62040000036,
    'V_CSH': 893.4317709166534,
    'V_EFEC': 1764.7784354503274,
    'n_trasacciones': 1236,
    'FECHA': '2025-02-20'
  },
  {
    'ID': 65,
    'V_USD': 6516.229438380001,
    'V_BS': 411890.8627999974,
    'V_CSH': 1457.1256130359122,
    'V_EFEC': 1624.8383863312765,
    'n_trasacciones': 1404,
    'FECHA': '2025-02-21'
  },
  {
    'ID': 66,
    'V_USD': 11393.076260085441,
    'V_BS': 720156.3503999966,
    'V_CSH': 2456.2629330802088,
    'V_EFEC': 3124.51190001582,
    'n_trasacciones': 2383,
    'FECHA': '2025-02-22'
  },
  {
    'ID': 67,
    'V_USD': 6414.135858250277,
    'V_BS': 405437.52759999793,
    'V_CSH': 1371.5562411010915,
    'V_EFEC': 2391.4273058060435,
    'n_trasacciones': 1465,
    'FECHA': '2025-02-23'
  },
  {
    'ID': 68,
    'V_USD': 4899.6735278347305,
    'V_BS': 310688.29840000015,
    'V_CSH': 788.3111496609368,
    'V_EFEC': 1996.1033086263994,
    'n_trasacciones': 1094,
    'FECHA': '2025-02-24'
  },
  {
    'ID': 69,
    'V_USD': 0,
    'V_BS': 0,
    'V_CSH': 0,
    'V_EFEC': 0,
    'n_trasacciones': 0,
    'FECHA': '2025-02-25'
  }
]
from datetime import datetime, timedelta

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



# Obtener la fecha actual y calcular el inicio y fin de la semana
semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas

rango_semanas = [
    (f'{año}-{mes_actual}-{min([d for d in semana if d > 0]):02d}', 
     f'{año}-{mes_actual}-{max([d for d in semana if d > 0]):02d}')
     
    for semana in semanas_variadas if any(d > 0 for d in semana)
]


    # Iterar sobre los datos en grafico_mensuales
for j in data:
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


print(weekly_sales)
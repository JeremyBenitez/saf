import calendar

data  =[
  {
    'ID': 1,
    'V_USD': 2032.8664462809913,
    'V_BS': 105770.04119999998,
    'V_CSH': 127.6048433596,
    'V_EFEC': 1231.5340226792237,
    'n_trasacciones': 401,
    'FECHA': '2025-01-02'
  },
  {
    'ID': 2,
    'V_USD': 2259.7600989157318,
    'V_BS': 118795.58839999957,
    'V_CSH': 332.026440935895,
    'V_EFEC': 1050.009518736922,
    'n_trasacciones': 478,
    'FECHA': '2025-01-03'
  },
  {
    'ID': 3,
    'V_USD': 2290.560007608901,
    'V_BS': 120414.73959999993,
    'V_CSH': 220.215902606049,
    'V_EFEC': 902.6975993912879,
    'n_trasacciones': 497,
    'FECHA': '2025-01-04'
  },
  {
    'ID': 4,
    'V_USD': 1740.7718622788661,
    'V_BS': 91512.37679999994,
    'V_CSH': 148.06733878638,
    'V_EFEC': 1003.439832604147,
    'n_trasacciones': 441,
    'FECHA': '2025-01-05'
  },
  {
    'ID': 5,
    'V_USD': 2192.6087426288764,
    'V_BS': 115265.44159999953,
    'V_CSH': 243.000570667681,
    'V_EFEC': 995.4123035952064,
    'n_trasacciones': 564,
    'FECHA': '2025-01-06'
  },
  {
    'ID': 6,
    'V_USD': 1731.5012110922476,
    'V_BS': 91786.87919999995,
    'V_CSH': 234.739860403697,
    'V_EFEC': 1032.7812865497076,
    'n_trasacciones': 342,
    'FECHA': '2025-01-07'
  },
  {
    'ID': 7,
    'V_USD': 2313.9213340870547,
    'V_BS': 122799.8051999997,
    'V_CSH': 259.514980214811,
    'V_EFEC': 889.303998492557,
    'n_trasacciones': 400,
    'FECHA': '2025-01-08'
  },
  {
    'ID': 8,
    'V_USD': 992.1146021021023,
    'V_BS': 52859.86600000006,
    'V_CSH': 63.5073198198198,
    'V_EFEC': 648.934954954955,
    'n_trasacciones': 207,
    'FECHA': '2025-01-09'
  },
  {
    'ID': 9,
    'V_USD': 970.5329025069638,
    'V_BS': 52263.19679999995,
    'V_CSH': 193.630640668524,
    'V_EFEC': 411.9721522748375,
    'n_trasacciones': 172,
    'FECHA': '2025-01-10'
  },
  {
    'ID': 10,
    'V_USD': 1638.3960631383477,
    'V_BS': 88227.62800000004,
    'V_CSH': 207.361559888579,
    'V_EFEC': 662.0001188486539,
    'n_trasacciones': 347,
    'FECHA': '2025-01-11'
  },
  {
    'ID': 11,
    'V_USD': 2483.0583026926656,
    'V_BS': 133712.68960000004,
    'V_CSH': 739.167873723305,
    'V_EFEC': 776.5069860724234,
    'n_trasacciones': 298,
    'FECHA': '2025-01-12'
  },
  {
    'ID': 12,
    'V_USD': 1641.3750120705668,
    'V_BS': 88388.04439999996,
    'V_CSH': 274.429340761374,
    'V_EFEC': 940.0059944289694,
    'n_trasacciones': 353,
    'FECHA': '2025-01-13'
  },
  {
    'ID': 13,
    'V_USD': 1586.986139569414,
    'V_BS': 85506.81319999998,
    'V_CSH': 191.356533036377,
    'V_EFEC': 550.3428210838902,
    'n_trasacciones': 268,
    'FECHA': '2025-01-14'
  },
  {
    'ID': 27,
    'V_USD': 1359.0120163083775,
    'V_BS': 73332.28839999995,
    'V_CSH': 195.20200148257967,
    'V_EFEC': 381.9990363232024,
    'n_trasacciones': 313,
    'FECHA': '2025-01-15'
  },
  {
    'ID': 28,
    'V_USD': 1923.1974324075773,
    'V_BS': 104564.24440000005,
    'V_CSH': 415.45852492183195,
    'V_EFEC': 428.99710869965065,
    'n_trasacciones': 476,
    'FECHA': '2025-01-16'
  },
  {
    'ID': 29,
    'V_USD': 2754.2418480642814,
    'V_BS': 150822.28360000043,
    'V_CSH': 380.22078159240317,
    'V_EFEC': 543.0009934258584,
    'n_trasacciones': 543,
    'FECHA': '2025-01-17'
  },
  {
    'ID': 30,
    'V_USD': 3113.3417092768445,
    'V_BS': 170486.5920000008,
    'V_CSH': 569.2116508400292,
    'V_EFEC': 593.0032651570489,
    'n_trasacciones': 736,
    'FECHA': '2025-01-18'
  },
  {
    'ID': 31,
    'V_USD': 2001.1900146092041,
    'V_BS': 109585.16520000028,
    'V_CSH': 455.31884587289994,
    'V_EFEC': 528.9938860482102,
    'n_trasacciones': 366,
    'FECHA': '2025-01-19'
  },
  {
    'ID': 32,
    'V_USD': 2350.92875614642,
    'V_BS': 129089.49799999988,
    'V_CSH': 527.6942269167729,
    'V_EFEC': 647.1154398105991,
    'n_trasacciones': 372,
    'FECHA': '2025-01-20'
  },
  {
    'ID': 34,
    'V_USD': 1328.1987343153298,
    'V_BS': 73037.6483999999,
    'V_CSH': 163.25950172758684,
    'V_EFEC': 489.99539552645933,
    'n_trasacciones': 292,
    'FECHA': '2025-01-21'
  },
  {
    'ID': 35,
    'V_USD': 1343.1352622061481,
    'V_BS': 74275.38000000009,
    'V_CSH': 278.78987341772154,
    'V_EFEC': 333.0014321880651,
    'n_trasacciones': 278,
    'FECHA': '2025-01-22'
  },
  {
    'ID': 36,
    'V_USD': 1667.6296054519364,
    'V_BS': 92987.02679999996,
    'V_CSH': 265.51614060258254,
    'V_EFEC': 641.994949784792,
    'n_trasacciones': 343,
    'FECHA': '2025-01-23'
  },
  {
    'ID': 37,
    'V_USD': 1717.3109523809526,
    'V_BS': 96650.26040000012,
    'V_CSH': 221.6636460554371,
    'V_EFEC': 575.9372139303483,
    'n_trasacciones': 360,
    'FECHA': '2025-01-24'
  },
  {
    'ID': 38,
    'V_USD': 2862.8581520966586,
    'V_BS': 161121.6567999998,
    'V_CSH': 518.0117270788912,
    'V_EFEC': 1033.7038734896944,
    'n_trasacciones': 547,
    'FECHA': '2025-01-25'
  },
  {
    'ID': 39,
    'V_USD': 1317.1962828713577,
    'V_BS': 74131.8068000001,
    'V_CSH': 128.03127221037667,
    'V_EFEC': 696.9957853589196,
    'n_trasacciones': 311,
    'FECHA': '2025-01-26'
  },
  {
    'ID': 40,
    'V_USD': 1348.751350397176,
    'V_BS': 76406.76400000007,
    'V_CSH': 130.47413945278024,
    'V_EFEC': 689.9814015887025,
    'n_trasacciones': 276,
    'FECHA': '2025-01-27'
  },
  {
    'ID': 41,
    'V_USD': 1370.3931129088987,
    'V_BS': 77920.55239999994,
    'V_CSH': 287.2599366865986,
    'V_EFEC': 509.697931762223,
    'n_trasacciones': 480,
    'FECHA': '2025-01-28'
  },
  {
    'ID': 42,
    'V_USD': 1565.2477207678878,
    'V_BS': 89688.69439999979,
    'V_CSH': 245.33420593368237,
    'V_EFEC': 480.07202792321124,
    'n_trasacciones': 402,
    'FECHA': '2025-01-29'
  },
  {
    'ID': 43,
    'V_USD': 1404.6983516292037,
    'V_BS': 80615.63840000011,
    'V_CSH': 297.86269384910264,
    'V_EFEC': 311.7555811116919,
    'n_trasacciones': 321,
    'FECHA': '2025-01-30'
  },
  {
    'ID': 44,
    'V_USD': 1518.236494738657,
    'V_BS': 88012.1696000001,
    'V_CSH': 252.08055890978096,
    'V_EFEC': 321.8467069173711,
    'n_trasacciones': 343,
    'FECHA': '2025-01-31'
  },
  {
    'ID': 45,
    'V_USD': 3330.6167327928247,
    'V_BS': 193075.852,
    'V_CSH': 560.7957564257374,
    'V_EFEC': 750.9192133862343,
    'n_trasacciones': 685,
    'FECHA': '2025-02-01'
  },
  {
    'ID': 46,
    'V_USD': 2175.3197653958946,
    'V_BS': 126103.28680000005,
    'V_CSH': 374.65482145937557,
    'V_EFEC': 662.0091357598759,
    'n_trasacciones': 425,
    'FECHA': '2025-02-02'
  },
  {
    'ID': 47,
    'V_USD': 2263.4370978781662,
    'V_BS': 132275.26400000026,
    'V_CSH': 289.2260438056126,
    'V_EFEC': 878.9278986995207,
    'n_trasacciones': 407,
    'FECHA': '2025-02-03'
  },
  {
    'ID': 48,
    'V_USD': 2211.0004236419545,
    'V_BS': 129431.9648,
    'V_CSH': 470.63887939870176,
    'V_EFEC': 644.0330440724291,
    'n_trasacciones': 477,
    'FECHA': '2025-02-04'
  },
  {
    'ID': 49,
    'V_USD': 1616.4995611498553,
    'V_BS': 95034.00919999993,
    'V_CSH': 283.86375233883314,
    'V_EFEC': 425.08151726484084,
    'n_trasacciones': 376,
    'FECHA': '2025-02-05'
  },
  {
    'ID': 50,
    'V_USD': 2073.543114698958,
    'V_BS': 123292.87359999998,
    'V_CSH': 237.31197443659602,
    'V_EFEC': 529.8726067944837,
    'n_trasacciones': 452,
    'FECHA': '2025-02-06'
  },
  {
    'ID': 51,
    'V_USD': 2257.6749783837713,
    'V_BS': 135776.57320000028,
    'V_CSH': 344.89125374127036,
    'V_EFEC': 538.5166478217493,
    'n_trasacciones': 459,
    'FECHA': '2025-02-07'
  },
  {
    'ID': 52,
    'V_USD': 2917.28176255404,
    'V_BS': 175445.32520000034,
    'V_CSH': 726.0987695377452,
    'V_EFEC': 627.9995211173928,
    'n_trasacciones': 530,
    'FECHA': '2025-02-08'
  },
  {
    'ID': 53,
    'V_USD': 2237.547994679082,
    'V_BS': 134566.13640000013,
    'V_CSH': 410.6258729630861,
    'V_EFEC': 659.8931626205521,
    'n_trasacciones': 611,
    'FECHA': '2025-02-09'
  },
  {
    'ID': 54,
    'V_USD': 1905.4485459352281,
    'V_BS': 115317.74600000006,
    'V_CSH': 194.11797752808988,
    'V_EFEC': 1067.8013284864508,
    'n_trasacciones': 399,
    'FECHA': '2025-02-10'
  },
  {
    'ID': 55,
    'V_USD': 1839.127882391808,
    'V_BS': 111340.80199999994,
    'V_CSH': 445.8965972910472,
    'V_EFEC': 558.9489263296994,
    'n_trasacciones': 429,
    'FECHA': '2025-02-11'
  },
  {
    'ID': 56,
    'V_USD': 1915.8026282156316,
    'V_BS': 116921.43439999997,
    'V_CSH': 198.67081763067344,
    'V_EFEC': 736.5014976241192,
    'n_trasacciones': 404,
    'FECHA': '2025-02-12'
  },
  {
    'ID': 57,
    'V_USD': 2345.9312469437655,
    'V_BS': 143922.88199999963,
    'V_CSH': 490.57473512632436,
    'V_EFEC': 896.0145656071719,
    'n_trasacciones': 509,
    'FECHA': '2025-02-13'
  },
  {
    'ID': 58,
    'V_USD': 3156.465079262374,
    'V_BS': 195132.67120000027,
    'V_CSH': 502.8857974765447,
    'V_EFEC': 1093.8163248139763,
    'n_trasacciones': 653,
    'FECHA': '2025-02-14'
  },
  {
    'ID': 59,
    'V_USD': 3663.1878680038812,
    'V_BS': 226458.27400000105,
    'V_CSH': 631.293109026205,
    'V_EFEC': 937.7622516984794,
    'n_trasacciones': 768,
    'FECHA': '2025-02-15'
  },
  {
    'ID': 60,
    'V_USD': 3099.424115173081,
    'V_BS': 191606.39880000104,
    'V_CSH': 748.8152701391135,
    'V_EFEC': 719.8339242963442,
    'n_trasacciones': 688,
    'FECHA': '2025-02-16'
  },
  {
    'ID': 61,
    'V_USD': 2754.2418480642814,
    'V_BS': 150822.28360000043,
    'V_CSH': 380.22078159240317,
    'V_EFEC': 543.0009934258584,
    'n_trasacciones': 543,
    'FECHA': '2025-02-17'
  },
  {
    'ID': 62,
    'V_USD': 2917.28176255404,
    'V_BS': 175445.32520000034,
    'V_CSH': 726.0987695377452,
    'V_EFEC': 627.9995211173928,
    'n_trasacciones': 530,
    'FECHA': '2025-02-18'
  },
  {
    'ID': 63,
    'V_USD': 951.5607976841427,
    'V_BS': 59168.050399999935,
    'V_CSH': 120.9137986490833,
    'V_EFEC': 410.00395625603085,
    'n_trasacciones': 191,
    'FECHA': '2025-02-19'
  }
]

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


# Inicializar el diccionario de semanas
semanas = {semana: [] for semana in range(1, 6)}

# Convertir las fechas de semanas_variadas en rangos de fechas
rango_semanas = [
    (f'{año}-{mes_actual}-{semanas_variadas[semana][0]:02d}', f'{año}-{mes_actual}-{semanas_variadas[semana][-1]:02d}')
    for semana in range(5)
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

print(sum(usds_semanal[1]))

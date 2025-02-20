import calendar

data  =[
  {
    'ID': 1,
    'V_USD': 7615.370278685367,
    'V_BS': 396227.7155999984,
    'V_CSH': 1275.92811839323,
    'V_EFEC': 2545.820219104363,
    'n_trasacciones': 1309,
    'FECHA': '2025-01-02'
  },
  {
    'ID': 2,
    'V_USD': 9071.408963287047,
    'V_BS': 476883.9691999952,
    'V_CSH': 1811.1729123074,
    'V_EFEC': 4028.144911546509,
    'n_trasacciones': 1788,
    'FECHA': '2025-01-03'
  },
  {
    'ID': 3,
    'V_USD': 10329.333657979845,
    'V_BS': 543013.0703999948,
    'V_CSH': 1823.97717329275,
    'V_EFEC': 3894.547932280768,
    'n_trasacciones': 2096,
    'FECHA': '2025-01-04'
  },
  {
    'ID': 4,
    'V_USD': 6373.379151607382,
    'V_BS': 335048.5419999993,
    'V_CSH': 933.348487730645,
    'V_EFEC': 3406.7477953205243,
    'n_trasacciones': 1273,
    'FECHA': '2025-01-05'
  },
  {
    'ID': 5,
    'V_USD': 8243.825862659312,
    'V_BS': 433377.9255999974,
    'V_CSH': 1401.27658360281,
    'V_EFEC': 3733.905078942362,
    'n_trasacciones': 1457,
    'FECHA': '2025-01-06'
  },
  {
    'ID': 6,
    'V_USD': 6061.417958875684,
    'V_BS': 321315.7659999996,
    'V_CSH': 1308.0752688172,
    'V_EFEC': 3382.5011507262775,
    'n_trasacciones': 1107,
    'FECHA': '2025-01-07'
  },
  {
    'ID': 7,
    'V_USD': 5058.2751912568265,
    'V_BS': 268442.66440000053,
    'V_CSH': 993.63538722442,
    'V_EFEC': 1573.0561145656684,
    'n_trasacciones': 1040,
    'FECHA': '2025-01-08'
  },
  {
    'ID': 8,
    'V_USD': 1877.688385885886,
    'V_BS': 100043.2372,
    'V_CSH': 277.712087087087,
    'V_EFEC': 687.3907432432433,
    'n_trasacciones': 440,
    'FECHA': '2025-01-09'
  },
  {
    'ID': 9,
    'V_USD': 1468.9175858867222,
    'V_BS': 79101.212,
    'V_CSH': 266.84661095636,
    'V_EFEC': 411.98867966573806,
    'n_trasacciones': 249,
    'FECHA': '2025-01-10'
  },
  {
    'ID': 10,
    'V_USD': 5835.59401299907,
    'V_BS': 314246.7375999992,
    'V_CSH': 974.493407613742,
    'V_EFEC': 2640.6643639740014,
    'n_trasacciones': 1208,
    'FECHA': '2025-01-11'
  },
  {
    'ID': 11,
    'V_USD': 4464.876857938719,
    'V_BS': 240433.61880000072,
    'V_CSH': 887.768802228412,
    'V_EFEC': 2258.4540835654593,
    'n_trasacciones': 1066,
    'FECHA': '2025-01-12'
  },
  {
    'ID': 12,
    'V_USD': 4904.459751160627,
    'V_BS': 264105.1576000005,
    'V_CSH': 858.317363045497,
    'V_EFEC': 2571.516642525534,
    'n_trasacciones': 1064,
    'FECHA': '2025-01-13'
  },
  {
    'ID': 13,
    'V_USD': 5688.147193763916,
    'V_BS': 306477.3707999991,
    'V_CSH': 669.800668151448,
    'V_EFEC': 2284.179740163326,
    'n_trasacciones': 1058,
    'FECHA': '2025-01-14'
  },
  {
    'ID': 27,
    'V_USD': 6706.026426982945,
    'V_BS': 361857.18600000074,
    'V_CSH': 1113.6097108969607,
    'V_EFEC': 2888.872868791698,
    'n_trasacciones': 1280,
    'FECHA': '2025-01-15'
  },
  {
    'ID': 28,
    'V_USD': 6612.454015081849,
    'V_BS': 359519.1247999996,
    'V_CSH': 1187.6418981055726,
    'V_EFEC': 2245.395195880081,
    'n_trasacciones': 1475,
    'FECHA': '2025-01-16'
  },
  {
    'ID': 29,
    'V_USD': 9061.641015339657,
    'V_BS': 496215.46200000204,
    'V_CSH': 1728.1409788166543,
    'V_EFEC': 2293.0339152666184,
    'n_trasacciones': 1908,
    'FECHA': '2025-01-17'
  },
  {
    'ID': 30,
    'V_USD': 13683.063221329443,
    'V_BS': 749284.542000001,
    'V_CSH': 3191.0354273192106,
    'V_EFEC': 4161.542140248356,
    'n_trasacciones': 2615,
    'FECHA': '2025-01-18'
  },
  {
    'ID': 31,
    'V_USD': 6823.560189919646,
    'V_BS': 373658.15600000205,
    'V_CSH': 1298.4605551497446,
    'V_EFEC': 2827.5323301680064,
    'n_trasacciones': 1373,
    'FECHA': '2025-01-19'
  },
  {
    'ID': 32,
    'V_USD': 6443.82788563103,
    'V_BS': 353830.58919999877,
    'V_CSH': 1186.602986705518,
    'V_EFEC': 3088.037974867966,
    'n_trasacciones': 1398,
    'FECHA': '2025-01-20'
  },
  {
    'ID': 34,
    'V_USD': 4478.3646844880905,
    'V_BS': 246265.27399999922,
    'V_CSH': 908.1136570285506,
    'V_EFEC': 2315.3942607746862,
    'n_trasacciones': 938,
    'FECHA': '2025-01-21'
  },
  {
    'ID': 35,
    'V_USD': 5126.170893309228,
    'V_BS': 283477.2504,
    'V_CSH': 886.1537070524415,
    'V_EFEC': 1663.352405063291,
    'n_trasacciones': 1034,
    'FECHA': '2025-01-22'
  },
  {
    'ID': 36,
    'V_USD': 4619.593902439019,
    'V_BS': 257588.55600000065,
    'V_CSH': 669.9103299856527,
    'V_EFEC': 1724.4609110473455,
    'n_trasacciones': 1005,
    'FECHA': '2025-01-23'
  },
  {
    'ID': 37,
    'V_USD': 5935.641677327646,
    'V_BS': 334057.9136000001,
    'V_CSH': 845.4783226723525,
    'V_EFEC': 1441.4075550817342,
    'n_trasacciones': 1327,
    'FECHA': '2025-01-24'
  },
  {
    'ID': 38,
    'V_USD': 9376.554335465526,
    'V_BS': 527712.4779999967,
    'V_CSH': 1760.5245202558633,
    'V_EFEC': 3604.007803837953,
    'n_trasacciones': 2076,
    'FECHA': '2025-01-25'
  },
  {
    'ID': 39,
    'V_USD': 5508.805167022031,
    'V_BS': 310035.5547999991,
    'V_CSH': 1052.269012082445,
    'V_EFEC': 2198.5046126510306,
    'n_trasacciones': 1019,
    'FECHA': '2025-01-26'
  },
  {
    'ID': 40,
    'V_USD': 4685.2215710503115,
    'V_BS': 265417.80200000055,
    'V_CSH': 736.9853486319505,
    'V_EFEC': 2279.089214474845,
    'n_trasacciones': 1103,
    'FECHA': '2025-01-27'
  },
  {
    'ID': 41,
    'V_USD': 4615.850742173754,
    'V_BS': 262457.27319999976,
    'V_CSH': 639.4145269081956,
    'V_EFEC': 2371.6476820260286,
    'n_trasacciones': 1275,
    'FECHA': '2025-01-28'
  },
  {
    'ID': 42,
    'V_USD': 4992.218513089001,
    'V_BS': 286054.12080000096,
    'V_CSH': 572.5905759162305,
    'V_EFEC': 1617.6804607329843,
    'n_trasacciones': 1112,
    'FECHA': '2025-01-29'
  },
  {
    'ID': 43,
    'V_USD': 7072.824199337861,
    'V_BS': 405909.38079999894,
    'V_CSH': 1924.6208398675724,
    'V_EFEC': 1899.0336365220423,
    'n_trasacciones': 1347,
    'FECHA': '2025-01-30'
  },
  {
    'ID': 44,
    'V_USD': 7144.358557874757,
    'V_BS': 414158.4655999994,
    'V_CSH': 1268.773503536312,
    'V_EFEC': 1728.8031671554252,
    'n_trasacciones': 1772,
    'FECHA': '2025-01-31'
  },
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
    'V_USD': 3150.18633000965,
    'V_BS': 195878.58600000045,
    'V_CSH': 446.55725313605666,
    'V_EFEC': 944.9260791251207,
    'n_trasacciones': 716,
    'FECHA': '2025-02-19'
  }
]
from datetime import datetime, timedelta

# Obtener la fecha actual y calcular el inicio y fin de la semana
fecha_sistema = datetime.now().date()  # Fecha del día actual
inicio_semana = fecha_sistema - timedelta(days=fecha_sistema.weekday())  # Lunes de la semana actual
fin_semana = inicio_semana + timedelta(days=6)  # Domingo de la semana actual

# Lista para el rango de fechas de la semana (de lunes a domingo)
fechas_semana = [(inicio_semana + timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]

# Inicializar ventas semanales con valores vacíos (uno por cada día de la semana)
ventas_semanales = [None] * 7

# Llenar las ventas semanales con los datos disponibles
for registro in data:
    fecha = registro['FECHA']
    if fecha in fechas_semana:  # Solo considerar fechas dentro de la semana actual
        indice_dia = fechas_semana.index(fecha)  # Obtener el índice correspondiente (lunes=0, martes=1, ...)
        ventas_semanales[indice_dia] = registro['V_USD']  # Asignar el valor de ventas para ese día

# Imprimir las fechas de la semana y las ventas para cada día
print("Fechas de la semana:", fechas_semana)
print("Ventas semanales:", ventas_semanales)


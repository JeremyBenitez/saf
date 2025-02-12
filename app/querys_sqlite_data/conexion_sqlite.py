import sqlite3
from datetime import datetime,timedelta
fecha = datetime.now()
fecha_diaria = fecha.date()
fecha_hace_6Day = fecha_diaria - timedelta(days=6)



def consulta_ventas(fecha_init,fecha_end):
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\BDTiendas.db")
    pointer = conexion.cursor()
    pointer.execute("""
                    SELECT 
    SUM(V_USD) AS total_usd,
    SUM(V_BS) AS total_bs,
    SUM(V_CSH) AS total_csh,
    SUM(V_EFEC) AS total_efec
FROM (
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM BABILON
    UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM BARALT
    UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CABUDARE
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CAGUA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CABIMAS
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CATIA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM CRUZ_VERDE
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM GUACARA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM GUANARE
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM KAPITANA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM MATURIN
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM PROPATRIA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM UPATA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM VALENCIA
	UNION ALL
    SELECT V_USD, V_BS, V_CSH, V_EFEC, FECHA FROM VALERA
) AS todas_las_tablas
WHERE FECHA BETWEEN ? AND ?;
""",(fecha_init,fecha_end))
    data = pointer.fetchall()
    conexion.close()
    return data


class index:

    def valores(self, tabla):
        self.conexion = sqlite3.connect(r'C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\BDTiendas.db')
        pointer = self.conexion.cursor()
        pointer.execute(f"SELECT V_USD , n_trasacciones FROM {tabla} ")
        self.data = pointer.fetchall()
        self.conexion.close()
        return  self.data
    
    def tiendas(self, tabla):
        self.conexion = sqlite3.connect(r'C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\BDTiendas.db')
        pointer = self.conexion.cursor()
        pointer.execute(f"SELECT * FROM {tabla} ")
        self.data = pointer.fetchall()
        self.conexion.close()
        return  self.data
    
    def tienda_times(self, tabla,fi,fo):
        self.conexion = sqlite3.connect(r'C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\BDTiendas.db')
        pointer = self.conexion.cursor()
        pointer.execute(f"SELECT * FROM {tabla} WHERE FECHA BETWEEN  ? AND  ?",(fi, fo))
        colums = [colum[0] for colum in pointer.description]
        rows = pointer.fetchall()
        self.data = [dict(zip(colums,row))for  row in rows]
        self.conexion.close()
        return  self.data


v = index()
valor = v.tienda_times('Kapitana',str(fecha_hace_6Day),str(fecha_diaria))
print(valor)


def consulta(tienda):
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
    pointer = conexion.cursor()
    pointer.execute("SELECT * FROM ventas_tienda WHERE TIENDA = ?",(tienda,))
    data = pointer.fetchall()
    conexion.close()
    return data


def consulta_anterior(tienda,tabla):
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
    pointer = conexion.cursor()
    pointer.execute(f"SELECT V_USD FROM {tabla} WHERE TIENDA = ?",(tienda,))
    data = pointer.fetchall()
    conexion.close()
    return data[0][0]


def consulta_fechas(columna):
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
    pointer = conexion.cursor()
    pointer.execute(f"SELECT {columna} FROM fechas")
    data = pointer.fetchall()
    conexion.close()
    return data[0][0]

def consulta_semanal(tienda,tabla):
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
    pointer = conexion.cursor()
    pointer.execute(f"SELECT * FROM {tabla} WHERE TIENDA = ?",(tienda,))
    data = pointer.fetchall()
    conexion.close()
    return data





def consulta_mensual(tienda,mes):
        conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
        pointer = conexion.cursor()
        pointer.execute(f"SELECT * FROM ventas_mensuales WHERE TIENDA = ? AND MES = ?",(tienda,mes))
        data = pointer.fetchall()
        conexion.close()
        return data




def consulta_dpto_ventas():
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
    pointer = conexion.cursor()
    pointer.execute("SELECT * FROM ventas_departamentos")
    data = pointer.fetchall()
    conexion.close()
    return data

m1 = consulta_mensual('Baralt','1') # TIENDA, MES
m2 = consulta_mensual('Baralt','2')
m3 = consulta_mensual('Baralt','3')
m4 = consulta_mensual('Baralt','4')
m5 = consulta_mensual('Baralt','5')
m6 = consulta_mensual('Baralt','6')
m7 = consulta_mensual('Baralt','7')
m8 = consulta_mensual('Baralt','8')
m9 = consulta_mensual('Baralt','9')
m10 = consulta_mensual('Baralt','10')
m11 = consulta_mensual('Baralt','11')


def prueba():
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
    pointer = conexion.cursor()
    pointer.execute("SELECT V_USD FROM ventas_tienda")
    data = pointer.fetchall()
    conexion.close()
    return data

def grafico_trans():
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
    pointer = conexion.cursor()
    pointer.execute("SELECT N_TRANSACCIONES FROM ventas_tienda")
    data = pointer.fetchall()
    conexion.close()
    return data


def users(username):
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
    pointer = conexion.cursor()
    pointer.execute(f"SELECT * FROM USUARIOS WHERE username = ?",(username,))
    data = pointer.fetchall()
    conexion.close()
    return data



def consulta_fechas_prueba():
    conexion = sqlite3.connect(r"C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db")
    pointer = conexion.cursor()
    pointer.execute(f"SELECT * FROM fechas")
    data = pointer.fetchall()
    conexion.close()
    return data


import sqlite3
from datetime import date, timedelta
import calendar

class BaseDatos:
    def __init__(self, db_path):
        self.db_path = db_path

    def conectar(self):
        """Establece la conexión con la base de datos."""
        self.conexion = sqlite3.connect(self.db_path)

    def obtener_semanas_febrero(self, año):
        """Devuelve los rangos de fechas para cada semana de febrero."""
        semanas = []
        mes = 2  # Febrero
        primer_dia = date(año, mes, 1)
        _, dias_en_mes = calendar.monthrange(año, mes)

        # Calcular las semanas
        dia_actual = primer_dia
        while dia_actual.month == mes:
            inicio_semana = dia_actual
            fin_semana = min(dia_actual + timedelta(days=6), date(año, mes, dias_en_mes))
            semanas.append((inicio_semana, fin_semana))
            dia_actual = fin_semana + timedelta(days=1)  # Ir a la siguiente semana

        return semanas

    def consultar_por_semana(self, tabla, año):
        """Consulta la base de datos por cada semana de febrero."""
        self.conectar()
        pointer = self.conexion.cursor()
        
        semanas = self.obtener_semanas_febrero(año)
        resultados = {}

        for i, (fi, fo) in enumerate(semanas, start=1):
            query = f"SELECT * FROM {tabla} WHERE FECHA BETWEEN ? AND ?"
            pointer.execute(query, (fi.strftime('%Y-%m-%d'), fo.strftime('%Y-%m-%d')))
            colums = [colum[0] for colum in pointer.description]
            rows = pointer.fetchall()
            data = [dict(zip(colums, row)) for row in rows]

            resultados[f"Semana {i}: {fi} - {fo}"] = data

        self.conexion.close()
        return resultados

# Uso del código
db = BaseDatos(r'C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\BDTiendas.db')
resultados = db.consultar_por_semana("Kapitana", 2025)

for semana, datos in resultados.items():
    print(f"\n{semana}")
    for fila in datos:
        print(fila)


if __name__ == "__main__":
    pass
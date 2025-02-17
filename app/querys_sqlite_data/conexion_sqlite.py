import sqlite3
from datetime import datetime,timedelta
from pathlib import Path



fecha = datetime.now()
fecha_diaria = fecha.date()
fecha_hace_6Day = fecha_diaria - timedelta(days=6)


base_dir  = Path().resolve()

db_path = base_dir / "BBDDs" / "BDTiendas.db"

db_path_bd1 = base_dir / "BBDDs" / "DBD1.db"

db_path_2024 = base_dir / "BBDDs" / "BD2024.db"

def get_db():
    conexion = sqlite3.connect(str(db_path))
    return conexion

def get_db_db1():
    conexion = sqlite3.connect(str(db_path_bd1))
    return conexion

def get_db_db2024():
    conexion = sqlite3.connect(str(db_path_2024))
    return conexion


def consulta_ventas(fecha_init,fecha_end):
    conexion = get_db()
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
        self.conexion = get_db()
        pointer = self.conexion.cursor()
        pointer.execute(f"SELECT V_USD , n_trasacciones FROM {tabla} ")
        self.data = pointer.fetchall()
        self.conexion.close()
        return  self.data
    
    def tiendas(self, tabla):
        self.conexion = get_db()
        pointer = self.conexion.cursor()
        pointer.execute(f"SELECT * FROM {tabla} ")
        self.data = pointer.fetchall()
        self.conexion.close()
        return  self.data
    
    def tienda_times(self, tabla,fi,fo):
        self.conexion = get_db()
        pointer = self.conexion.cursor()
        pointer.execute(f"SELECT * FROM {tabla} WHERE FECHA BETWEEN  ? AND  ?",(fi, fo))
        colums = [colum[0] for colum in pointer.description]
        rows = pointer.fetchall()
        self.data = [dict(zip(colums,row))for  row in rows]
        self.conexion.close()
        return  self.data

a = index()

valor =a.tienda_times('Kapitana','2025-02-01','2025-02-28')
print(valor)

semana1 = []
semana2 = []
semana3= []
semana4 = []

valores = []

for i in valor:
        if i['FECHA'] >= '2025-02-01' and i['FECHA'] <= '2025-02-02':
            semana1.append(i['V_USD'])
        elif i['FECHA'] >= '2025-02-03' and i['FECHA'] <= '2025-02-09':
            semana2.append(i['V_USD'])
        elif i['FECHA'] >= '2025-02-10' and i['FECHA'] <= '2025-02-16':
            semana3.append(i['V_USD'])
        elif i['FECHA'] >= '2025-02-17' and i['FECHA'] <= '2025-02-23':
            semana4.append(i['V_USD'])   


valores.append((semana1))
valores.append((semana2))
valores.append((semana3))
valores.append((semana4))
print(valores)



def consulta_dpto_ventas():
    conexion = get_db_db1()
    pointer = conexion.cursor()
    pointer.execute("SELECT * FROM ventas_departamentos")
    data = pointer.fetchall()
    conexion.close()
    return data



def users(username):
    conexion = get_db_db1()
    pointer = conexion.cursor()
    pointer.execute(f"SELECT * FROM USUARIOS WHERE username = ?",(username,))
    data = pointer.fetchall()
    conexion.close()
    return data



def consulta_fechas_prueba():
    conexion = get_db_db1()
    pointer = conexion.cursor()
    pointer.execute(f"SELECT * FROM fechas")
    data = pointer.fetchall()
    conexion.close()
    return data


if __name__ == "__main__":
    pass
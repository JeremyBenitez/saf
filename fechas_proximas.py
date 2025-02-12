
import sqlite3
from datetime import datetime, timedelta

fecha = datetime.now()
fecha_diaria = fecha.date()
fecha_1Day = fecha_diaria + timedelta(days=1)
fecha_2Day = fecha_diaria + timedelta(days=2)
fecha_3Day = fecha_diaria + timedelta(days=3)
fecha_4Day = fecha_diaria + timedelta(days=4)
fecha_5Day = fecha_diaria + timedelta(days=5)
fecha_6Day = fecha_diaria + timedelta(days=6)

def Update(f1,f2,f3,f4,f5,f6,id_fecha):    
    conexion = sqlite3.connect(r'C:\Users\Windows 11\Downloads\Dashboard-main\Dashboard-main\BBDDs\DBD1.db')
    pointer = conexion.cursor()
    pointer.execute("UPDATE fechas SET field1 = ?,field2= ?, field3 = ?, field4 = ?,field5=?, field6= ? WHERE ID = ?",(f1,f2,f3,f4,f5,f6, id_fecha))
    conexion.commit()
    conexion.close()

Update(fecha_1Day,fecha_2Day,fecha_3Day,fecha_4Day,fecha_5Day,fecha_6Day,9)

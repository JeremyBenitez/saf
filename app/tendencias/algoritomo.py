import json
from collections import defaultdict
from data import data

# Tu JSON de ejemplo


# Diccionario para almacenar la suma por departamento
departamentos_totales = defaultdict(float)

# Recorrer los datos y sumar las cantidades por departamento
for registro in data:
    departamento = registro["c_Departamento"]
    cantidad = float(registro["cantidad"])  # Convertir a número
    departamentos_totales[departamento] += cantidad

# Mostrar los resultados
for departamento, total in departamentos_totales.items():
    print(f"Departamento {departamento}: Total {total}")


dpto = ['HG', 'CZ']
for i in dpto:
    print(i)
import calendar

def semanas_del_mes(año, mes):
    semanas = calendar.monthcalendar(año, mes)
    return semanas

año = 2025
mes = 2  # Febrero
for i, semana in enumerate(semanas_del_mes(año, mes), start=1):
    print(f"Semana {i}: {año}{mes}{semana}")

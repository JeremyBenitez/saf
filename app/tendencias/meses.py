from datetime import datetime,date
import calendar

fecha = datetime.now()
mes_date = fecha.date().month
mes_actual = f'{mes_date:02d}'

year = 2025

mes_init = []
mes_fin = []
for month in range(1, 13):
    first_day = date(year, month, 1)

    last_day_of_month = calendar.monthrange(year, month)[1]
    last_day = date(year, month, last_day_of_month)

    mes_init.append(str(first_day))
    mes_fin.append(str(last_day))






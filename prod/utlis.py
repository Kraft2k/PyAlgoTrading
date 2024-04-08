from datetime import datetime

# Определяем текущую дату и время
now = datetime.now()

# Проверяем, является ли текущий день рабочим
if now.weekday() < 5:
    print("Сегодня рабочий день")
else:
    print("Сегодня выходной")

# Проверяем, является ли текущее время рабочим
main_exchange_session_start = datetime.strptime("10:00", "%H:%M")
main_exchange_session_end = datetime.strptime("18:40", "%H:%M")

print(f'')
print(f'{now:%d-%m-%Y}')

if main_exchange_session_end.time() <= now.time() <= work_end.time():
    print("Сейчас рабочее время")
else:
    print("Сейчас не рабочее время")

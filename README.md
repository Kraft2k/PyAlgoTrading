# Термины и определения:

Список счетов (аккаунтов) доступных в терминале трейдера Quik

Тикер инструмента - краткое обозначения инструментов денежного рынка: акции, фьючерсы, облигации и т.д.

Направление заявки - покупка - 'B' или продажа 'S'


# Модули

## accounts.py

### Description
Получение информации по счетам: деньги и открытые позиции.
Построение таблицы состояния счетов (портфелей) в формате List of list для дальнейшего отображения в терминале.

### Tasks
1 дополнить таблицу информации о процентном изменении курса иструментов к закрытию предыдущего торгового дня

2 выход из модуля и программы при несоответствии аккаунтов доступных в текущем терминале Quik +++

3 исправить ошибку "TypeError: can't multiply sequence by non-int of type 'float" line 106 модуля 

## transactions.py

### Description
Модуль отправки заявок через API терминала Quik

## read_params.py

### Description
Модуль чтения параметров (счета, тикеры и т.д.) из файла

## command_analyzer.py



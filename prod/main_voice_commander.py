import json, pyaudio
from vosk import Model, KaldiRecognizer

from transactions import Trans2Quik, TransactionUnit
from command_analyzer import audio_str_to_quik_str
from accounts import GetAccountPosition, TablePositions

from prettytable import PrettyTable

import sys

model = Model('C:/PyAlgoTrading/prod/vosk-model-small-ru-0.22')
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']


if __name__ == '__main__':
    
    big_accounts = ['1220166', '1311258', '1761021', '1946559', '1988370', '321697', '224420', '356046', '43816', '63031', ]
    cur_accounts = ['1220166', '1311258', '1761021', '1946559', '1988370', '356046', '43816', '63031', ]
    small_accounts = ['29570', '170743', '1411251', '1753378', ]
    shturm_accounts = ['2007695', ]
    
    accounts = shturm_accounts

    portfolio = TransactionUnit(accounts)
    portfolio.quik_api_connect()
    table = PrettyTable()
    
    for text in listen():
        print(str(text))    
        p = str(text)
        command = audio_str_to_quik_str(p)
        print('')

        if text == "привет":
            print('И Вам не болеть.')
            print('Желаю удачной торговли!')
            print('')

        elif text == "показать портфель":
            portfolio.close_connection()
            portfolio_info = GetAccountPosition(accounts)
            portfolio_info.get_cash()
            portfolio_info.build_table_positions()
            portfolio_info.get_positions()
            portfolio_info.get_portfolios_with_account_value()
            portfolio_info.get_portfolios_as_percentage()     
            table.field_names = TablePositions.rows[0]
            for i in range(1,len(TablePositions.rows)):
                table.add_row(TablePositions.rows[i])
            print(table)
            print('')
            portfolio_info.close_connection()

        elif text == 'помощь':
            print('Формат сообщения для подачи заявки')
            print('----------------------------------------')
            print('направление : тикер : цена : количество')
            print('----------------------------------------')
            print('')
            print('Примеры сообщений для подачи заявок:')
            print('----------------------------------------')
            print('купить лукойл цена 4300 количество 50')
            print('сбер продать цена 300 количество 100')
            print('----------------------------------------')
            print('')

        elif text == 'выход' :
            print('')
            portfolio.close_connection()
            sys.exit()
        
        elif 'купи' in text:
            print(command)
            portfolio.command_to_transaction(command)
            print('')

        elif 'прод' in text:
            print(command)
            portfolio.command_to_transaction(command)
            print('')

        elif text == 'закрыть':
            portfolio.close_all_short_positions()

        else:
            print('Команда не определена!')
            print('')
                
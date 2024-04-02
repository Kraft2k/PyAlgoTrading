import json, pyaudio
from vosk import Model, KaldiRecognizer


from transactions import Trans2Quik, TransactionUnit
#from command_analyzer import audio_str_to_quik_str
from accounts import GetAccountPosition, TablePositions
from messages import CommandMessages

from colorama import Fore, Style
from prettytable import PrettyTable


import sys

alias = {
        '108098' : 'Kangaroo',
        '1220166': 'Elephant',
        '1311258': 'Rhino',
        '1411251': 'Zebra',
        '1689321': 'Ant',
        '1701218': 'Dolphin',
        '170743' : 'Panda',
        '1753378': 'Giraffe',
        '1761021': 'Gorilla',
        '1862020': 'Whale',
        '1946559': 'Bear',
        '1988370': 'Flamingo',
        '2089746': 'Octopus',
        '224420' : 'Spider',
        '29570'  : 'Capybara',
        '31753'  : 'Giraffe',
        '321697' : 'Sturgeon',
        '356046' : 'Pike',
        '43816'  : 'Turtle',
        '63031'  : 'Ladybug',
        '697409' : 'Gudgeon'
}


model = Model('C:/PyAlgoTrading/prod/vosk-model-small-ru-0.22')
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

messages = CommandMessages

big1_accounts = ['1220166', '43816',  ]
big2_accounts = ['1311258', '1761021', '321697', '356046',]
big3_accounts = ['1988370', '224420', '63031', '1862020',]
medium_accounts = ['108098', '2202763', '1946559', '1689321', '31753']
small_accounts = ['1411251', '1701218', '697409']
micro_accounts = ['170743', '2089746', '1753378', ]
nano_accounts = ['29570']

accounts = big1_accounts

portfolio = TransactionUnit('QTBR', accounts)


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']


if __name__ == '__main__':
       
    portfolio.quik_api_connect()
    table = PrettyTable()
    messages.greetings()

    for text in listen():
         
        print(f'{Fore.YELLOW}{text}{Style.RESET_ALL}')
        command_text = str(text)
    
        #command = audio_str_to_quik_str(command_text)
        print('')

        if text == "привет":
            messages.respond_on_greeting()

        elif text == "как дела":
            messages.respond_on_how_are_you()

        elif text == "показать":
            portfolio.close_connection()
            portfolio_info = GetAccountPosition(accounts )
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
            portfolio = TransactionUnit('TQBR', accounts)
            

        elif text == 'помощь':
            messages.help_list()

        elif text == 'выход' :
            print(f'')
            portfolio.close_connection()
            sys.exit()
        
        # elif 'купи' in text:
        #     print(command)
        #     portfolio.command_to_transaction(command)
        #     print('')

        # elif 'прод' in text:
        #     print(command)
        #     portfolio.command_to_transaction(command)
        #     print('')


        elif text == 'закрыть шорт весь':
            portfolio.close_all_short_positions()
            print('')

        elif text == 'открыть лонг':
            portfolio.open_long_once_random_qauntity([ 'AFLT',], 5, 3, 200)

        elif text == 'закрыть лонг':
            portfolio.close_some_long_positions(['NVTK',] )

            print('')

        else:
            messages.misundestanding()
                
        
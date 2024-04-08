import json, pyaudio
from vosk import Model, KaldiRecognizer
import pyttsx3
import configparser

from transactions import Trans2Quik, TransactionUnit
#from command_analyzer import audio_str_to_quik_str
from accounts import GetAccountPosition, TablePositions
from messages import CommandMessages

from colorama import Fore, Style
from prettytable import PrettyTable

import sys
import os
import time
from datetime import datetime

sys.path.insert(1, os.path.join(sys.path[0], ".."))
sys.path.insert(1, os.path.join(sys.path[0], "../.."))

from MarketPy.Schedule import Schedule, MOEXStocks, MOEXFutures


#Set voice recognizer
model = Model('C:/PyAlgoTrading/prod/vosk-model-small-ru-0.22')
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

#Set speaker
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', 'ru')
#Set russian system voice assistent
i = 0
for voice in voices:
    #print(voice.name)
    if voice.name == 'Microsoft Irina Desktop - Russian':
        engine.setProperty('voice', voices[i].id)   
    i+=1
engine.setProperty("rate", 210)


schedule = MOEXStocks()
market_datetime_now = schedule.utc_to_msk_datetime(datetime.utcnow())  
print(f'Текущее время: {market_datetime_now.strftime("%d.%m.%Y %H:%M:%S")}',  end='')
if schedule.trade_session(market_datetime_now) == None: print(f' Торги закрыты, откроются через {schedule.time_until_trade(market_datetime_now)}')

#Global setting
speaker = True
check_command = True
show_percentage = True
messages = CommandMessages

big1_accounts = ['1220166', '43816', ]
big2_accounts = ['1311258', '1761021', '321697', '356046',]
big3_accounts = ['1988370', '224420', '63031', '1862020',]
medium_accounts = ['108098', '2202763', '1946559', '1689321', '31753']
small_accounts = ['1411251', '1701218', '697409']
micro_accounts = ['170743', '2089746', '1753378', ]
nano_accounts = ['29570']

#Read settings from file
config = configparser.ConfigParser()
config.sections()
config.read('C:/PyAlgoTrading/prod/config/big1_config.ini')
groups_accounts = [item for item in config.sections() if 'accounts' in item]
index_group = 0
accounts = config[groups_accounts[index_group]]
#print(accounts)

portfolio = TransactionUnit('TQBR', accounts)
#portfolio.quik_api_connect()

def show_portfolios(portfolio, show_percentage=True):
    portfolio.close_connection()
    portfolio_info = GetAccountPosition(accounts, display_alias=True)
    portfolio_info.get_cash()
    portfolio_info.build_table_positions()
    portfolio_info.get_positions()
    portfolio_info.get_portfolios_with_account_value()
    if show_percentage: portfolio_info.get_portfolios_as_percentage()
    print(f'Текущая группа счетов: {Fore.GREEN}{groups_accounts[index_group]}{Style.RESET_ALL}')
    table = PrettyTable()
    table.field_names = TablePositions.rows[0]
    for i in range(1,len(TablePositions.rows)):
        table.add_row(TablePositions.rows[i])
    print(table)
    del table
    TablePositions.rows = [["account", "cash"], ]
    print(f'')
    portfolio_info.close_connection()
 
def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']
    
def voice_message(message):
    time.sleep(0.8)
    engine.say(message)
    engine.runAndWait()
    

if __name__ == '__main__':
       
    
    #table = PrettyTable()
    portfolio.quik_api_connect()

    message = messages.greetings()
    if speaker: voice_message(message)
    show_portfolios(portfolio)
    message = messages.waiting_commands()
    if speaker: voice_message(message)
    print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

    for text in listen():
         
        print(f'{Fore.YELLOW}{text}{Style.RESET_ALL}')
        command_text = str(text)
        #command = audio_str_to_quik_str(command_text)
        print('')
        if text == "привет":
            message = messages.response_on_greeting()
            if speaker: voice_message(message)
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

        elif text == "как дела":
            message = messages.response_on_how_are_you()
            if speaker: voice_message(message)
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

        elif "включить" in text:
            message = messages.on_voice_messages()
            speaker = True
            if speaker: voice_message(message)
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

        elif "выключить" in text:
            message = messages.off_voice_messages()
            speaker = False
            if speaker: voice_message(message)
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

        elif "изменить" in text:
            #print(groups_accounts)
            #print(f'')
            print(f'Текущая группа счетов выделена {Fore.GREEN}зеленым{Style.RESET_ALL} цветом:')
            print(f'')
            for index in range(0 , len(groups_accounts)):
                if index == index_group:
                    print(f'{Fore.GREEN}{groups_accounts[index]}{Style.RESET_ALL} : ',  end='')
                else:
                    print(f'{groups_accounts[index]} : ',  end='')
                for key in config[groups_accounts[index]]: print(f' {key}', end='')
                print(f'')
            print(f'')
            print(f'Чтобы изменить текущую группу счетов скажите {Fore.GREEN}"Вниз"{Style.RESET_ALL},{Fore.GREEN}"Вверх"{Style.RESET_ALL} или {Fore.GREEN}"Сохранить"{Style.RESET_ALL}')
            print(f'')
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

            for text in listen():

                print(f'{Fore.YELLOW}{text}{Style.RESET_ALL}')
                if 'вниз' in text:

                    if index_group < (len(groups_accounts)-1) :
                        index_group += 1
                    elif index_group == (len(groups_accounts)-1):
                        index_group = 0
                    else:
                        index_group = 0 
                    
                    print(f'')
                    print(f'Текущая группа счетов выделена зеленым цветом:')
                    print(f'')
                    for index in range(0 , len(groups_accounts)):
                        if index == index_group:
                            print(f'{Fore.GREEN}{groups_accounts[index]}{Style.RESET_ALL} : ',  end='')
                        else:
                            print(f'{groups_accounts[index]} : ',  end='')
                        for key in config[groups_accounts[index]]: print(f' {key}', end='')
                        print(f'')
                    print(f'')
                    print(f'Чтобы изменить текущую группу счетов скажите {Fore.GREEN}"Вниз"{Style.RESET_ALL},{Fore.GREEN} "Вверх"{Style.RESET_ALL} или {Fore.GREEN}"Сохранить"{Style.RESET_ALL}!')
                    
                    print(f'')
                    print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

                elif 'верх' in text:

                    if index_group > 0 :
                        index_group -= 1
                    elif index_group == 0:
                        index_group = (len(groups_accounts)-1)
                    else:
                        index_group = (len(groups_accounts)-1)
                    print(f'')
                    print(f'Текущая группа счетов выделена зеленым цветом:')
                    print(f'')
                    for index in range(0 , len(groups_accounts)):
                        if index == index_group:
                            print(f'{Fore.GREEN}{groups_accounts[index]}{Style.RESET_ALL} : ',  end='')
                        else:
                            print(f'{groups_accounts[index]} : ',  end='')
                        for key in config[groups_accounts[index]]: print(f' {key}', end='')
                        print(f'')
                    print(f'')
                    print(f'Чтобы изменить текущую группу счетов скажите {Fore.GREEN}"Вниз"{Style.RESET_ALL},{Fore.GREEN} "Вверх"{Style.RESET_ALL} или {Fore.GREEN}"Сохранить"{Style.RESET_ALL}')
                    print(f'')
                    print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)
                    
                else:
                    accounts = config[groups_accounts[index_group]]
                    portfolio.close_connection()
                    del portfolio
                    portfolio = TransactionUnit('TQBR', accounts)
                    print(f'')
                    print(f'Настройки сохранены.')
                    print(f'')
                    show_portfolios(portfolio)
                    break
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

        elif text == "показать":
            show_portfolios(portfolio)
             
            #print(f'')
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

        elif text == "показать все":
            show_portfolios(portfolio, False)
     
            #print(f'')
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)
        
        elif text == "очистить":
            os.system('cls' if os.name == 'nt' else 'clear')
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

        elif 'какая' in text:
            message = messages.ask_Alice()
            if speaker: voice_message(message)
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)
            
        elif text == 'помощь':
            message = messages.help_list()
            if speaker: voice_message(message)
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)


        elif text == 'выход' :
            message = messages.response_on_exit()
            if speaker: voice_message(message)
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
            show_portfolios(portfolio)
            portfolio = TransactionUnit('TQBR', accounts)
            market_datetime_now = schedule.utc_to_msk_datetime(datetime.utcnow())  
           
            if schedule.trade_session(market_datetime_now) == None: 
                print(f'Торги закрыты, повторите попытку через {schedule.time_until_trade(market_datetime_now)}')
            else:
                message = messages.check_close_all_short_postions()
                if speaker: voice_message(message)
                print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)
            
                for text in listen():
                    print(f'{Fore.YELLOW}{text}{Style.RESET_ALL}')
                    if text == 'исполнить':
                        portfolio.close_all_short_positions()
                        print(f'')
                        print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)
                        break
                    else:
                        print(f'Вы отменили команду.')
                        print(f'')
                        print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)
                        break

        elif text == 'закрыть лонг весь':
            show_portfolios(portfolio)
            portfolio = TransactionUnit('TQBR', accounts)
            message = messages.check_close_all_long_postions()
            if speaker: voice_message(message)
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)
            for text in listen():
                print(f'{Fore.YELLOW}{text}{Style.RESET_ALL}')
                if text == 'исполнить':
                    portfolio.close_all_short_positions()
                    print(f'')
                    print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)
                    break
                else:
                    print(f'Вы отменили команду.')
                    print(f'')
                    print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)
                    break

        elif text == 'открыть лонг':
            portfolio.open_long_once_random_qauntity([ 'AFLT',], 5, 3, 200)

        elif text == 'закрыть лонг':
            portfolio.close_some_long_positions(['MTLRP',] )
            print('')

        else:
            message = messages.misundestanding()
            if speaker: voice_message(message)
            print(f'{Fore.YELLOW}>>>{Style.RESET_ALL} ', end='', flush=True)

            
                
        
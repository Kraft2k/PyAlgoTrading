import ctypes
from ctypes import *
from ctypes import wintypes
from pathlib import Path

import random
import time
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../QuikPy"))

sys.path.insert(1, os.path.join(sys.path[0], "../.."))
sys.path.insert(1, os.path.join(sys.path[0], ".."))

from QuikPy import QuikPy  # Working with QUIK from Python via QuikSharp LUA scripts
from backtrader_moexalgo.moexalgo_store import MoexAlgoStore  # Storage AlgoPack

class Trans2Quik:

    LIB_QUIK_API = cdll.LoadLibrary(r"C:\Trans2QuikAPI\trans2quik.dll")

    PATH_2_QUIK = "C:/BCS_Shturm/QUIK_BCS/"
    PATH_2_QUIK = str(Path(PATH_2_QUIK)) 
    PATH_2_QUIK = bytes(PATH_2_QUIK,'ascii')

    _TRANS2QUIK_CONNECT = LIB_QUIK_API.TRANS2QUIK_CONNECT
    _TRANS2QUIK_CONNECT.restype = c_long
    _TRANS2QUIK_CONNECT.argtypes = [wintypes.LPSTR, 
                                    ctypes.POINTER(c_long), 
                                    wintypes.LPSTR,  
                                    wintypes.DWORD]


    _TRANS2QUIK_SEND_ASYNC_TRANSACTION = LIB_QUIK_API.TRANS2QUIK_SEND_ASYNC_TRANSACTION
    _TRANS2QUIK_SEND_ASYNC_TRANSACTION.restype = c_long
    _TRANS2QUIK_SEND_ASYNC_TRANSACTION.argtypes = [wintypes.LPSTR, 
                                                    ctypes.POINTER(c_long), 
                                                    wintypes.LPSTR,  
                                                    wintypes.DWORD]


class TransactionUnit:
    
    def __init__(self, accounts ):
        
        self.quik_provider = QuikPy()
        self.class_code = 'TQBR'
        self.ticker_prefix = self.class_code + '.'

        self.store = MoexAlgoStore()

        self.accounts = accounts
        self.depo_limits = self.quik_provider.GetAllDepoLimits()['data']
        self.accounts_cash = self.quik_provider.GetMoneyLimits()['data']

        self.lpstrPathToQUIK = Trans2Quik.PATH_2_QUIK
        self.pnExtendedErrorCode = ctypes.c_long()
        self.lpstrErrorMessage = create_string_buffer(250)
        self.dwErrorMessageSize = 250
        
 
    def quik_api_connect(self):

        FunctionResult = Trans2Quik._TRANS2QUIK_CONNECT(self.lpstrPathToQUIK,
                                     ctypes.byref(self.pnExtendedErrorCode), 
                                     self.lpstrErrorMessage, 
                                     self.dwErrorMessageSize)

        print()
        print("connect:")
        print("FunctionResult = ", FunctionResult)
        print("ErrorCode =", self.pnExtendedErrorCode.value)
        print("error = ", self.lpstrErrorMessage.value,"\n")


    def quik_api_send_async_transaction(self, classcode, seccode, client_code, operation, quantity, price):
        """ """
        # transaction_string = b"ACTION=NEW_ORDER; TRANS_ID=777; CLASSCODE=TQBR; SECCODE=SIBN; ACCOUNT=L01-00000F00; CLIENT_CODE=2007693; TYPE=L; OPERATION=B; QUANTITY=25; PRICE=825;"
        self.transaction_string = "ACTION=NEW_ORDER; TRANS_ID=777; "
        classcode_string = "CLASSCODE=" + str(classcode) + "; "
        seccode_string = "SECCODE=" + str(seccode) + "; "
        self.transaction_string = self.transaction_string + classcode_string + seccode_string
        account_string = "ACCOUNT=L01-00000F00; " # for BCS broker
        client_code_string = "CLIENT_CODE=" + str(client_code)+"; "
        self.transaction_string = self.transaction_string + account_string + client_code_string
        type_string = "TYPE=L; "
        operation_string =  "OPERATION=" + str(operation) + "; "
        self.transaction_string = self.transaction_string + type_string + operation_string
        quantity_string = "QUANTITY=" + str(quantity) + "; "
        price_string = "PRICE=" + str(price) + "; "
        self.transaction_string = self.transaction_string + quantity_string + price_string
        
        print(self.transaction_string)

        FunctionResult = Trans2Quik._TRANS2QUIK_SEND_ASYNC_TRANSACTION(bytes(self.transaction_string,'ascii'),
                                                    ctypes.byref(self.pnExtendedErrorCode), 
                                                    self.lpstrErrorMessage, 
                                                    self.dwErrorMessageSize)

        print("send_async_transaction:")
        print("FunctionResult = ", FunctionResult)
        print("ErrorCode =", self.pnExtendedErrorCode.value)
        print("error = ", self.lpstrErrorMessage.value,"\n")


    def command_to_transaction(self, command):
        """ """
        seccode = command[0]
        operation = command[1]
        price = command [2]
        quantity = command[3]
        price_threshold = 0.02

        if seccode == '':
            print('Тикер инструмента не определен!')
        elif operation == '':
            print('Направление заявки не определено!')
        elif quantity == 0: 
            print('Количество лотов заявки не определено!')
        elif price == 0:
            print("Цена заявки не определана!")
        else:
            last_price = float(self.quik_provider.GetParamEx(self.class_code, seccode, 'LAST')['data']['param_value'])
            if price > last_price * (1 + price_threshold) or price < last_price * (1 - price_threshold):
                print(f"Значение цены операции находится за пределами диапазона в {price_threshold * 100}% относительно текущей цены {last_price} инструмента {seccode} ")
            else:

                for _account in self.accounts:
                    self.quik_api_send_async_transaction(self.class_code, seccode , _account, operation, quantity , price)



    def info_tickers(self, tickers, ticker_prefix):
        """ Getting information for the tickers """
        info = {}
        for ticker in tickers:
            i = self.store.get_symbol_info(ticker)
            info[f"{ticker_prefix}{ticker}"] = i
        return info
    
    def get_account_total_value(self, account):
        """ Getting the cash position and total value of account """
        for _accounts_cash in self.accounts_cash:
            if ((_accounts_cash.get('client_code') == account) and (_accounts_cash.get('limit_kind') == 2)
                        and (_accounts_cash.get('tag')=='EQTV') and (_accounts_cash.get('currcode')=='SUR')):
                cash = _accounts_cash.get('currentbal')
                total_account_value = cash
                for _position in self.depo_limits:
                    if (_position.get('client_code') == account and _position.get('limit_kind') == 2 and int(_position.get('currentbal')) > 0):
                        last_price = float(self.quik_provider.GetParamEx(self.class_code, _position.get('sec_code'), 'LAST')['data']['param_value'])  # last price
                        total_account_value = total_account_value +  int(_position.get('currentbal')) * last_price

        return cash, total_account_value


    def open_positions_random_qauntity(self, tickers, min_qauntity=1, max_quantity=100):

        list_tickers = []
        for _ticker in tickers:
            list_tickers.append(_ticker)
        if list_tickers == None:
            print('Список тикеров пуст')

        else: 
            info = self.info_tickers(list_tickers, self.ticker_prefix)

            for _account in self.accounts:
                cash, total_account_value = self.get_account_total_value(_account)
                for _ticker in tickers:
                
                    quantity = random.randint(min_qauntity, max_quantity)
            
                    last_price = float(self.quik_provider.GetParamEx(self.class_code, _ticker, 'LAST')['data']['param_value'])
                    # for position in self.depo_limits:
                    #     if (position.get('client_code') == _account and position.get('limit_kind') == 2):
                    #         current_position = position.get('currentbal') * last_price
                    # print(current_position)
                    if (cash > (quantity * last_price)):

                        self.quik_api_send_async_transaction(self.class_code, _ticker, _account, 'B', quantity, last_price)
                        time.sleep(0.05)


    def open_positions_fix_qauntity(self, tickers, qauntity=1):
        pass




    def close_all_positions(self):
        
        positions = []
        for _account in self.accounts:
            for _position in self.depo_limits:
                if (_position.get('client_code') == _account and _position.get('limit_kind') == 2 and int(_position.get('currentbal')) > 0):
                    positions.append(_position.get('sec_code'))
                                                
        print(positions)
        if positions == None:
            print('Нет открытых позиций для входящих счетов!')
        else:
            info = self.info_tickers(positions, self.ticker_prefix)
            for _account in self.accounts:
                print('acs')
                for _position in self.depo_limits:
                    print('pos')
                    if (_position.get('client_code') == _account and _position.get('limit_kind') == 2 and int(_position.get('currentbal')) > 0):
                            print('bal')
                            if str(_position.get('sec_code') + self.ticker_prefix) in info:
                                last_price = float(self.quik_provider.GetParamEx(self.class_code, _position.get('sec_code'), 'LAST')['data']['param_value'])
                                info = self.info_tickers(_position, self.ticker_prefix)
                                quantity = int(_position.get('currentbal') / info[str(self.ticker_prefix + _position.get('sec_code'))]['securities']['LOTSIZE'])
                                self.quik_api_send_async_transaction(self.class_code, _position.get('sec_code'), _account, 'S', quantity, last_price)

    def close_some_positions(self, tickers):

        info = self.info_tickers(tickers, self.ticker_prefix)
        print(info)
        #print(tickers)
        for _account in self.accounts:      
            for _position in self.depo_limits:
                print(_position)

                if (_position.get('client_code') == _account and _position.get('limit_kind') == 2 and int(_position.get('currentbal'))> 0):
                        print('11')
                        if str(_position.get('sec_code') + self.ticker_prefix) in info:

                            last_price = float(self.quik_provider.GetParamEx(self.class_code, _position.get('sec_code'), 'LAST')['data']['param_value'])
                            quantity = int(_position.get('currentbal') / info[str(self.ticker_prefix + _position.get('sec_code'))]['securities']['LOTSIZE'])
                            self.quik_api_send_async_transaction(self.class_code, _position.get('sec_code'), _account, 'S', quantity, last_price)
                            time.sleep(0.05)
                        else:
                            print('Такого эмитента нет в портфеле')


    def reduce_some_positions(self, tickers):
        pass


    
    def format_price(self, ticker, price):
        """
        The function of rounding up the price step by keeping the signs of decimal places
        print(round_custom_f(0.022636, 0.000005, 6)) --> 0.022635
        """
        step = self.p.info_tickers[ticker]['securities']['MINSTEP']  # we keep the minimum price step
        signs = self.p.info_tickers[ticker]['securities']['DECIMALS']  # we keep the number of decimal places
        

        val = round(price / step) * step
        return float(("{0:." + str(signs) + "f}").format(val))

        
    def close_connection(self):
        self.quik_provider.CloseConnectionAndThread()
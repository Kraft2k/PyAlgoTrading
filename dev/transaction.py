import ctypes
from ctypes import *
from ctypes import wintypes
from pathlib import Path


import random
import time
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../QuikPy"))
from QuikPy import QuikPy  # Working with QUIK from Python via QuikSharp LUA scripts

class Trans2Quik:

    LIB_QUIK_API = cdll.LoadLibrary(r"C:\Trans2QuikAPI\trans2quik.dll")

    PATH_2_QUIK = "C:/BCS_Work/QUIK_BCS/"
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
    
    def __init__(self, accounts):
        
        self.quik_provider = QuikPy()
        self.class_code = 'TQBR'

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


    def quik_api_send_async_transaction(self, ticker, client_code, operation, quantity, price):

        # transaction_string = b"ACTION=NEW_ORDER; TRANS_ID=888; CLASSCODE=TQBR; SECCODE=SIBN; ACCOUNT=L01-00000F00; CLIENT_CODE=2007693; TYPE=L; OPERATION=B; QUANTITY=25; PRICE=825;"
        self.transaction_string = "ACTION=NEW_ORDER; TRANS_ID=777; CLASSCODE=TQBR; "
        seccode_string = "SECCODE=" + str(ticker) + "; "
        self.transaction_string = self.transaction_string + seccode_string
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


    def get_account_total_value(self, account):
        """ """
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


    def open_positions(self, tickers, percentage):

        _tickers = tickers
        _percentage = percentage
        t0 = time.time()
        for _account in self.accounts:
            cash, total_account_value = self.get_account_total_value(_account)
            for _position in _tickers:
                quantity = random.randint(9, 60)
                last_price = float(self.quik_provider.GetParamEx(self.class_code, _position, 'LAST')['data']['param_value'])
                for position in self.depo_limits:
                    if (position.get('client_code') == _account and position.get('limit_kind') == 2):
                        current_position = position.get('currentbal') * last_price
                #print(current_position)
                if (cash > (quantity * last_price)) and (current_position < _percentage * total_account_value):
                    self.quik_api_send_async_transaction(_position, _account, 'B', quantity, last_price)
                    time.sleep(0.02)


    def close_all_positions(self):

        for _account in self.accounts:
            for _position in self.depo_limits:
                if (_position.get('client_code') == _account and _position.get('limit_kind') == 2 and int(_position.get('currentbal')) > 0):
                        last_price = float(self.quik_provider.GetParamEx(self.class_code, _position.get('sec_code'), 'LAST')['data']['param_value'])

                        self.quik_api_send_async_transaction(_position.get('sec_code'), _account, 'S', int(_position.get('currentbal')), last_price)
                        time.sleep(0.02)

    def close_some_positions(self, tickers):
        _tickers = tickers
        for _account in self.accounts:
            for _position in _tickers:
                if (_position.get('client_code') == _account and _position.get('limit_kind') == 2 and int(_position.get('currentbal')) > 0):
                        last_price = float(self.quik_provider.GetParamEx(self.class_code, _position.get('sec_code'), 'LAST')['data']['param_value'])

                        self.quik_api_send_async_transaction(_position.get('sec_code'), _account, 'S', int(_position.get('currentbal')), last_price)
                        time.sleep(0.02)

    def reduce_some_positions(self):
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


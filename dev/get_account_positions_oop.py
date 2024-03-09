import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../QuikPy"))

from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp


    
class GetAccountPosition:
    """ Get account positions from the moex equities market"""

    def __init__(self, account):

        self.qp_provider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK
        self.class_code = 'TQBR' # moex equities market
        is_account = False
        self.account = account
        self.account_positions = {'cash': 0.0}

        self.accounts = self.qp_provider.GetClientCodes()['data']
        self.accounts_positions = {}

        for _account in self.accounts:
            if _account == self.account:
                is_account = True

        
        if not is_account:
            print(f'Account : {self.account}  is not available!')
            self.qp_provider.CloseConnectionAndThread()
            exit()
            

        print(self.accounts)
        print(self.accounts[0])
        self.accounts_cash = self.qp_provider.GetMoneyLimits()['data']
        self.depo_limits = self.qp_provider.GetAllDepoLimits()['data']
        self.total_account_value = 0.0
        self.account_cash = 0.0

    def get_cash(self):
        ''''''
        for _account_cash in self.accounts_cash:
            if ((_account_cash.get('client_code') == self.account) and (_account_cash.get('limit_kind') == 2)
                and (_account_cash.get('tag')=='EQTV') and (_account_cash.get('currcode')=='SUR')):
                self.account_positions['cash'] = _account_cash.get('currentbal')
                print(self.account_positions['cash'])
                
        self.total_account_value = self.account_positions['cash']

    def get_positions(self):
        print(f'Account : {self.account}')
        print('Cash : ',format(self.account_positions['cash']))
        print('Ticker : Quantity : Last')
        for positions in self.depo_limits:
            if (positions.get('client_code') == self.account and positions.get('limit_kind') == 2):
                last_price = float(self.qp_provider.GetParamEx(self.class_code, positions.get('sec_code'), 'LAST')['data']['param_value'])  # last price
                self.account_positions[positions.get('sec_code')] = int(positions.get('currentbal'))
                print(self.account_positions)
                print(f"{positions.get('sec_code')}  : {int(positions.get('currentbal'))} : {last_price}")
                self.total_account_value = self.total_account_value + (positions.get('currentbal') * last_price)
        print(f'Total account value : {self.total_account_value}')
        
    def close_connection(self):
        self.qp_provider.CloseConnectionAndThread()

if __name__ == '__main__':

    portfolio = GetAccountPosition('2007693')
    portfolio.get_cash()
    portfolio.get_positions()
    portfolio.close_connection()



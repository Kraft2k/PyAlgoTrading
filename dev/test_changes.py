import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../QuikPy"))

from QuikPy import QuikPy  # Working with QUIK from Python via QuikSharp LUA scripts

if __name__ == '__main__':  
    
    qp_provider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK

    class_code = 'TQBR'
    account = '2007695'
    accounts = qp_provider.GetClientCodes()['data']
    print(accounts)
    accounts_cash = qp_provider.GetMoneyLimits()['data']
    #print(accounts_cash[1])
    depo_limits = qp_provider.GetAllDepoLimits()['data']
    
    # for client_cash in accounts_cash:
    #     if (client_cash.get('client_code') == accounts[1]):
    #             print(client_cash)

    #print(depo_limits[0])
    total_account_value = 0.0
    account_cash = 0.0
    for _account_cash in accounts_cash:
        if ((_account_cash.get('client_code') == account) and (_account_cash.get('limit_kind') == 2)
             and (_account_cash.get('tag')=='EQTV') and (_account_cash.get('currcode')=='SUR')):
            account_cash = _account_cash.get('currentbal')
    total_account_value = account_cash
    print(f'Account : {account}')
    print(f'Cash : {account_cash}')
    print('Ticker : Quantity : Last')
    for positions in depo_limits:
        if (positions.get('client_code') == account and positions.get('limit_kind') == 2):
            last_price = float(qp_provider.GetParamEx(class_code, positions.get('sec_code'), 'LAST')['data']['param_value'])  # last price
            print(f"{positions.get('sec_code')}  : {int(positions.get('currentbal'))} : {last_price}")
            total_account_value = total_account_value + (positions.get('currentbal') * last_price)
    print(f'Total account value : {total_account_value}')

    
    portfolio = qp_provider.GetPortfolioInfoEx('NC0058900000','108098', 2, trans_id=0)['data']
    print(portfolio)
    change = portfolio.get('rate_change')
    print(change)



    qp_provider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy из любого экземпляраm,.
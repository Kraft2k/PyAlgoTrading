import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../QuikPy"))

from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp




# def GetMoney(self, client_code, firm_id, tag, curr_code, trans_id=0):  # 1
#         """Денежные позиции"""
#         return self.process_request({'data': f'{client_code}|{firm_id}|{tag}|{curr_code}', 'id': trans_id, 'cmd': 'getMoney', 't': ''})


if __name__ == '__main__':  # Точка входа при запуске этого скрипта
    
    qp_provider = QuikPy()  # Вызываем конструктор QuikPy с подключением к локальному компьютеру с QUIK

    class_code = 'TQBR'
    clients_code = qp_provider.GetClientCodes()['data']
    print(clients_code)
    clients_cash = qp_provider.GetMoneyLimits()['data']
    print(clients_cash[0])
    depo_limits = qp_provider.GetAllDepoLimits()['data']
    
    for client_cash in clients_cash:
        if (client_cash.get('client_code') == clients_code[0]):
                print(client_cash)

    #print(depo_limits[0])
    portfolio_value = 0.0
    portfolio_cash = 0.0
    for client_cash in clients_cash:
        if ((client_cash.get('client_code') == clients_code[0]) and (client_cash.get('limit_kind') == 2) and (client_cash.get('tag')=='EQTV') and (client_cash.get('currcode')=='SUR')):
            portfolio_cash = client_cash.get('currentbal')
    portfolio_value = portfolio_cash
    print(portfolio_cash)
    print('Tiker : Bal : ')
    for positions in depo_limits:
        if (positions.get('client_code') == clients_code[0] and positions.get('limit_kind') == 2):
            last_price = float(qp_provider.GetParamEx(class_code, positions.get('sec_code'), 'LAST')['data']['param_value'])  # last price
            print(f"{positions.get('sec_code')}  : {int(positions.get('currentbal'))} : {last_price}")
            portfolio_value = portfolio_value + (positions.get('currentbal') * last_price)
    print(portfolio_value)
        
    qp_provider.CloseConnectionAndThread()  # Перед выходом закрываем соединение и поток QuikPy из любого экземпляраm,.
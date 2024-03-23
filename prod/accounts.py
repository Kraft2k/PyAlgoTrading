import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../QuikPy"))

from QuikPy import QuikPy  # Working with QUIK from Python via QuikSharp LUA scripts


class TablePositions():

    rows = [["account", "cash"], # Header of table
    ]

class GetAccountPosition:
    """ Get account positions from the moex equities market"""

    def __init__(self, accounts):
        self.qp_provider = QuikPy()  # Calling the QuikPy constructor with a connection to the local host with QUIK
        self.class_code = 'TQBR' # moex equities market
        
        accounts_from_quik = self.qp_provider.GetClientCodes()['data']
        for _account in accounts:
            if accounts_from_quik.count(_account) == 0:
                print(f'Ошибка: cчет {_account} не найден!')
                self.qp_provider.CloseConnectionAndThread()
                sys.exit(1)

        self.accounts = accounts
        self.is_header_row = True
        self.is_first_account_row = True

        self.account_positions = {'cash': 0.0}

        for _account in self.accounts:
            next_account_list = [_account]
            TablePositions.rows.append(next_account_list)
             
        self.accounts_cash = self.qp_provider.GetMoneyLimits()['data']
        self.depo_limits = self.qp_provider.GetAllDepoLimits()['data']
        self.total_account_value = 0.0
        self.account_cash = 0.0

    def __del__(self):
        print(str(self))

    def get_cash(self):
        """ Get the cash position of accounts """
        index = 1
        for _account in self.accounts:
            for _account_cash in self.accounts_cash:
                if ((_account_cash.get('client_code') == _account) and (_account_cash.get('limit_kind') == 2)
                    and (_account_cash.get('tag')=='EQTV') and (_account_cash.get('currcode')=='SUR')):
                    self.account_positions['cash'] = _account_cash.get('currentbal')
                    TablePositions.rows[index].append(self.account_positions['cash'])
                    #print(self.account_positions['cash'])
                    index += 1
                
        self.total_account_value = self.account_positions['cash']



    def build_table_positions(self):
        """ Building a table of accounts with positions """
        index_account = 1
        for _account in self.accounts:
            for positions in self.depo_limits:
                if (positions.get('client_code') == _account and positions.get('limit_kind') == 2):

                    # Check postions in first account and add to header account positions
                    if index_account == 1:
                        TablePositions.rows[0].append(positions.get('sec_code'))
                        TablePositions.rows[index_account].append(int(positions.get('currentbal')))

                    # Check position in other accounts and if not avalable in header add its
                    elif positions.get('sec_code') in TablePositions.rows[0]:
                        TablePositions.rows[index_account].append(0)
                    
                    elif positions.get('sec_code') not in TablePositions.rows[0]:
                        TablePositions.rows[0].append(positions.get('sec_code'))
                        TablePositions.rows[index_account].append(0)
            
            index_account += 1

        # Fill the cells with zeros to a uniform TablePositions
        for index_account in range(1, len(self.accounts)+1):
            for i in range(len(TablePositions.rows[0]) - len(TablePositions.rows[index_account])): TablePositions.rows[index_account].append(0)
            
    def get_positions(self):
        """ Getting8 the quantities of equities for each position of accounts """
        index_account = 1
        for _account in self.accounts:
            for positions in self.depo_limits:
                if (positions.get('client_code') == _account and positions.get('limit_kind') == 2):

                    # Fill in the ticker columns with the quantity of account positions
                    TablePositions.rows[index_account][TablePositions.rows[0].index(positions.get('sec_code'))] = int(positions.get('currentbal'))
            index_account += 1

    def get_portfolios_with_account_value(self):
        
        index_account = 1
        for _account in self.accounts:
            total_account_value = float(TablePositions.rows[index_account][1])
            index_position = 1
            for _position in TablePositions.rows[0][1:]: 
                last_price = float(self.qp_provider.GetParamEx(self.class_code, _position, 'LAST')['data']['param_value'])  # last price
                total_account_value = total_account_value + ((TablePositions.rows[index_account][index_position]) * last_price)
                index_position += 1
                
            TablePositions.rows[index_account].append(total_account_value)
            index_account += 1
            
        TablePositions.rows[0].append(str('Total value'))
        TablePositions.rows[0].append(str('change'))
        index_account = 1
        for _account in self.accounts:
            portfolio = self.qp_provider.GetPortfolioInfoEx('NC0058900000',_account, 2, trans_id=0)['data']
            TablePositions.rows[index_account].append(portfolio.get('rate_change'))
            index_account += 1

    def get_portfolios_as_percentage(self):
        """ Getting portfolio positions as a percentage """
        index_account = 1
        for _account in self.accounts:
            index_position = 1
            for _position in TablePositions.rows[0][1:(len(TablePositions.rows[0])-2)]: 
                last_price = float(self.qp_provider.GetParamEx(self.class_code, _position, 'LAST')['data']['param_value'])  # last price
                total_value_account = float(TablePositions.rows[index_account][(len(TablePositions.rows[0])-2)])
                if total_value_account == 0.0:
                    print(f'Ошибка: Стоимость портфеля для счета {_account} равна 0.0')

                else:
                    if index_position == 1:
                        position_percentage = float(TablePositions.rows[index_account][index_position]) /  total_value_account * 100
                    else:
                        position_percentage = float((TablePositions.rows[index_account][index_position])) * last_price / total_value_account  * 100
                if position_percentage == 0.0 :
                    TablePositions.rows[index_account][index_position] = str(' ')
                else:
                    TablePositions.rows[index_account][index_position] = format(position_percentage, ' .2f')
                index_position += 1
            index_account += 1

        # Remove the 'Total account value' column
        TablePositions.rows[0].pop((len(TablePositions.rows[0])-2))
        index_account = 1
        for _account in self.accounts:
            TablePositions.rows[index_account].pop((len(TablePositions.rows[0])-1))
            index_account += 1

    def close_connection(self):
        self.qp_provider.CloseConnectionAndThread()
        #self.qp_provider.__del__()
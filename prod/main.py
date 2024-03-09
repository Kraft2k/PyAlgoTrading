from transaction import Trans2Quik, TransactionUnit


if __name__ == '__main__':
    cur_accounts = ['1220166', '1311258', '1761021', '1946559', '1988370', '356046', '43816', '63031', ]
    my_account = ['108098', ]
    portfolio = TransactionUnit(my_account)
    portfolio.quik_api_connect()
    # cash, value = portfolio.get_account_total_value('2007695')
    #print(cash, value)
    #portfolio.close_all_positions()
    # portfolio.open_positions(["GMKN", ], 0.15)
    portfolio.close_connection()
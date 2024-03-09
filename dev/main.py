from transaction import Trans2Quik, TransactionUnit


if __name__ == '__main__':

    portfolio = TransactionUnit(['2007693', ])
    portfolio.quik_api_connect()
    # cash, value = portfolio.get_account_total_value('2007695')
    #print(cash, value)
    #portfolio.close_all_positions()
    portfolio.open_positions(["ALRS", ], 0.15)

    portfolio.close_connection()
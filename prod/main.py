from transactions import Trans2Quik, TransactionUnit


if __name__ == '__main__':
    cur_accounts = ['1946559', '1988370', '356046', '43816', '63031', ]
    my_account = ['108098', ]
    portfolio = TransactionUnit(['1761021', '356046', ])
    #portfolio = TransactionUnit('TQBR', [''])
    portfolio.quik_api_connect()

    #portfolio.close_some_positions(["CHMF", ])
    #portfolio.close_some_positions(['PLZL', 'ALRS', ])

    portfolio.close_all_positions()

    #portfolio.open_positions_random_qauntity(['SBER', ], 21, 100)

    portfolio.close_connection()
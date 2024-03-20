from transactions import Trans2Quik, TransactionUnit


import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))
sys.path.insert(1, os.path.join(sys.path[0], "../.."))



if __name__ == '__main__':
    cur_accounts = ['1220166', '1311258', '1761021', '1946559', '1988370', '356046', '43816', '63031', ]
    my_account = ['108098', ]
    accounts = ['356046', '43816', ]
    portfolio = TransactionUnit(accounts)
    portfolio.quik_api_connect()
    portfolio.close_some_short_positions(['SBER', ])
    portfolio.close_connection()

    

    
    

   

    



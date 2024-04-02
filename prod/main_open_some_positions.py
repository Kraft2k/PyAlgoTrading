from transactions import Trans2Quik, TransactionUnit


import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], ".."))
sys.path.insert(1, os.path.join(sys.path[0], "../.."))



if __name__ == '__main__':

    big1_accounts = ['1220166', '43816',  ]
    big2_accounts = ['1311258', '1761021', '321697', '356046',]
    big2_accounts = ['1988370', '224420', '63031', '1862020',]
    medium_accounts = ['108098', '2202763', '1946559', '1689321', '31753']
    small_accounts = ['1411251', '1701218', '697409']
    micro_accounts = ['170743', '2089746', '1753378', ]
    nano_accounts = ['29570']


    portfolio = TransactionUnit(big2_accounts)
    portfolio.quik_api_connect()
    #['YNDX','ASTR', 'CHMF', 'OZON', 'SNGSP']
    #(['PLZL', 'SVCB', ]
    portfolio.open_long_once_random_qauntity(['MTLRP', ], 17, 50, 125)
    portfolio.close_connection()

    

    
    

   

    



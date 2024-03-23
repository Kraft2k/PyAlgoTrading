from transactions import Trans2Quik, TransactionUnit
from read_params import read_params

if __name__ == '__main__':

    accounts = read_params('C:/PyAlgoTrading/prod/config/', 'accounts.txt')
    tickers = read_params('C:/PyAlgoTrading/prod/config/', 'tickers.txt')
    portfolio = TransactionUnit(accounts)
    portfolio.quik_api_connect()
    portfolio.open_long_block(tickers)
    portfolio.close_connection()
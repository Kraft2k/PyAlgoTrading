from transactions import Trans2Quik, TransactionUnit
import configparser



if __name__ == '__main__':


    config = configparser.ConfigParser()
    config.sections()
    config.read('C:/PyAlgoTrading/prod/config/big1_config.ini')


    #portfolio = TransactionUnit('TQBR', config['accounts'])
    print(config.sections())
 
    groups_accounts = [item for item in config.sections() if 'accounts' in item]

    # for i in config.sections():
    #     if str('accounts') in config.sections():
    #         list_accounts.append(i)

    print(groups_accounts)

    print(config['open_long_block']['tickers'])

    content = config['open_long_block']['tickers']
        
    # Разделяем содержимое файла на строки
    lines = content.split('\n')
    
    # Очищаем строки от лишних символов
    lines = [line.strip() for line in lines if line.strip()]
    
    # Преобразуем строки в элементы списка типа str
    tickers = list(map(str, lines))
    print(tickers)

    print(config['open_long_block']['percentage'])
    # for ticker in config['open_long_block']['tickers']:
    #     print(str(ticker))
    #portfolio.quik_api_connect()
    #portfolio.kill_all_orders('TQBR')
    #portfolio.open_long_block(tickers, 10, 300000)
    #portfolio.close_connection()
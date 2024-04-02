from transactions import Trans2Quik, TransactionUnit
import configparser



if __name__ == '__main__':


    config = configparser.ConfigParser()
    config.sections()
    config.read('C:/PyAlgoTrading/prod/config/big1_config.ini')


    portfolio = TransactionUnit('TQBR', config['accounts'])
    print(config.sections())
    print(config['open_long_block']['tickers'])

    content = config['open_long_block']['tickers']
        
    # Разделяем содержимое файла на строки
    lines = content.split('\n')
    
    # Очищаем строки от лишних символов
    lines = [line.strip() for line in lines if line.strip()]
    
    # Преобразуем строки в элементы списка типа str
    tickers = list(map(str, lines))
    print(tickers)

    print(config['open_long_block']['ratio'])
    # for ticker in config['open_long_block']['tickers']:
    #     print(str(ticker))
    portfolio.quik_api_connect()
    portfolio.open_long_block(tickers, 0.1, 100000)
    portfolio.close_connection()
import configparser

config = configparser.ConfigParser()
config['accounts'] = {

        '1220166': 'Elephant',
        '43816'  : 'Turtle',
}
config['open_long_block'] = {}


    



with open('C:/PyAlgoTrading/prod/config/big1_config.ini', 'w') as configfile:
  config.write(configfile)
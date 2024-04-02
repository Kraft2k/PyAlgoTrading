import configparser

config = configparser.ConfigParser()
config.sections()
config.read('C:/PyAlgoTrading/prod/config/config.ini')
print(config.sections())

accounts = []

for key in config['accounts']:
    accounts.append(str(key))
    print(config['accounts'].get(key))

print(accounts)
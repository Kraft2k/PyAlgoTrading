import configparser

config = configparser.ConfigParser()
config['accounts'] = {
        '108098' : 'Kangaroo',
        '1220166': 'Elephant',
        '1311258': 'Rhino',
        '1411251': 'Zebra',
        '1689321': 'Ant',
        '1701218': 'Dolphin',
        '170743' : 'Panda',
        '1753378': 'Giraffe',
        '1761021': 'Gorilla',
        '1862020': 'Whale',
        '1946559': 'Bear',
        '1988370': 'Flamingo',
        '2089746': 'Octopus',
        '2202763': 'Koala',
        '224420' : 'Spider',
        '29570'  : 'Capybara',
        '31753'  : 'Giraffe',
        '321697' : 'Sturgeon',
        '356046' : 'Pike',
        '43816'  : 'Turtle',
        '63031'  : 'Ladybug',
        '697409' : 'Gudgeon'
}

with open('C:/PyAlgoTrading/prod/config/config.ini', 'w') as configfile:
  config.write(configfile)
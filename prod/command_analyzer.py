########################
# Section word to number
#
russian_number_system = {
    'ноль':     0,
    'один':     1,
    'одна':     1,
    'два':      2,
    'две':      2,
    'три':      3,
    'четыре':   4,
    'пять':     5,
    'шесть':    6,
    'семь':     7,
    'восемь':   8,
    'девять':   9,
    'десять':   10,
    'одиннадцать':  11,
    'двенадцать':   12,
    'тринадцать':   13,
    'четырнадцать': 14,
    'пятнадцать':   15,
    'шестнадцать':  16,
    'семнадцать':   17,
    'восемнадцать': 18,
    'девятнадцать': 19,
    'двадцать':     20,
    'тридцать':     30,
    'сорок':        40,
    'пятьдесят':    50,
    'шестьдесят':   60,
    'семьдесят':    70,
    'восемьдесят':  80,
    'девяносто':    90,
    'сто':          100,
    'двести':       200,
    'триста':       300,
    'четыреста':    400,
    'пятьсот':      500,
    'шестьсот':     600,
    'семьсот':      700,
    'восемьсот':    800,
    'девятьсот':    900,
    'тысяча':       1000,
    'тысячи':       1000,
    'тысяч' :       1000,
    'миллион':      1000000,
    'миллионов':    1000000,
    'миллиард':     1000000000,
    'запятая': ',',
    'точка': '.'
}

decimal_words = ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']

"""
#TODO

"""


"""
function to form numeric multipliers for million, billion, thousand etc.

input: list of strings
return value: integer
"""


def number_formation(number_words):
    numbers = []
    for number_word in number_words:
        numbers.append(russian_number_system[number_word])
    if len(numbers) == 4:
        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]
    elif len(numbers) == 3:
        return numbers[0] + numbers[1] + numbers[2] # Внимание замена умножения на сложение
    elif len(numbers) == 2:
        if 100 in numbers:
            return numbers[0] + numbers[1]
        else:
            return numbers[0] + numbers[1]
    else:
        return numbers[0]


"""
function to convert post decimal digit words to numerial digits
input: list of strings
output: double
"""


def get_decimal_sum(decimal_digit_words):
    decimal_number_str = []
    for dec_word in decimal_digit_words:
        if(dec_word not in decimal_words):
            return 0
        else:
            decimal_number_str.append(russian_number_system[dec_word])
    final_decimal_string = '0.' + ''.join(map(str,decimal_number_str))
    return float(final_decimal_string)


"""
function to return integer for an input `number_sentence` string
input: string
output: int or double or None
"""


def word_to_num(number_sentence):
    if (type(number_sentence) is not str) or (number_sentence == ""):
        return 0
    #ValueError("Type of input is not string! Please enter a valid number word (eg. \'two million twenty three thousand and forty nine\')")

    number_sentence = number_sentence.replace('-', ' ')
    number_sentence = number_sentence.lower()  # converting input to lowercase

    if(number_sentence.isdigit()):  # return the number if user enters a number string
        return int(number_sentence)

    split_words = number_sentence.strip().split()  # strip extra spaces and split sentence into words
    if split_words[0] == "тысяча":
        number_sentence = "одна " + number_sentence
    split_words = number_sentence.strip().split()  # strip extra spaces and split sentence into words

    clean_numbers = []
    clean_decimal_numbers = []

    # removing and, & etc.
    for word in split_words:
        if word in russian_number_system:
            clean_numbers.append(word)

    # Error message if the user enters invalid input!
    if len(clean_numbers) == 0:
        return 0
    #ValueError("No valid number words found! Please enter a valid number word (eg. two million twenty three thousand and forty nine)") 

    # Error if user enters million,billion, thousand or decimal point twice
    if clean_numbers.count('тысяча') > 1 or clean_numbers.count('million') > 1 or clean_numbers.count('billion') > 1 or clean_numbers.count('point')> 1:
        return 0
    #ValueError("Redundant number word! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    # separate decimal part of number (if exists)
    if clean_numbers.count('point') == 1:
        clean_decimal_numbers = clean_numbers[clean_numbers.index('point')+1:]
        clean_numbers = clean_numbers[:clean_numbers.index('point')]

    billion_index = clean_numbers.index('billion') if 'billion' in clean_numbers else -1
    million_index = clean_numbers.index('million') if 'million' in clean_numbers else -1

    thousand_index = clean_numbers.index('тысяча') if 'тысяча' in clean_numbers else -1
    thousand_index = clean_numbers.index('тысяч') if 'тысяч' in clean_numbers else -1
    thousand_index = clean_numbers.index('тысячи') if 'тысячи' in clean_numbers else -1

    if (thousand_index > -1 and (thousand_index < million_index or thousand_index < billion_index)) or (million_index>-1 and million_index < billion_index):
        return 0
    #ValueError("Malformed number! Please enter a valid number word (eg. two million twenty three thousand and forty nine)")

    total_sum = 0  # storing the number to be returned

    if len(clean_numbers) > 0:
        # hack for now, better way TODO
        if len(clean_numbers) == 1:
                total_sum += russian_number_system[clean_numbers[0]]

        else:
            if billion_index > -1:
                billion_multiplier = number_formation(clean_numbers[0:billion_index])
                total_sum += billion_multiplier * 1000000000

            if million_index > -1:
                if billion_index > -1:
                    million_multiplier = number_formation(clean_numbers[billion_index+1:million_index])
                else:
                    million_multiplier = number_formation(clean_numbers[0:million_index])
                total_sum += million_multiplier * 1000000

            if thousand_index > -1:
                if million_index > -1:
                    thousand_multiplier = number_formation(clean_numbers[million_index+1:thousand_index])
                elif billion_index > -1 and million_index == -1:
                    thousand_multiplier = number_formation(clean_numbers[billion_index+1:thousand_index])
                else:
                    thousand_multiplier = number_formation(clean_numbers[0:thousand_index])
                total_sum += thousand_multiplier * 1000

            if thousand_index > -1 and thousand_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[thousand_index+1:])
            elif million_index > -1 and million_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[million_index+1:])
            elif billion_index > -1 and billion_index != len(clean_numbers)-1:
                hundreds = number_formation(clean_numbers[billion_index+1:])
            elif thousand_index == -1 and million_index == -1 and billion_index == -1:
                hundreds = number_formation(clean_numbers)
            else:
                hundreds = 0
            total_sum += hundreds

    # adding decimal part to total_sum (if exists)
    if len(clean_decimal_numbers) > 0:
        decimal_sum = get_decimal_sum(clean_decimal_numbers)
        total_sum += decimal_sum

    return total_sum
#
#
# Section audio string converting to QUIK string
#
quantity_key = ['количество']        # QUIK name  
price_key =    ['цена','цене']

_SECCODE = {
    'лукойл':   "LKOH",
    'лук':      "LKOH",
    'лука':     "LKOH",
    'сбербанк': "SBER",
    'сбер':     "SBER",
    'сбера':    "SBER"
}
_OPERATION = {
    'покупка': "B",
    'купить':  "B",
    'покупку': "B",
    'продажа': "S",
    'продать': "S",
    'продажу': "S"
}

def get_ticker_operation(split_audio_str,seccode_operation):

    clean_audio_str = []

    for word in split_audio_str:                 # set ticker, B/S
        if word in seccode_operation:
            clean_audio_str.append(word)
    if len(clean_audio_str) == 0:                # Error, ticker, B/S not found
        return ""
    
    ticker_bs = []

    for word in clean_audio_str:
        ticker_bs.append(seccode_operation[word])
    if (len(ticker_bs) == 0) or (len(ticker_bs) > 1):
        return ""
    else:
        return ticker_bs[0]
    
   
def get_price_quant(str_words,price_quant_key):
    many = 0

    for word in price_quant_key:
        if (word in str_words):
            many += 1
            i = str_words.index(word) 
    # нет кючевых слов или встречаются несколько раз
    if (many == 0 or many > 1):
        return ""                                       
    
    i += 1
    price_quant_str = []   

    while str_words[i] in russian_number_system:
        price_quant_str.append(str_words[i])
        i += 1
        if i == len(str_words):
            break
    
    return " ".join(price_quant_str)
        
        
        
def audio_str_to_quik_str(audio_str):
    if (type(audio_str) is not str) or (len(audio_str) < 4):
        return ""
    
    audio_str = audio_str.lower()                # converting input to lowercase
    split_audio_str = audio_str.strip().split()  # strip extra spaces and split sentence into words
    
    result = []

    result.append(get_ticker_operation(split_audio_str,_SECCODE))             # ticker
    result.append(get_ticker_operation(split_audio_str,_OPERATION))           # B/S
    result.append(word_to_num(get_price_quant(split_audio_str,price_key)))    # price
    result.append(word_to_num(get_price_quant(split_audio_str,quantity_key))) # lot

    return result
########################
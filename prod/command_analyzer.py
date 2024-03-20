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
    'миллиард':     1000000000
}


"""
function to form numeric multipliers for million, billion, thousand etc.

input: list of strings
return value: integer
"""

def number_formation(number_words):
    numbers = []
    for number_word in number_words:
        numbers.append(russian_number_system[number_word])

    n = len(numbers)    
    
    match n:
        case 1:
           return numbers[0]
        case 2:
            if (1000 not in numbers) and (1000000 not in numbers):
                return numbers[0] + numbers[1]
            else:
                match numbers[0]:
                    case 1000:
                        return numbers[0] + numbers[1]
                    case 1000000:
                        return numbers[0] + numbers[1]
                    case _:
                        return numbers[0] * numbers[1]  
        case 3:
            if ((1000 not in numbers) and (1000000 not in numbers)): 
                return numbers[0] + numbers[1] + numbers[2]
            
            match numbers[0]:
                case 1000:
                    return numbers[0] + numbers[1] + numbers[2]
                case 1000000:
                    if numbers[2] == 1000:
                        return numbers[0] + (numbers[1] * numbers[2])
                    else:
                        return numbers[0] + numbers[1] + numbers[2]
            match numbers[1]:
                case 1000:
                    return (numbers[0] * numbers[1]) + numbers[2]
                case 1000000:
                    return (numbers[0] * numbers[1]) + numbers[2]
            match numbers[2]:
                case 1000:
                    return (numbers[0] + numbers[1]) * numbers[2] 
                case 1000000:
                    return (numbers[0] + numbers[1]) * numbers[2]
                case _:
                   return -3 
        case 4:
            match numbers[0]:
                case 1000:
                    return numbers[0] + numbers[1] + numbers[2] + numbers[3] 
                case 1000000:
                    if  numbers[3] == 1000:
                        return numbers[0] + (numbers[1] + numbers[2]) * numbers[3] # 1021000 
                    else:
                        return numbers[0] + numbers[1] + numbers[2] + numbers[3]   # 1001031
            match numbers[1]:
                case 1000:
                    return (numbers[0] * numbers[1]) + numbers[2] + numbers[3] 
                case 1000000:
                    if  numbers[3] == 1000:
                        return (numbers[0] * numbers[1]) + (numbers[2] * numbers[3]) # 7002000 
                    else:
                        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3]   # 7001100   
            match numbers[2]:
                case 1000:
                    return (numbers[0] + numbers[1]) * numbers[2] + numbers[3] 
                case 1000000:
                    return (numbers[0] + numbers[1]) * numbers[2] + numbers[3]
            match numbers[3]:
                case 1000:
                    return (numbers[0] + numbers[1] + numbers[2]) * numbers[3] 
                case 1000000:
                    return (numbers[0] + numbers[1] + numbers[2]) * numbers[3]    
                case _:
                    return -4
        case 5:
            match numbers[0]:
                case 1000:
                    return -5 
                case 1000000:
                    if  numbers[2] == 1000:
                        return numbers[0] + (numbers[1] * numbers[2]) + numbers[3] + numbers[4] # 1 002 032
                    if  numbers[3] == 1000:
                        return numbers[0] + (numbers[1] + numbers[2]) * numbers[3] + numbers[4] # 1 042 040
                    if  numbers[4] == 1000:
                        return numbers[0] + (numbers[1] + numbers[2] + numbers[3]) * numbers[4] # 1 342 000
                    else:
                        return numbers[0] + numbers[1] + numbers[2] + numbers[3] + numbers[4]   # 1 001 431  
            match numbers[1]:
                case 1000:
                    return (numbers[0] * numbers[1]) + numbers[2] + numbers[3] + numbers[4]
                case 1000000:
                    if  numbers[3] == 1000:
                        return (numbers[0] * numbers[1]) + (numbers[2] * numbers[3]) + numbers[4] # 9 002 300
                    if  numbers[4] == 1000:
                        return (numbers[0] * numbers[1]) + (numbers[2] + numbers[3]) * numbers[4] # 9 042 000
                    else:
                        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3] + numbers[4]   # 9 000 431  
            match numbers[2]:
                case 1000:
                    return (numbers[0] + numbers[1]) * numbers[2] + numbers[3] + numbers[4]
                case 1000000:
                    if  numbers[4] == 1000:
                        return (numbers[0] + numbers[1]) * numbers[2] + (numbers[3] * numbers[4])   # 99 00 2000
                    else:
                        return (numbers[0] + numbers[1]) * numbers[2] + numbers[3] + numbers[4]     # 99 000 640
            match numbers[3]:
                case 1000:
                    return (numbers[0] + numbers[1] + numbers[2]) * numbers[3] + numbers[4]
                case 1000000:
                    return (numbers[0] + numbers[1] + numbers[2]) * numbers[3] + numbers[4]   
            match numbers[4]:
                case 1000:
                    return -5 
                case 1000000:
                    return -5   
                case _:
                    return -5   
        case 6:
            match numbers[0]:
                case 1000:
                    return -6 
                case 1000000:
                    return -6 
            match numbers[1]:
                case 1000:
                    return -6 #(numbers[0] * numbers[1]) + numbers[2] + numbers[3] + numbers[4] + numbers[5]
                case 1000000:
                    if  numbers[3] == 1000:
                        return (numbers[0] * numbers[1]) + (numbers[2] * numbers[3]) + numbers[4] +numbers[5]  # 9 002 320
                    if  numbers[4] == 1000:
                        return (numbers[0] * numbers[1]) + (numbers[2] + numbers[3]) * numbers[4] + numbers[5] # 9 042 099
                    if  numbers[5] == 1000:
                        return (numbers[0] * numbers[1]) + (numbers[2] + numbers[3] + numbers[4]) * numbers[5] # 9 999 000
                    else:
                       return (numbers[0] * numbers[1]) + numbers[2] + numbers[3] + numbers[4] #+ numbers[5]   # 9 000 431  
            match numbers[2]:
                case 1000:
                    return (numbers[0] + numbers[1]) * numbers[2] + numbers[3] + numbers[4]+ numbers[5]
                case 1000000:
                    if  numbers[4] == 1000:
                        return (numbers[0] + numbers[1]) * numbers[2] + ((numbers[3] * numbers[4])) + numbers[5] # 99 002 300
                    if  numbers[5] == 1000:
                        return (numbers[0] + numbers[1]) * numbers[2] + ((numbers[3] + numbers[4])) * numbers[5] # 99 042 000
                    else:
                        return (numbers[0] + numbers[1]) * numbers[2] + numbers[3] + numbers[4] #+ numbers[5]     # 99 000 423
            match numbers[3]:
                case 1000:
                    return (numbers[0] + numbers[1] + numbers[2]) * numbers[3] + numbers[4]+ numbers[5]
                case 1000000:
                    if  numbers[5] == 1000:
                        return ((numbers[0] + numbers[1] + numbers[2]) * numbers[3]) + (numbers[4]* numbers[5]) # 999 002 000
                    else:
                        return ((numbers[0] + numbers[1] + numbers[2]) * numbers[3]) + numbers[4]  + numbers[5] # 999 001 100
            match numbers[4]:
                case 1000:
                    return -6 
                case 1000000:
                    return -6 
            match numbers[5]:
                case 1000:
                    return -6 
                case 1000000:
                    return -6 
                case _:
                    return -6     
        case 7:
            match numbers[0]:
                case 1000:
                    return -7
                case 1000000:
                    return -7
            match numbers[1]:
                case 1000:
                    return -7 #(numbers[0] * numbers[1]) + numbers[2] + numbers[3] + numbers[4] + numbers[5] + numbers [7]
                case 1000000:
                    if  numbers[3] == 1000:
                        return (numbers[0] * numbers[1]) + (numbers[2] * numbers[3]) + numbers[4] + numbers[5] + numbers[6] # 9 002 321
                    if  numbers[4] == 1000:
                        return (numbers[0] * numbers[1]) + (numbers[2] + numbers[3]) * numbers[4] + numbers[5] + numbers[6] # 9 042 999
                    if  numbers[5] == 1000:
                        return (numbers[0] * numbers[1]) + (numbers[2] + numbers[3] + numbers[4]) * numbers[5] + numbers[6] # 9 999 100
                    else:
                        return (numbers[0] * numbers[1]) + numbers[2] + numbers[3] + numbers[4] #+ numbers[5]  # 9 000 431 
            match numbers[2]:
                case 1000:
                    return (numbers[0] + numbers[1]) * numbers[2] + numbers[3] + numbers[4]+ numbers[5] # + number[6]
                case 1000000:
                    if  numbers[4] == 1000:
                        return (numbers[0] + numbers[1]) * numbers[2] + ((numbers[3] * numbers[4])) + numbers[5] + numbers[6] # 99 002 309
                    if  numbers[5] == 1000:
                        return (numbers[0] + numbers[1]) * numbers[2] + ((numbers[3] + numbers[4])) * numbers[5] + numbers[6] # 99 042 099
                    else:
                        return (numbers[0] + numbers[1]) * numbers[2] + numbers[3] + numbers[4]# + numbers[5]     # 99 000 423
            match numbers[3]:
                case 1000:
                    return (numbers[0] + numbers[1] + numbers[2]) * numbers[3] + numbers[4]+ numbers[5] + numbers[6]
                case 1000000:
                    if  numbers[5] == 1000:
                        return ((numbers[0] + numbers[1] + numbers[2]) * numbers[3]) + (numbers[4]* numbers[5]) + numbers[6] # 999 002 100
                    else:
                        return ((numbers[0] + numbers[1] + numbers[2]) * numbers[3]) + numbers[4]  + numbers[5] + numbers[6] # 999 001 120
            match numbers[4]:
                case 1000:
                    return -7
                case 1000000:
                    return -7 
            match numbers[5]:
                case 1000:
                    return -7 
                case 1000000:
                    return -7 
                case _:
                    return -7
        case _:
            return -100
 

"""
function to return integer for an input `number_sentence` string
input: string
output: int or double or None

"""

def word_to_num(number_sentence):
    
    if (type(number_sentence) is not str) or (number_sentence == ""):
        return 0
    #ValueError("Type of input is not string! Please enter a valid number word (eg. \'two million twenty three thousand and forty nine\')")

   # number_sentence = number_sentence.replace('-', ' ')
    number_sentence = number_sentence.lower()  # converting input to lowercase

    if(number_sentence.isdigit()):  # return the number if user enters a number string
        return int(number_sentence)
    
    split_words = number_sentence.strip().split()  # strip extra spaces and split sentence into words

    clean_numbers = []
    
    # removing and, & etc.
    for word in split_words:
        if word in russian_number_system:
            clean_numbers.append(word)

    # Error message if the user enters invalid input!
    if len(clean_numbers) == 0:
        return 0
    #ValueError("No valid number words found! Please enter a valid number word (eg. two million twenty three thousand and forty nine)") 

    total_sum = 0  # storing the number to be returned
    total_sum = number_formation(clean_numbers)
    
    return total_sum

#
# Section audio string converting to QUIK string
#
quantity_key = ['количество','количеством','количестве','количеству']          
price_key =    ['цена','цене','цену','ценой']
decimal_key =  ['запятая','точка','точкой']

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
    
    if len(str_words) == 1:
        return ""
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
    if i == len(str_words):
        return ""            
          
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
    result.append(word_to_num(get_price_quant(split_audio_str,quantity_key))) # lot
    result.append(word_to_num(get_price_quant(split_audio_str,price_key)))    # price
    result.append(word_to_num(get_price_quant(split_audio_str,decimal_key)))  # decimal price
    
    return result
########################
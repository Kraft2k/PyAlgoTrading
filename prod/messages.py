from colorama import Fore, Style


    # print('Формат сообщения для подачи заявки')
    # print('----------------------------------------')
    # print('направление : тикер : количество : цена')
    # print('----------------------------------------')
    # print('')
    # print('Примеры сообщений для подачи заявок:')
    # print('----------------------------------------')
    # print('купить лукойл цена 4300 количество 50')
    # print('сбер продать цена 300 количество 100')
    # print('----------------------------------------')
    # print('')

class CommandMessages:

    def greetings():
        print(f'Голосовая система поддержки принятия решений {Fore.GREEN}Axioma{Style.RESET_ALL} приветствует Вас!')
        print(f'')
        message = str('Голосовая система поддержки принятия решений Аксиома приветствует Вас!')
        return message

    def waiting_commands():
        print(f'Жду ваших команд!')
        print(f'')
        message = str('Жду Ваших команд!')
        return message


    def response_on_greeting():
        print(f'И Вам не болеть, желаю удачной торговли!')
        print(f'')
        message = str('И Вам не болеть, желаю удачной торговли!')
        return message 

    def response_on_how_are_you():
        print(f'У меня неплохо, надеюсь что сегодняшний день станет лучшим!')
        print(f'')
        message = str('У меня неплохо, надеюсь что сегодняшний день станет лучшим!')
        return message
    
    def response_on_exit():
        print(f'До свидания, до новых встреч!')
        print(f'')
        print(f'PS:')
        print(f'Если Вы обнаружили ошибки или есть предолжения по увеличению функционала,')
        print(f'оставляйте комментарии на  {Fore.GREEN}t.me/axiomabroker{Style.RESET_ALL} или пишите на {Fore.GREEN}kraft2k@yandex.ru{Style.RESET_ALL}')
        print(f'')
        message = str('До свидания, до новых встреч!')
        return message
    
    def ask_Alice():
        print(f'К сожалению у меня нет ответа, лучше спросите у  {Fore.GREEN}Алисы{Style.RESET_ALL}!')
        print(f'')
        message = str('К сожалению у меня нет ответа, лучше cпросите у Алисы!')
        return message
    
    def off_voice_messages():
        print(f'Конечно, я лучше помолчу!')
        print(f'')
        message = str('Конечно, я лучше помолчу!')
        return message

    def on_voice_messages():
        print(f'Буду очень рада вновь пообщаться с Вами!')
        print(f'')
        message = str('Буду очень рада вновь пообщаться с Вами!')
        return message

    def help_list():
        print(f'Доступные голосовые команды:')
        print(f'--------------------------------------------------------------------')
        print(f'{Fore.GREEN}"Помощь"{Style.RESET_ALL} - показать список доступных голосовых команд.')
        print(f'{Fore.GREEN}"Выход"{Style.RESET_ALL} - выйти из программы.')
        print(f'{Fore.GREEN}"Выключить"{Style.RESET_ALL} - выключить голосовые сообщения {Fore.GREEN}Axioma{Style.RESET_ALL}.')
        print(f'{Fore.GREEN}"Включить"{Style.RESET_ALL} - включить голосовые сообщения {Fore.GREEN}Axioma{Style.RESET_ALL}.')
        print(f'{Fore.GREEN}"Изменить"{Style.RESET_ALL} - изменить текущую группу счетов.')
        print(f'{Fore.GREEN}"Показать"{Style.RESET_ALL} - показать состояние текущей группы счетов.')
        print(f'{Fore.GREEN}"Показать все"{Style.RESET_ALL} - показать состояние всех счетов.')
        print(f'{Fore.GREEN}"Очистить"{Style.RESET_ALL} - очистить окно терминала.')
        print(f'{Fore.GREEN}"Закрыть шорт весь"{Style.RESET_ALL} - выставить заявки на покупку всех открытых')
        print(f'                      шорт-позиций группы счетов по текущей цене.')
        print(f'{Fore.GREEN}"Закрыть лонг весь"{Style.RESET_ALL} - выставить заявки на продажу всех открытых')
        print(f'                      лонг-позиций группы счетов по текущей цене.')
        print(f'---------------------------------------------------------------------')
        print(f'')
        message = ('Доступные голосовые команды')
        return message

    def check_close_all_short_postions():
        print(f'Вы хотите закрыть все шорт-позиции для представленных выше счетов?')
        print(f'Cкажите {Fore.GREEN}"Исполнить"{Style.RESET_ALL} для подтверждения или {Fore.GREEN}"Нет"{Style.RESET_ALL} для отмены.')
        print(f'')
        message = str('Cкажите Исполнить для подтверждения или Нет для отмены.')
        return message

    def check_close_all_long_postions():
        print(f'Вы хотите закрыть все лонг-позиции для представленных выше счетов?')
        print(f'Cкажите {Fore.GREEN}"Исполнить"{Style.RESET_ALL} для подтверждения или {Fore.GREEN}"Нет"{Style.RESET_ALL} для отмены.')
        print(f'')
        message = str('Cкажите Исполнить для подтверждения или Нет для отмены.')
        return message

    def misundestanding():
        print(f'Команда не определена, повторите команду или скажите {Fore.GREEN}"Помощь"{Style.RESET_ALL}!')
        print(f'')
        message = str('Команда не определена, повторите команду или скажите Помощь')
        return message



import json, pyaudio
from vosk import Model, KaldiRecognizer
from transaction import Trans2Quik, TransactionUnit

from accounts import GetAccountPosition, TablePositions


from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import DataTable


model = Model('C:/PyAlgoTrading/prod/vosk-model-small-ru-0.22')
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

class TableApp(App):
    """"""
    def compose(self) -> ComposeResult:
        yield DataTable()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*TablePositions.rows[0])
        for row in TablePositions.rows[1:]:
            # Adding styled and justified `Text` objects instead of plain strings.
            styled_row = [
                Text(str(cell), justify="right") for cell in row
            ]
            table.add_row(*styled_row)
        #table.add_rows(TablePositions.rows[1:])
        table.zebra_stripes = True
        table.cursor_type = "column"

def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            answer = json.loads(rec.Result())
            if answer['text']:
                yield answer['text']



if __name__ == '__main__':

    big_accounts = ['1220166', '1311258', '1761021', '1946559', '1988370', '321697', '224420', '356046', '43816', '63031', ]
    cur_accounts = ['1220166', '1311258', '1761021', '1946559', '1988370', '356046', '43816', '63031', ]
    small_accounts = ['29570', '170743', '1411251', '1753378', ]
    portfolio = TransactionUnit(cur_accounts)
    portfolio.quik_api_connect()

    # cash, value = portfolio.get_account_total_value('2007695')
    #print(cash, value)
    #portfolio.close_all_positions()
    
    for text in listen():
        print(str(text))
    # with open ('data.txt', 'a') as f:
    #     f.write(str(text))
    #     f.write(' \n')

        match text:

            case "купить" | "купи":
                portfolio.open_positions(['SBER', 'PIKK' ], 35, 250)
                

            case "купить лукойл":
                portfolio.open_positions(['LKOH', ], 45, 155),
    

            case "показать портфель":
                portfolio.close_connection
                portfolio_info = GetAccountPosition() 
                portfolio_info.get_cash()
                portfolio_info.build_table_positions()
                portfolio_info.get_positions()
                portfolio_info.get_portfolios_with_account_value()
                portfolio_info.get_portfolios_as_percentage()

                #print(TablePositions.rows)
                app = TableApp()
                app.run()
                portfolio_info.close_connection()

            case "продать":
                pass

            case "выход":
                portfolio.close_connection()
                quit()

            case _:
                print('Команда не опознана')
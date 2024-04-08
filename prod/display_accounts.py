from accounts import GetAccountPosition, TablePositions

import configparser


from rich.text import Text
from textual.app import App, ComposeResult
from textual.widgets import DataTable

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

alias = {
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

# accounts = ['108098', '1220166', '1311258', '1411251',
#             '1689321', '1701218', '170743', '1753378',
#             '1761021', '1862020', '1946559', '1988370',
#             '2089746', '2202763', '224420', '29570', '31753',
#             '321697', '356046', '43816', '63031', '697409', ]



accounts_ = ['2007693', ]

if __name__ == '__main__':

    config = configparser.ConfigParser()
    config.sections()
    config.read('C:/PyAlgoTrading/prod/config/config.ini')

    #print(config.sections())

    portfolio = GetAccountPosition(config['accounts']) 
    portfolio.get_cash()
    portfolio.build_table_positions()
    portfolio.get_positions()
    portfolio.get_portfolios_with_account_value()
    portfolio.get_portfolios_as_percentage()

    #print(TablePositions.rows)
    app = TableApp()
    app.run()
    portfolio.close_connection()
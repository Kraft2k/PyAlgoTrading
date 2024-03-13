from accounts import GetAccountPosition, TablePositions


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

accounts = ['108098', '1220166', '1311258', '1411251',
            '1689321', '1701218', '170743', '1753378',
            '1761021', '1862020', '1946559', '1988370',
            '2089746', '224420', '29570', '31753',
            '321697', '356046', '43816', '63031', '697409', ]

if __name__ == '__main__':

    portfolio = GetAccountPosition('TQBR', accounts) 
    portfolio.get_cash()
    portfolio.build_table_positions()
    portfolio.get_positions()
    portfolio.get_portfolios_with_account_value()
    portfolio.get_portfolios_as_percentage()

    #print(TablePositions.rows)
    app = TableApp()
    app.run()
    portfolio.close_connection()
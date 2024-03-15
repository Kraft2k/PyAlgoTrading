from prettytable import PrettyTable
from accounts import GetAccountPosition, TablePositions

table = PrettyTable()

accounts_ = ['2007693', '2007695', ]


portfolio = GetAccountPosition(accounts_) 
portfolio.get_cash()
portfolio.build_table_positions()
portfolio.get_positions()
portfolio.get_portfolios_with_account_value()
portfolio.get_portfolios_as_percentage()
table.field_names = TablePositions.rows[0]

for i in range(1,len(accounts_) + 1):
    table.add_row(TablePositions.rows[i])

print(table)
from controller import historical
from config import connection
from database import db
from utils import mapper

data = historical.GetData(connection.client)
symbol = 'DOTUSDT'

print(symbol)


def extract():
    item = data.get_daily_by_symbol(symbol)
    return item


items = extract()

for i in items:
    i.append(symbol)
    db.insert_rows(i)

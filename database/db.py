from pony.orm import *

db = Database('sqlite', 'coins.db')


class Historical(db.Entity):
    OpenTime = Required(float)
    Open = Required(float)
    High = Required(float)
    Low = Required(float)
    Close = Required(float)
    Volume = Required(float)
    CloseTime = Required(float)
    QuoteAssetVolume = Required(float)
    NumberTraders = Required(int)
    TakerBuyBase = Required(float)
    TakerBuyQuote = Required(float)
    Ignore = Required(int)
    symbol = Required(str)
    ID = PrimaryKey(int, auto=True)


db.generate_mapping(create_tables=True)


@db_session
def insert_rows(rows):
    Historical(
        OpenTime=rows[0],
        Open=rows[1],
        High=rows[2],
        Low=rows[3],
        Close=rows[4],
        Volume=rows[5],
        CloseTime=rows[6],
        QuoteAssetVolume=rows[7],
        NumberTraders=rows[8],
        TakerBuyBase=rows[9],
        TakerBuyQuote=rows[10],
        Ignore=rows[11],
        symbol=rows[12]
    )


@db_session
def get_rows():
    return select(c for c in Historical)[:]
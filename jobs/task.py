import pandas as pd
from controller import historical
from config import connection
from prefect import task, Flow
from prefect.schedules import IntervalSchedule
from datetime import timedelta
from utils import graphics

data = historical.GetData(connection.client)
symbol = 'BTCUSDT'


@task(log_stdout=True)
def extract():
    items = data.get_current(symbol, minutes=60)
    dataframe = pd.DataFrame(items, columns=[])
    graphics.candelstick_chart(items, "")
    return items


def build_flow():
    schedule = IntervalSchedule(interval=timedelta(minutes=1))

    with Flow('Coins', schedule) as _flow:
        items = extract()

    return _flow


flow = build_flow()
flow.run()

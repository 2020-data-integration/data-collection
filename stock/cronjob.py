import tushare as ts
import pandas as pd
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from tqdm import tqdm
import os
import logging

logging.basicConfig(level=logging.INFO, filename="/usr/app/integration/cronjob/logfile", filemode="a+",
                    format="%(asctime)-15s %(levelname)-8s %(message)s")

ts_token = '53cd3b985c649c978160c6ec04bce24f4fbd2ebcb4673e8f2fba9a43'
influx_host = '47.101.33.219'
port = 8086
username = 'influx'
password = '2020liufeng'
db = 'stock'

ts.set_token(ts_token)
pro = ts.pro_api()

client = InfluxDBClient(influx_host, port, username, password, database=db)

now = datetime.utcnow() + timedelta(hours=8) - timedelta(days=1)
yesterday = now.strftime("%Y%m%d")
yesterday_dash = now.strftime("%Y-%m-%d")

def test_exists(measurement):
    res = client.query("select * from {} where time='{}' limit 1".format(measurement, yesterday_dash))
    return res


def stock_price():
    measurement = 'stock'

    if test_exists(measurement):
        logging.info('already exists stock price data for {}'.format(yesterday_dash))
        return

    df = pro.daily(trade_date=yesterday)
    df['trade_date'] = pd.to_datetime(df['trade_date'])

    logging.info('Got stock price data for {} with len: {}'.format(yesterday_dash, len(df)))

    js = df.to_dict('records')
    processed_js = []
    for record in js:
        time = record.pop('trade_date')
        companyId = record.pop('ts_code')
        processed_js.append({
            "measurement": measurement,
            "tags": {
                'companyId': companyId
            },
            "time": time,
            "fields": record
        })
    
    client.write_points(processed_js)

    logging.info('Successfully inserted')

def ann():
    measurement = 'announcement'

    if test_exists(measurement):
        logging.info('already exists announcement price data for {}'.format(yesterday_dash))
        return

    df = pro.anns(ann_date=yesterday)
    df['ann_date'] = pd.to_datetime(df['ann_date'])

    logging.info('Got announcement data for {} with len: {}'.format(yesterday_dash, len(df)))

    js = df.to_dict('records')
    processed_js = []
    for record in js:
        time = record.pop('ann_date')
        companyId = record.pop('ts_code')
        processed_js.append({
            "measurement": measurement,
            "tags": {
                'companyId': companyId
            },
            "time": time,
            "fields": record
        })
    
    client.write_points(processed_js)

    logging.info('Successfully inserted')


def main():
    stock_price()
    ann()
    

if __name__ == '__main__':
    main()
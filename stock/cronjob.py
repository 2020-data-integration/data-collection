import tushare as ts
import pandas as pd
from influxdb import InfluxDBClient
from datetime import datetime, timedelta
from tqdm import tqdm
import os

ts_token = os.getenv('TS_TOKEN')
influx_host = os.getenv('INFLUX_HOST')
port = int(os.getenv('PORT', 8086))
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')
db = 'stock'
measurement = 'stock'

ts.set_token(ts_token)
pro = ts.pro_api()

client = InfluxDBClient(influx_host, port, username, password, database=db)

now = datetime.utcnow() + timedelta(hours=8) - timedelta(days=1)
yesterday = now.strftime("%Y%m%d")

def main():
    df = pro.daily(trade_date=yesterday)
    df['trade_date'] = pd.to_datetime(df['trade_date'])

    print('Got data for {}'.format(yesterday))

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

    print('Successfully inserted')

if __name__ == '__main__':
    main()
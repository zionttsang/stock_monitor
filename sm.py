
from datetime import datetime, timedelta
import requests
import time
import pandas as pd
import json
# import sys
# sys.path.append("/mnt/c/0000/airflow/projects/stock_monitor/")
# from stock_monitor import get_latest_stock_zjc_disclosure

import subprocess

def send_wechat(msg, title = '新的交易披露通知'):
    token = '55a581896cbe4a0fa3537b66117fc71e'#前边复制到那个token
    # title = 
    content = msg
    template = 'html'
    url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}"
    print(url)
    r = requests.get(url=url)
    print("pushplus message sent... \n",r.text)

def get_latest_stock_zjc_disclosure():

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.79 Safari/537.36'
    }
    # config_path = './config/objects.xlsx'

    print(subprocess.call("gsutil cp gs://free-gcs/StockMonitor/stocks.txt ./",shell=True))
    time.sleep(5)
    #exit()
    # df = pd.read_table("./stocks.txt",sep="," , dtype=str, header=None)
    df = pd.read_table("./stocks.txt",sep="," , dtype=str, header=None)
    print('df:\n', df)
    
    msg = ""
    for stock in df.itertuples():
        stock_code = stock[2]
        # print('stock code:',stock_code[2])

        url_head = 'http://www.cninfo.com.cn/data20/tradeInformation/getExecutivesIncDecDetail?scode='
        res = requests.get(url_head+stock_code, headers)
        time.sleep(10)
        print("get data of {}.. status code: {}".format(stock_code,res.status_code))
        text = res.text
        new_text = json.loads(text)

        # get stock detail for msg.
        for record in new_text['data']['records']:
            print(f"{stock_code} does have data.")
            stock_name = record['SECNAME']
            trade_date = record['DECLAREDATE']
            market_volume = record['F006N']
            market_price = record['F008N']

            market_value = int(market_price*market_volume)
            today_date = str(datetime.now().strftime('%Y-%m-%d'))
            # if trade_date == "2012-09-18" or trade_date == "2022-03-01":
            if trade_date == today_date:
                print("today's date: ", today_date)
                msg = msg+'stock: {}, date: {} value: {} W \n'.format(stock_name, trade_date, market_value/10000)
    
    # send all info in one message is there is new declaration..
    if msg != "":
        print(msg) 
        send_wechat(msg)
    else:
        print("Batch run normally.")
        send_wechat(msg="Batch run normally.", title="No new Declaration...")



if __name__ == "__main__":
    get_latest_stock_zjc_disclosure()

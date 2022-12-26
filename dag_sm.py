from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

import requests
import time
import pandas as pd
import json
# import sys
# sys.path.append("/mnt/c/0000/airflow/projects/stock_monitor/")
# from stock_monitor import get_latest_stock_zjc_disclosure


def get_latest_stock_zjc_disclosure():

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.79 Safari/537.36'
    }
    # config_path = './config/objects.xlsx'

    # df = pd.read_table("./stocks.txt",sep="," , dtype=str, header=None)
    df = pd.read_table("/opt/airflow/dags/projects/stock_monitor/stocks.txt",sep="," , dtype=str, header=None)
    print('df:\n', df)
    
    for stock in df.itertuples():
        stock_code = stock[2]
        # print('stock code:',stock_code[2])

        url_head = 'http://www.cninfo.com.cn/data20/tradeInformation/getExecutivesIncDecDetail?scode='
        res = requests.get(url_head+stock_code, headers)
        time.sleep(1)
        print("status code: ",res.status_code)
        text = res.text
        new_text = json.loads(text)
        for record in new_text['data']['records']:
            stock_name = record['SECNAME']
            trade_date = record['DECLAREDATE']
            market_volume = record['F006N']
            market_price = record['F008N']

            market_value = int(market_price*market_volume)
            today_date = str(datetime.now().strftime('%Y-%m-%d'))
            if trade_date == "2012-09-18" or trade_date == "2022-03-01":
            # if trade_date == today_date:
                print("today's date: ", today_date)
                print('stock: {}, date: {} value: {} W'.format(stock_name, trade_date, market_value/10000))
       


# Following are defaults which can be overridden later on
default_args = {
    'owner': 'tsang',
    'depends_on_past': False,
    'start_date': datetime(2022, 12, 15),
    'email': ['schwarzen221@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

dag = DAG('sm', 'stock_monitor_v1',
    # start_date=datetime(2018, 10, 1),
    schedule_interval="@daily",
    default_args=default_args, catchup=False
    )

# t1 = BashOperator(
#     task_id='download_config',
#     bash_command="curl -O 'https://github.com/zionttsang/stock_monitor/raw/main/config/objects.xlsx'",
#     dag=dag)

t2 = PythonOperator(task_id="monitor_task",
                                        python_callable=get_latest_stock_zjc_disclosure,
                                        dag = dag)
# monitor_task
# t1>>t2
# t1>>[t2,t3]>>t4

# get_latest_stock_zjc_disclosure()
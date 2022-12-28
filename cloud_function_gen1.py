'''
REQUIREMENTS.TXT:
requests>=2.28.1
pandas>=1.4.4
fsspec>=2022.10.0
gcsfs>=2022.11.0

'''
import base64

from datetime import datetime
import requests
import time
import pandas as pd
import json


def send_wechat(msg, title):
    for i in range(1,10,1):
        token = '55a581896cbe4a0fa3537b66117fc71e'#前边复制到那个token
        title = title
        content = msg+"\n ---- trying time:"+str(i)
        template = 'html'
        url = f"https://www.pushplus.plus/send?token={token}&title={title}&content={content}&template={template}"
        print(url)
        r = requests.get(url=url)
        print("pushplus message sent... \n",r.text)
        r_json = json.loads(r.text)
        
        #in case push timeout.
        if str(r_json["code"])=="200":
            break;
        else:
            print("message push failed, try again after 5 seconds.")
            time.sleep(5)

def get_latest_stock_zjc_disclosure(event, context):
    pubsub_message = base64.b64decode(event['data']).decode('utf-8')
    print(pubsub_message)

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.79 Safari/537.36'
    }
    # config_path = './config/objects.xlsx'

    # print(subprocess.call("gsutil cp gs://free-gcs/StockMonitor/stocks.txt ./",shell=True))
    
    #exit()
    # df = pd.read_table("./stocks.txt",sep="," , dtype=str, header=None)
    df = pd.read_table("gs://free-gcs/StockMonitor/stocks.txt", sep=",", dtype=str, header=None)
    print('df:\n', df)
    # exit()
    
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
            #print(f"{stock_code} does have data.")
            stock_name = record['SECNAME']
            trade_date = record['DECLAREDATE']
            market_volume = record['F006N']
            market_price = record['F008N']

            market_value = int(market_price*market_volume)
            today_date = str(datetime.now().strftime('%Y-%m-%d'))
            # if trade_date == "2012-09-18" or trade_date == "2022-03-01":
            if trade_date == today_date:
                print("today's date: ", today_date)
                msg =msg+'{} [ date: {} value: {} W ]\n'.format(stock_name, trade_date, market_value/10000)
    
    # send all info in one message is there is new declaration..
    if msg != "":
        print(msg) 
        send_wechat(msg=msg, title = "!!! New Trading Declaration.")
    else:
        msg="Batch run normally."
        print(msg)
        send_wechat(msg=msg, title="No Declaration.")

# import base64

# def stock_monitor(event, context):
#     """Triggered from a message on a Cloud Pub/Sub topic.
#     Args:
#          event (dict): Event payload.
#          context (google.cloud.functions.Context): Metadata for the event.
#     """
#     pubsub_message = base64.b64decode(event['data']).decode('utf-8')
#     print(pubsub_message)
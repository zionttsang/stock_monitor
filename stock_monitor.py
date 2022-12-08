import csv
import sys
import json

import requests
import pandas as pd




def get_latest_stock_zjc_disclosure(headers, config_excel:str):
    df = pd.read_excel(config_excel,sheet_name='stocks',dtype=str)
    print('df:\n', df)
    
    for stock in df.itertuples():
        stock_code = stock[2]
        # print('stock code:',stock_code[2])

        url_head = 'http://www.cninfo.com.cn/data20/tradeInformation/getExecutivesIncDecDetail?scode='
        res = requests.get(url_head+stock_code, headers)
        text = res.text
        # print(text)
        new_text = json.loads(text)
        # jsonText = json.dumps(text)
        # print(new_text['data']['records'])
        for record in new_text['data']['records']:
            stock_name = record['SECNAME']
            trade_date = record['DECLAREDATE']
            market_volume = record['F006N']
            market_price = record['F008N']

            market_value = int(market_price*market_volume)
            print('stock: {}, date: {} value: {} W'.format(stock_name, trade_date, market_value/10000))


def getSP500list(p):
    url = "http://stock.finance.sina.com.cn/usstock/api/jsonp.php/IO.XSRV2.CallbackList['uOnBeR6QLQptOfWx']/US_CategoryService.getChengfen?page={}&num=20&sort=mktcap&asc=0&market=&id=&type=2".format(p)
    res = requests.get(url).text
    # res = requests.get(url.format(p)).text
    # print(res+'\n')  # 该处获得的数据与第3步网页获取一致
    res2 = res[res.find("[{"):-3]
    # print(res2+'\n') # 删除无关字符
    spList = json.loads(res2)
    # print(spList) # json格式

    contentList = []
    for s in spList:
        symbol = s.get('symbol')
        name = s.get('name')
        cname = s.get('cname')
        contentList.append((symbol, name, cname))
        # print(symbol,name,cname)  # 可以获取多种相关信息，此处只截取代码、英文名称和中文名
        # return(symbol,name,cname)  # 可以获取多种相关信息，此处只截取代码、英文名称和中文名
       # f.writelines(symbol + '\n') # 把股票代码逐行写入txt文档，保存在本地
    print(contentList)
    return contentList
# for p in range(1):
# getSP500list(1)

if __name__=="__main__":
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/67.0.3396.79 Safari/537.36'
    }
    config_path = './config/objects.xlsx'
    # config_path = '/Users/tsang/Desktop/stock_monitor/config/objects.xlsx'
    get_latest_stock_zjc_disclosure(headers ,config_path)
import csv
import sys
import json

import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import pandas as pd


def get_latest_stock_zjc_disclosure(config_excel:str):
    df = pd.read_excel(config_excel,sheet_name='stocks',dtype=str)
    print('df:\n', df)
    
    for stock in df.itertuples():
        stock_code = stock[2]
        # print('stock code:',stock_code[2])
        disclousure_url = 'http://www.cninfo.com.cn/new/disclosure/stock?stockCode=%s&orgId=9900023680#shareholdersIncreaseOrDecrease'%(stock_code)
        print(disclousure_url)
        
        # chrome_options = Options()
        # chrome_options.add_argument("--headless")
        # driver = webdriver.Chrome(executable_path=(r'C:\Program Files\Google\Chrome\Application\chromedriver.exe'), options=chrome_options)
        # driver.get(disclousure_url)
        # print(driver.page_source)

        # data = requests.get(url=disclousure_url)
        # print('data:\n',data.text)


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
    config_path = '.\\config\\objects.xlsx'
    get_latest_stock_zjc_disclosure(config_path)
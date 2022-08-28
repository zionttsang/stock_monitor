import csv
import requests

import requests
import json
import datetime

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
getSP500list(1)

# f.close()
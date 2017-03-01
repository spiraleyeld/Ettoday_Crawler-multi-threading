### 一般爬蟲方法
# -*- coding: utf-8 -*-
import requests as r
from bs4 import *
import json
import time

### 取得網頁的Url
def getUrl():
    Num = 1##input('Press Pages: ')
    Num = 10##int(Num)
    linkList = []
    for pageNum in range(1,Num+1):
        res = r.get('http://sports.ettoday.net/news-search.phtml?keywords=mlb&idx=1&kind=10&page={}'.format(pageNum))
        soup = BeautifulSoup(res.text, "lxml")
        aGroup = soup.select('a')
        for aTag in aGroup:
            if aTag.get('href').startswith('http://sports.ettoday.net/news/'):
                if aTag.get('href') not in linkList:
                    linkList.append(aTag.get('href'))
    getContent(linkList)



### 取得網頁的內容
def getContent(linkList):
    
    try:
        for url in linkList:
            NewsContent = {}
            res = r.get(url)
            soup = BeautifulSoup(res.text, 'lxml')

            ## 抓tag資料
            article=soup.select('.story > p')
            title=soup.select('.title')
            titleT =title[0].text.strip()
            date = soup.select('.date')
            dateTime =date[0].text.split('時間：')[1].strip()
            content = ''
            for tag in article:
                content+=tag.text

            ## 裝資料
            NewsContent['Title']=titleT
            NewsContent['Date']=dateTime
            NewsContent['Content']=content
            NewsContent['Link']=url
            wholeContent.append(NewsContent)

    ## 例外處理        
    except:
        print('error')
        x = 'error happened'
        ## 寫error進檔案
        with open('error.txt', 'a+') as f:
            f.write(" "+x+":"+url+" , ")


    ## 複寫資料（舊＋新）    
    with open('test1.json', 'w+',encoding= 'utf-8') as f:
        f.write(json.dumps(wholeContent, ensure_ascii=False))
    
    


    


print( "start parsing...")
tStart = time.time() # 起始時間
wholeContent = []
getUrl()
tEnd = time.time()  # 結束時間
print(len(wholeContent))
print ('Cost %d seconds' % (tEnd - tStart))  # 完成花費時間      

# -*- coding: utf-8 -*-
from bs4 import *
import urllib
import re
import time
import threading
from multiprocessing import Queue
import urllib.request
import requests as r
import json

### 宣告Queue類別
titles = Queue()
urls = Queue()
##semaphore = threading.Semaphore()

### 建立treading的類別(for Queue-urls)
class Parser1(threading.Thread):# 此為python繼承語法
    
    counter = 0
    def __init__(self, name): #constructor 接受 name 參數
        threading.Thread.__init__(self) # initialize super class
        self.name = name # 每條Parser的名子
    
    ### 執行緒start時的run方法
    def run(self): # thread啟動後執行函數
        ### 因為有放置網址在Queue中，故此時，將網址取出，開始跑爬蟲程式(parse1)
        while urls.empty() is False: #檢查titles queue不為空的話，獲取URL後parse
            ### 取出Queue:"urls"中網址指定給current_url
            current_url = urls.get()
            ## print(current_url)
            ### 使用爬蟲程式一
            parse1(current_url)
           
            
    


### 爬蟲器一:爬取需要的網址
def parse1(current_url):
    global counter
    
    try:
    
        res = r.get(current_url)
        soup = BeautifulSoup(res.text, "lxml")
        aGroup = soup.select('a')
        for aTag in aGroup:
            if aTag.get('href').startswith('http://sports.ettoday.net/news/'):
                if aTag.get('href') not in linkList:
                    linkList.append(aTag.get('href'))
 
    except:
        print('error')




### 建立treading的類別(for Queue-titles)
class Parser2(threading.Thread):# 此為python繼承語法
    
    counter = 0
    def __init__(self, name): #constructor 接受 name 參數
        threading.Thread.__init__(self) # initialize super class
        self.name = name # 每條Parser的名子
    
    ### 執行緒的run方法
    def run(self): # thread啟動後執行函數
 
        while titles.empty() is False: #檢查titles queue不為空的話，獲取URL後parse
            ### 取出Queue:"titles"中網址指定給current_url
            current_url = titles.get()
            ### 使用爬蟲程式二
            NewsContent = parse2(current_url)
            ### 使用wholeCount，將爬取的文章{}丟進陣列中
            wholeCount.append(NewsContent)
            ##print(NewsContent)
            
    
### 爬蟲器二:爬取需要的網頁內容
def parse2(current_url):
    global counter
    
    try:
    
        NewsContent = {}
        res = r.get(current_url)
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
        NewsContent['Link']=current_url
        
        ### 包裝完畢，要把{}資訊丟出去給wholeCount[]
        return NewsContent
 
    except:
        print('error')



        
#### 執行緒的主函數因為需求所以拆出main(Queue-urls:for url) 跟 sub(Queue-titles:for content, link, title)


### 次流程取文章-搭配parse2 parser2   
def sub():
    global wholeCount
    linkListSub = linkList
    for url in linkListSub:
        titles.put(url)
        
       
    threads2 = []
    
    ### 執行緒的數量
    ##turbo =input('Turbo (Max:3):')
    for j in range(10):
        c = Parser2('c' + str(j)) # 建立Parser物件
        c.start() # 啟動thread
        threads2.append(c)

    for thread in threads2:
        thread.join() # 主線程必須等到所有threads執行完畢才繼續執行


        
### 主流程取Url-搭配parse1 parser1     
def main():
    global wholeCount
    numStart =input('Press Start Page: ')
    numEnd =input('Press End Page: ')
    numStart = int(numStart)
    numEnd = int(numEnd)
    ### 先以迴圈將要使用的網址一一丟進Queue中
    for pageNum in range(numStart,numEnd+1):
        url = ('http://sports.ettoday.net/news-search.phtml?keywords=mlb&idx=1&kind=10&page={}'.format(pageNum))
        urls.put(url)
     
        
    ### 宣告一個空陣列來放tread  
    threads1 = []
    
    ### 執行緒的數量
    ##turbo =input('Turbo (Max:3):')
    for j in range(10):
        c = Parser1('c' + str(j)) # 建立Parser物件
        c.start() # 啟動thread
        threads1.append(c)

    for thread in threads1:
        thread.join() # 主線程必須等到所有threads執行完畢才繼續執行


### 流程控控管中心(main → sub)，程式是依照如下的順序執行        
if __name__ == '__main__':
 
    print( "start parsing...")
    tStart = time.time() # 起始時間
    ### 變數宣告於此，方法內可共用
    ### wholeCount = 所有的文章 linkList = 所有的 Url
    wholeCount = []
    linkList = []
    ### 流程一:獲取網址
    main()
    print('main_OK')
    ### 流程二:獲取網頁內容(文章)
    sub()
    print('sub_OK')
    ### 寫進檔案
    with open('Ettoday.json', 'w+',encoding= 'utf-8') as f:
        f.write(json.dumps(wholeCount, ensure_ascii=False))
    
    ### print出成功文章數(Ettoday一頁10張)，除以10可與page數核對
    print(len(wholeCount))
    tEnd = time.time()  # 結束時間
    print ('Cost %d seconds' % (tEnd - tStart))  # 完成花費時間
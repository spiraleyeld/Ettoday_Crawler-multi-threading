# -*- coding:utf-8 -*-
import pymongo
import requests as r
from bs4 import BeautifulSoup
import json

print('Start get my data!!!')

### 建立連線MongoDB
client = pymongo.MongoClient("x.x.x.x", 27017)
db = client['spadeAce']
collection = db.awsmongoEttoday

## eToday單一標題新聞擷取網址

### 預設用來比對 "歷史" 的裝網址陣列
dataList = []

### 預設用來比對 "當天自己" 的裝網址陣列
checkList = []

### 預設用來容納通過檢核1 & 檢合2 的new news
wholeContent = []

### 宣告全域變數
data = []

## Step1 建立空陣列 導入歷史新聞的url


with open('baseEttoday.json', 'r',encoding= 'utf-8') as f:
    try:
        data = json.load(f)
        print(type(data))
        for i in data:
            ### 將每一筆歷史網址放進陣列中，後面要比對
            dataList.append(i['Link'])         
    except:
        ### 此腳本第一次執行會有空值所以exception，或著是重複執行但沒有東西
        print('no data')


## Method:獲取網頁新聞網址
def eTodayNewsUrl(number):
    

    for page in range(1,number+1):
        ## get web infomation
        res = r.get('http://sports.ettoday.net/news-list/%E6%A3%92%E7%90%83/MLB/{}'.format(page))
        pageInfomation = 'http://sports.ettoday.net/news-list/%E6%A3%92%E7%90%83/MLB/{}'.format(page)
        soup = BeautifulSoup(res.text, 'lxml')
        ## 格式讀入
        soupPage = soup.select('.block_content')
        ## 主要網頁 後面要搭配標題網頁
        home = 'http://sports.ettoday.net'
        ## 因為網頁使用類別.block_countent 有數個範圍，故soupPage會是list
        for listNum in range(len(soupPage)):
            ## 每個範圍中因為同一個tag組成一list 所以要再用迴圈一一讀出
            item = soupPage[listNum].select('div > h3 > a')
            for i in item:
                href = i.get('href')
                ## 只有href中開頭為/news/才是需要的單一新聞標題＆網址
                if href.startswith('/news/'):
                    record =i.text.replace('\u3000',' ')
                    ## 此判定非常非常非常重要，如果新聞的資訊已經在陣列中就不添加進字典or陣列中
                    if collection.find_one({'Link':home+href}) == None:
                        if home+href not in dataList and home+href not in checkList:
                            checkList.append(home+href)
                            get_content(home+href)

                            ## 存字典 {標題：網址}


## Method:獲取新聞資訊加進陣列 wholeContent
def get_content(url):
 
    NewsContent = {}
    res = r.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
        ## 抓tag資料
    article = soup.select('.story > p')
    title = soup.select('.title')
    titleT = title[0].text.strip()
    date = soup.select('.date')
    dateTime = date[0].text.split('時間：')[1].strip()
    content = ''
    for tag in article:
        content+=tag.text
        ## 裝資料
    NewsContent['Title']=titleT
    NewsContent['Date']=dateTime
    NewsContent['Content']=content
    NewsContent['Link']=url
    wholeContent.append(NewsContent)

    print("========================================================")
    print(titleT)
    print(dateTime)
    print(content)
    print("========================================================")


### ---------------------程式的起點------------------------------

## 輸入想要搜尋的總頁數
pageTotal = 15  ##input('Page Total: ')
eTodayNewsUrl(pageTotal)        


## 將文章寫進檔案中 
print('New_Record_Count: ' + str(len(wholeContent)))
### 新舊資料合併
       
finalAll = data + wholeContent       

## 將文章寫進檔案中        
with open('baseEttoday.json', 'w+', encoding = 'utf-8') as f:
    f.write(json.dumps(finalAll, ensure_ascii=False))
    
        
## 將新資料新增進系統 並關閉mongoDB連線
try:
    collection.insert(wholeContent)
except:
    print('cannot do an empty bulk write')
client.close()

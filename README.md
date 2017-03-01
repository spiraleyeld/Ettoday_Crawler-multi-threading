# 本例主要提供Ettoday, Search欄位屬於MLB的相關新聞
# 使用的的爬蟲方式為 多執行緒(multi-threading)

主要針對的部分如下:

1.獲取想要標的物的網址 

2.透過步驟一的標的物網址獲取網頁內容

程式的流程為建立兩條Queue，分先後主次：

主Queue多緒爬urls（目標網址）

次Queue依照主Queue的urls多緒爬文章最後寫出檔案．

細項程式碼說明，請詳ettoday_crawler(multi).py : )

附上ettoday_crawler(normal) 版本供比較

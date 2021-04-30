# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 16:08:21 2021

@author: sungmin.hwang
"""

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import sys



def crawl(url):
    data = requests.get(url)
    #print(data)
    return data.content

def getProductInfo(li):
    info = li.find("div",{"class":"basicList_title__3P9Q7"})
    aTag = info.find('a',{"class":"basicList_link__1MaTN"})
    title = aTag["title"]
    link = aTag["href"]
    priceReload = li.find("span",{"class":"price_num__2WUXn"})
    price = priceReload.text
    price = price.replace(",","").replace(",","").replace(",","").replace("원","")
    
    #print(title, price, link)
    return {"title":title, "price":price,"link":link}


def parse(pageString):
    
    bsObj = BeautifulSoup(pageString, "html.parser")
    
    
    
    ul = bsObj.find('ul',{'class':'list_basis'})
    
    lis = ul.findAll('li',{"class":"basicList_item__2XT81"})
    products = []
    
    for li in lis:
        try:
            productInfo = getProductInfo(li)
            #print(productInfo)
            products.append(productInfo)

        except:
            pass
            
    #info = bsObj.find('div',{"class":"basicList_title__3P9Q7"})
    
    #aTag = info.find('a',{"class":"basicList_link__1MaTN"})
    #title = aTag["title"]
 #   price = bsObj.find('span',{"class":"price_num__2WUXn"}).text
   # link = aTag["href"]
    #print(priceReload)
    
    #print(title)
    
    
    #print(info)
    #productInfo = {"title":title, "price":price,"link":link}
    #print(productInfo)
    #print(title, price, link)
    
    return products

def getPageResult(pageNo, keyword):
    
    #url="https://search.shopping.naver.com/search/all?query=%EC%85%94%EC%B8%A0"
    url="https://search.shopping.naver.com/search/all?frm=NVSHATC&origQuery=%EC%85%94%EC%B8%A0&pagingIndex={}&pagingSize=40&productSet=total&query={}&sort=rel&timestamp=&viewType=list".format(pageNo, keyword)

    options = Options()
    options.headless = True
    
    path=("D:\\temp\\chromedriver.exe")
    driver = webdriver.Chrome(path, options = options)  #크롬 실행 안하는 옵션
    #driver = webdriver.Chrome(path) 
    print(url)
    driver.get(url)
    time.sleep(1)
    driver.execute_script("window.scrollBy(0,9300);")
    time.sleep(1)
    #pageString = crawl(url)
    pageString = driver.page_source
    
    products = parse(pageString)
    #print(products)
    #print(len(products))
    return products
    
pageResultTotal = []

for pageNo in range(1,10+1):
    pageResultTotal = pageResultTotal + getPageResult(pageNo, "청바지")
    
print(len(pageResultTotal))

import json
file = open("./청바지2.json", "w+")
file.write(json.dumps(pageResultTotal))


import pandas as pd

#dataframe => 표
df = pd.read_json("청바지2.json")
print(df.count())
    

def save(df, filename):
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer,'Sheet1')
    writer.save()
    
save(df, "./청바지2.xlsx")



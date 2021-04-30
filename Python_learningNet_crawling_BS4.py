# -*- coding: utf-8 -*-
"""
Created on Thu Apr 29 08:25:03 2021

@author: sungmin.hwang
"""

#crawling 
#crawl() -> 데이터 받아오기
#parse() -> 받아온 데이터에서 필요한 정보 뽑기
#crawl -> requests
#parse -> bs4

import requests
from bs4 import BeautifulSoup

def crawl(url):
    data = requests.get(url)
    #print(data)
    return data.content
    

def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    #print(bsObj)
    #price = bsObj.find('p',class_='no_today').find('span',class_='blind').get_text()
    price = bsObj.find('p', {"class":"no_today"}).find("span",{"class":"blind"}).text
    title = bsObj.find('div',{"class":"wrap_company"}).find('a').text
    code = bsObj.find('div',{"class":"description"}).find("span",{"class":"code"}).text
     
    
    img = bsObj.find('div',{"class":"description"}).find("img")
    # 테그가 하나만 있을 경우 딕셔너리 처럼 속성에서 alt를 키로 하는 값을 가져옴
    cate = img['alt']
    category = img['class'][0]
    
    
    #print(category)
    #blind = noToday.find("span",{"class":"blind"})
    #price = blind.text
    #print(blind)
    #print(price)
    return {"name":title, "price":price, "종목코드":code, "카테고리":cate, "catEng":category}


    
#url = "https://finance.naver.com/item/main.nhn?code=068270" #사이트 주소(google.com, naver.com 등)

def getCompanyInfo(code):
    url = "https://finance.naver.com/item/main.nhn?code=" #사이트 주소(google.com, naver.com 등)
    #readcode = input("입력받을 종목 코드(예:001360)")

    pageString = crawl(url+str(code))
    #print(pageString)

    companyInfo = parse(pageString)
    return companyInfo
    #print(companyInfo)


codes = ["001360","102940","000660"]

for code in codes:
    print(getCompanyInfo(code))
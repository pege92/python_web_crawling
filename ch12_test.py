# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 09:40:24 2021

@author: sungmin.hwang
"""

from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
query_txt = input("크롤링할 키워드=")
fx_name = input("xls로 저정할 경로=")

path=("D:\\temp\\chromedriver.exe")
driver = webdriver.Chrome(path)
driver.get("https://www.naver.com/")

time.sleep(2)
# query 검색창 ID
#검색버튼 ico_search_submit

element = driver.find_element_by_id("query")

element.send_keys(query_txt)
time.sleep(1)

driver.find_element_by_id("search_btn").click()

time.sleep(1)

html = driver.page_source

soup = BeautifulSoup(html,'html.parser')

content_list = soup.find('ul', class_= 'lst_total _list_base')





no=1
no2=[]
contents2=[]
title2=[]
date2=[]
nick2=[]
link2=[]

for i in content_list:
    try:
        title = i.find('a','api_txt_lines total_tit').get_text()
        #print('제목:',title.strip())
        title2.append(title)

        contents = i.find('div','api_txt_lines dsc_txt').get_text()
        #print('내용:',contents.strip())
        contents2.append(contents)

        date = i.find('span','sub_time sub_txt').get_text()
        #print('작성일자:',date.strip())
        date2.append(date)

        nick = i.find('a','sub_txt sub_name').get_text()
        #print('닉네임:',nick.strip())
        nick2.append(nick)
        

        link = i.find('a','api_txt_lines total_tit')
        #print('링크주소:',link['href'])
        link2.append(link['href'])
        
        no2.append(no)
        #print('\n')
        no += 1
    except :
        pass
    


import pandas as pd

korea_trip = pd.DataFrame()
korea_trip['번호'] = no2
korea_trip['제목'] = title2
korea_trip['내용'] = contents2
korea_trip['작성일자'] = date2
korea_trip['블로그닉네임'] = nick2
korea_trip['링크'] = link2


import xlwt
korea_trip.to_excel(fx_name)
print("xls 파일 저장경로=%s"%fx_name)

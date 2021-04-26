# -*- coding: utf-8 -*-
"""
Created on Mon Apr 26 19:55:29 2021

@author: pege9
"""

# 한겨레 신문 경제 분야 정보 수집하기

#Step 1. 필요한 모듈과 라이브러리를 로딩합니다.

from bs4 import BeautifulSoup
from selenium import webdriver
import os
import time
import sys
import re
import math
import numpy  
import pandas as pd  
import xlwt 
import random

#Step 2. 사용자에게 검색어 키워드를 입력 받습니다.
print("=" *80)
print(" 이 크롤러는 한겨레신문의 경제 분야 기사 정보를 수집합니다")
print("=" *80)
print("\n")

query_txt = '한겨레신문_경제뉴스'

url_1='http://www.hani.co.kr/arti/economy/economy_general/list'  
url_2 ='.html'

cnt = int(input('1.크롤링 할 뉴스의 건수는 몇건입니까?: '))
page_cnt = math.ceil(cnt / 15)

f_dir = input("2.파일을 저장할 폴더명만 쓰세요(예:c:\\temp\\):")
print("\n")

# Step 3. 파일 저장 관련 내용 설정
now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

os.makedirs(f_dir+s+'-'+query_txt)
os.chdir(f_dir+s+'-'+query_txt)

ff_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.txt'
fc_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.csv'
fx_name=f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.xls'

#Step 4. 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다.

s_time = time.time( )
path = "c:/temp/chromedriver_240/chromedriver.exe"
driver = webdriver.Chrome(path)
driver.set_page_load_timeout(20)

#Step 5. 실제 내용을 수집합니다.
count = 0

no2=[]         #번호
title2=[]      #제목
contents2=[]   #내용
cdate2=[]      #날짜

no= 1

for i in range(2,135) :
  
  full_url = url_1+str(i)+url_2
  
  driver.get(full_url)
  time.sleep(5)

  html = driver.page_source
  soup = BeautifulSoup(html, 'html.parser')
    
  article_result = soup.find('div','section-list-area ')
  ar_list2 = article_result.find_all('div','list')
    
  print("한겨레 신문 경제 뉴스 수집 중 =========================================================")

  for i in ar_list2:
        
        f = open(ff_name, 'a',encoding='UTF-8')
        
        #번호 
        no2.append(no)
        
        # 기사 제목 
        title = i.find('h4','article-title').get_text().replace("\n","")
        print(no,"기사제목: ",title)
        title2.append(title)
        f.write(str(no) +'*기사제목:' + title + "\n")
        
        # 기사 요약 내용
        contents = i.find('p','article-prologue').find('a').get_text()
        print('*요약내용:'+contents)
        contents2.append(contents)
        f.write('*요약내용' + ':' + contents + "\n")
        
        # 기사 날짜
        date = i.find('p','article-prologue').find('span','date').get_text()
        print('*게시날짜:'+date)
        cdate2.append(date)
        f.write('*게시날짜' + ':' + date + "\n")
        
        f.write("\n")
        
        print("\n")
        
        time.sleep(0.4)
        f.close( )
        
        count += 1
        no += 1
        
        if count == cnt :
            break

  if count == cnt :
            break    
        
  print("%s 건  완료========================================================" %count)
  time.sleep(2)
                                          
#Step 6. 출력 결과를 파일에 저장하기

han_news = pd.DataFrame()
han_news['번호']=no2
han_news['기사제목']=title2
han_news['요약내용']=contents2
han_news['게시날짜']=cdate2

# csv 형태로 저장하기
han_news.to_csv(fc_name,encoding="utf-8-sig",index=True)

# 엑셀 형태로 저장하기
han_news.to_excel(fx_name ,index=True)

# Step 7. 요약 정보 출력하기

e_time = time.time( )
t_time = e_time - s_time

print("\n") 
print("=" *80)
print("1.요청된 총 %s 건의 리뷰 중에서 실제 크롤링 된 리뷰수는 %s 건입니다" %(cnt,count))
print("2.총 소요시간은 %s 초 입니다 " %round(t_time,1))
print("3.파일 저장 완료: txt 파일명 : %s " %ff_name)
print("4.파일 저장 완료: csv 파일명 : %s " %fc_name)
print("5.파일 저장 완료: xls 파일명 : %s " %fx_name)
print("=" *80)
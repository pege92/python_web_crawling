# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 11:23:52 2021

@author: sungmin.hwang
"""

from bs4 import BeautifulSoup
from selenium import webdriver

import time
import sys


query_txt = input("크롤링할 키워드=")
f_name = input("저정할 경로=")

path=("D:\\temp\\chromedriver.exe")
#driver = webdriver.chrome(path)
driver = webdriver.Chrome(path)
driver.get("https://korean.visitkorea.or.kr")

time.sleep(2)
driver.find_element_by_xpath("/html/body/div[5]/div/div/div/button").click()


#search_button = driver.find_element_by_xpath("/html/body/header/div[5]/div/div/div//button")





element = driver.find_element_by_id("inp_search")

element.send_keys(query_txt)
time.sleep(1)
driver.find_element_by_link_text("검색").click()


time.sleep(1)

full_html = driver.page_source

soup = BeautifulSoup(full_html,'html.parser')

content_list = soup.find('ul', class_= 'list_thumType type1')

for i in content_list:
    print(i.text.strip())
    print("\n")


orig_stdout = sys.stdout

f = open(f_name, 'a', encoding='UTF-8')
sys.stdout = f
time.sleep(1)

html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
content_list = soup.find('ul', class_='list_thumType type1')
for i in content_list:
    print(i.text.strip())
    print("\n")


sys.stdout = orig_stdout
f.close()
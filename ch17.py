
#필요한 모듈과 라이브러리 로딩
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import math
import numpy
import pandas as pd
import random
import os
import re


#사용자에게 검색어 키워드를 입력받고 저장할 폴더와 파일명을 설정합니다.
print("="*80)
print(" 8.뉴스 기사의 댓글 정보 수집하기")
print("="*80)
print("\n")


#query_txt = input("크롤링할 키워드=")
query_txt = '뉴스기사댓글'
#query_url = input('1.댓글을 크롤링할 뉴스의 url을 입력하세요')
query_url = 'https://news.naver.com/main/ranking/read.nhn?mode=LSD&mid=shm&sid1=001&oid=009&aid=0004782015&rankingType=RANKING'
cnt = int(input('2. 크롤링할 건수는 몇건입니까?(10건 단위로 입력):'))
page_cnt = math.ceil(cnt/20)
f_dir = input("3.파일을 저장할 폴더명:")


#저장될 파일 위치와 이름을 지정
now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d'%(now.tm_year,now.tm_mon, now.tm_mday, now.tm_hour,now.tm_min,now.tm_sec)


os.makedirs(f_dir+s+'-'+query_txt)
os.chdir(f_dir+s+'-'+query_txt)

ff_name = f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.txt'
fc_name = f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.csv'
fx_name = f_dir+s+'-'+query_txt+'\\'+s+'-'+query_txt+'.xls'

#크롬 드라이버를 사용해서 웹 브라우저를 실행
s_time = time.time()

path=("D:\\temp\\chromedriver.exe")
driver = webdriver.Chrome(path)
driver.get(query_url)
time.sleep(5)

#현재 총 리뷰 건수를 확인하여 사용자의 요청건수와 비교 후 동기화
html = driver.page_source
soup = BeautifulSoup(html,'html.parser')
result = soup.find('div',class_='u_cbox_head').find('span','u_cbox_count').get_text()

print("="*80)
result3 = result.replace(".","")
result4 = re.search("\d+",result3)
search_cnt = int(result4.group())

if(cnt>search_cnt):
    cnt = search_cnt
    
print("전체 검색 결과 건수:",search_cnt,"건")
print("실제 최종 출력 건수",cnt)
print("실제 출력될 최종 페이지수",page_cnt)

#사용자가 요청한 건수가 많을 경우 리뷰 더보기 버튼을 클릭합니다. 
driver.find_element_by_xpath('''//*[@id="cbox_module"]/div[2]/div[9]/a/span[1]''').click()
time.sleep(3)

#20건 출력되어 있는 현재 페이지 리뷰와 점수 등 내용 수집
writer_id2=[]
review2=[]
write_date2=[]
gogam=[]
gogam_0=[]
gogam_1=[]

if cnt <= 20:
    f=open(ff_name,'a',encoding='UTF-8')
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    
    count = 0
    
    reple_result = soup.find('div', class_='u_cbox_content_wrap').find('ul')
    slist = reple_result.find_all('li')
    
    for li in slist:
        count += 1
        print('\n')
        print("%s번째 댓글 수집 중 ============" %count)
        
        write_id = li.find('span',class_='u_cbox_nick').get_text()
        print("1.작성자 ID:"+write_id)
        f.write("\n")
        f.write("총 %s건 중 %s 번째 리뷰 데이터를 수집합니다========="%(cnt,count)+"\n")
        f.write("1.작성자ID:"+write_id+"\n")
        writer_id2.append(write_id)
        
        
        try:
            review = li.find('span', class_= 'u_cbox_contents').get_text()
        except AttributeError:
            review='작성자에 의해 삭제된 댓글입니다.'
            print("2. 리뷰:",review)
        else :
            print("2.리뷰:",review)
        f.write("2.리뷰:"+review + "\n")
        review2.append(review)
        
        write_date = li.find('span',class_='u_cbox_date').get_text()
        print("3.작성일자:",write_date)
        f.write("3.작성일자:"+write_date+"\n")
        write_date2.append(write_date)
        
        
        
        try:
            gogam = li.find('div',class_= 'u_cbox_recomm_set').find_all('em')
            g_gogam = gogam[0].text
            print('4.공감:',g_gogam)
        except :
            g_gogam='0'
            print("4.공감:",g_gogam)
        f.write("4.공감:"+g_gogam+"\n")
        gogam_0.append(g_gogam)

        
        
        try:
            gogam = li.find('div', class_= 'u_cbox_recomm_set').find_all('em')
            b_gogam = gogam[1].text
            print('4.비 공감:',b_gogam)
        except :
            b_gogam='0'
            print("4.비 공감:",b_gogam)
        f.write("4.비 공감:"+b_gogam+"\n")
        gogam_1.append(b_gogam)  
        
        print("\n")
        
        time.sleep(0.2)
        
        if count == cnt:
            break
    print("%s 건 완료 ============================="%count)
    time.sleep(random.randrange(3,8))
else:
    
    i=1
    while(i<=page_cnt-1):
        driver.find_element_by_xpath('''//*[@id="cbox_module"]/div[2]/div[9]/a/span[1]''').click()
        time.sleep(3)
        i += 1
        
    f=open(ff_name,'a',encoding='UTF-8')
    html = driver.page_source
    soup = BeautifulSoup(html,'html.parser')
    
    count = 0
    
    reple_result = soup.find('div', class_='u_cbox_content_wrap').find('ul')
    slist = reple_result.find_all('li')
    
    for li in slist:
        count += 1
        print('\n')
        print("%s번째 댓글 수집 중 ============" %count)
        
        write_id = li.find('span',class_='u_cbox_nick').get_text()
        print("1.작성자 ID:"+write_id)
        f.write("\n")
        f.write("총 %s건 중 %s 번째 리뷰 데이터를 수집합니다========="%(cnt,count)+"\n")
        f.write("1.작성자ID:"+write_id+"\n")
        writer_id2.append(write_id)
        
        
        try:
            review = li.find('span', class_= 'u_cbox_contents').get_text()
        except AttributeError:
            review='작성자에 의해 삭제된 댓글입니다.'
            print("2. 리뷰:",review)
        else :
            print("2.리뷰:",review)
        f.write("2.리뷰:"+review + "\n")
        review2.append(review)
        
        write_date = li.find('span',class_='u_cbox_date').get_text()
        print("3.작성일자:",write_date)
        f.write("3.작성일자:"+write_date+"\n")
        write_date2.append(write_date)
        
        
        
        try:
            gogam = li.find('div',class_= 'u_cbox_recomm_set').find_all('em')
            g_gogam = gogam[0].text
            print('4.공감:',g_gogam)
        except :
            g_gogam='0'
            print("4.공감:",g_gogam)
        f.write("4.공감:"+g_gogam+"\n")
        gogam_0.append(g_gogam)

        
        
        try:
            gogam = li.find('div', class_= 'u_cbox_recomm_set').find_all('em')
            b_gogam = gogam[1].text
            print('4.비 공감:',b_gogam)
        except :
            b_gogam='0'
            print("4.비 공감:",b_gogam)
        f.write("4.비 공감:"+b_gogam+"\n")
        gogam_1.append(b_gogam)  
        
        print("\n")
        
        time.sleep(0.2)
        
        if count == cnt:
            break
    print("%s 건 완료 ============================="%count)
    time.sleep(random.randrange(3,8))
        
    
    
#csv 파일 형식 저장
import pandas as pd
    
# xls 형태와 csv 형태로 저장하기
news_reple = pd.DataFrame()

news_reple['작성자 ID'] = pd.Series(writer_id2)
news_reple['리뷰내용'] = pd.Series(review2)
news_reple['작성일자'] = pd.Series(write_date2)
news_reple['공감횟수'] = pd.Series(gogam_0)
news_reple['비공감횟수'] = pd.Series(gogam_1)

news_reple.to_csv(fc_name, encoding="utf-8-sig", index=True)    

#엑셀 형태로 저장하기
news_reple.to_excel(fx_name, index=True)

#요약정보 출력하기

e_time = time.time()
t_time = e_time - s_time

print("\n")
print("="*80)
print("1.요청된 총 %s건의 리뷰 중에서 실제 크롤링 된 리뷰수는 %s건 입니다." %(cnt,count))
print("2.총 소요시간은 %s 초 입니다."%round(t_time,1))
print("3.파일 저장 완료: txt파일명 : %s"%ff_name)
print("4.파일 저장 완료: csv파일명 : %s"%fc_name)
print("5.파일 저장 완료: xls파일명 : %s"%fx_name)
print("="*80)

driver.close()









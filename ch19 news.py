from bs4 import BeautifulSoup
from selenium import webdriver
import time
import sys
import random
import os

#Step 2. 사용자에게 검색어 키워드를 입력 받습니다.
print("=" *80)
print(" 인터넷 언론 정보 수집하기 - 조선일보 랭킹 뉴스중 경제 분야")
print("=" *80)
print("\n")

#네이버 뉴스에서 가져
url = 'https://news.naver.com/main/list.nhn?mode=LPOD&mid=sec&oid=023&listType=paper&date=' # 경제분야 url

#start_date=int(20210301)
#end_date=int(20210331)
st_date = input('1.조회할 달을 입력하세요(예:202101) :  ')
#st_date = input('1.조회 시작일을 입력하세요(예:20210101) :  ')
#en_date = input('2.조회 종료일을 입력하세요(예:20211231) :  ')

f_dir=input('3.파일이 저장될 경로만 쓰세요;(예:c:\\temp\\): ')

now = time.localtime()
s = '%04d-%02d-%02d-%02d-%02d-%02d' % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

#year = '2021'  

os.makedirs(f_dir+'네이버_경제뉴스'+'-'+s)
os.chdir(f_dir+'네이버_경제뉴스'+'-'+s)

ff_name=f_dir+'네이버_경제뉴스'+'-'+s+'\\'+'네이버_경제뉴스'+'-'+s+'.txt'
fx_name=f_dir+'네이버_경제뉴스'+'-'+s+'\\'+'네이버_경제뉴스'+'-'+s+'.xls'

#Step 3. 크롬 드라이버를 사용해서 웹 브라우저를 실행합니다.
s_time = time.time( )

path=("D:\\temp\\chromedriver.exe")
driver = webdriver.Chrome(path)

#Step 4. 날짜 계산하기
s_year=st_date[0:4]
e_year= st_date[0:4]
s_mon=st_date[4:6]

mon=["01","02","03","04","05","06","07","08","09","10","11","12"]
i=0

start_date2=[]
end_date2=[]


#월 단위 검색 시 
if s_mon =="02" :
    sdate=s_year+s_mon+'01'
    start_date2.append(sdate)
  
    edate=e_year+s_mon+'28'
    end_date=edate
    end_date2.append(end_date)

elif s_mon == "04" or s_mon=="06" or s_mon=="09" or s_mon=="11" :
    sdate=s_year+s_mon+'01'
    start_date2.append(sdate)

    edate=e_year+s_mon+'30'
    end_date=edate
    end_date2.append(end_date)
else :
    sdate=s_year+s_mon+'01'
    start_date2.append(sdate)

    edate=e_year+s_mon+'31'
    end_date=edate
    end_date2.append(end_date)
        

""" #1년으로 검색 시 
for i in range(0,len(mon)) :
    if mon[i] =="02" :
        sdate=s_year+mon[i]+'01'
        start_date2.append(sdate)
  
        edate=e_year+mon[i]+'28'
        end_date=edate
        end_date2.append(end_date)
    
    elif mon[i] == "04" or mon[i]=="06" or mon[i]=="09" or mon[i]=="11" :
        sdate=s_year+mon[i]+'01'
        start_date2.append(sdate)
    
        edate=e_year+mon[i]+'30'
        end_date=edate
        end_date2.append(end_date)
    else :
        sdate=s_year+mon[i]+'01'
        start_date2.append(sdate)
    
        edate=e_year+mon[i]+'31'
        end_date=edate
        end_date2.append(end_date)
        
"""
        
#Step 5. 각 날짜별 기사의 Title 을 추출합니다.
total_count = 0

for x in range(0,len(end_date2)) :

    for i in range(int(start_date2[x]),int(end_date2[x])) :
        full_url = url+str(i)
  
        driver.get(full_url)
        time.sleep(2)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
    
        count = 0
        news_no = 1
        c_year=str(i)[0:4]
        c_mon=str(i)[4:6]
        c_day=str(i)[6:]
        
        #article_result = soup.find('div', class_='list_content rank_numbering')
        article_result = soup.find('div', class_='list_body newsflash_body')
        ar_list = article_result.find_all('dl')
        print("\n")
        print("%s년 %s월 %s일의 뉴스 수집 중 ===================================" %(c_year,c_mon,c_day))
        
        f = open(ff_name, 'a',encoding='UTF-8')
        f.write("%s년 %s월 %s일의 뉴스 수집 중 =================================" %(c_year,c_mon,c_day))
        f.write("\n")
        
        for li in ar_list: 
            if len(li.find_all('dt')) > 1 :
                title = li.find_all('dt')
                title = title[1].find('a').get_text()
            else :
                title = li.find('dt').find('a').get_text()
                
            print(news_no,": ",title)
            
            f.write(str(news_no) + ": " + title + "\n")        
            time.sleep(0.2)
                        
            count += 1
            news_no += 1
            
        f.write("%s 건  완료=====================================================" % count + "\n")
        f.write("\n")
        f.close( )
                    
        print("%s 건  완료========================================================" % count)
        
        total_count += count
        print("현재까지 총 %s 건의 기사를 수집 완료 했습니다" %total_count)
        print("\n")
        time.sleep(1)
        
#Step 8. 출력 결과를 파일에 저장하기
e_time = time.time( )
t_time = e_time - s_time


print("총 소요시간은 %s 초 입니다 " %round(t_time,1))
print("총 저장 건수는 %s 건 입니다 " %total_count)
print("txt 파일 저장 완료: 파일명 : %s " %ff_name)

driver.close( )

#필요한 모듈 실행
from konlpy.tag import *  #한글 분석 모듈
import matplotlib.pyplot as plt  #그래프를 그리고 폰트 출력할 때 사용
from matplotlib import font_manager, rc #그래프를 그리고 폰트 출력할 때 사용
from wordcloud import WordCloud  #워드 클라우드 그릴 때 사용
from collections import Counter #단어의 빈도를 계산할 때 

okt = Okt()
kkma = Kkma()

#print("Kkma:",kkma.nouns("나는 사과, 사과, 복숭아, 복숭아가 좋아요") )
#print("Okt:",okt.nouns("나는 사과, 사과, 복숭아, 복숭아가 좋아요") )



#data1 = open("d:\\temp\\tamplate\\파이썬_텍스트분석예제_1.txt").readlines()
data1 = open("d:\\temp\\tamplate\\파이썬_텍스트분석예제_1.txt").read()
print(data1)

data2 = okt.nouns(data1)
print("추출된 키워드:",data2)

print("\n")
data3 = Counter(data2)
print("단어별 빈도수:",data3)


'''
data22=[]
for i in data1:
    data2=kkma.nouns(i)
    for j in range(0,len(data2)):
        data22.append(data2[j])

print(data22)
'''
print("\n")
#data23 = Counter(data22)
#print(data23)

#불용어 제거하기
sword = open("d:\\temp\\tamplate\\불용어목록.txt").read()
print(sword)
data4 = [ each_word for each_word in data2
         if each_word not in sword ]
print(data4)

data5=[]
for i in data4:
    if len(i) >= 2 | len(i) <= 10:
        data5.append(i)
print(data5)

data6 = Counter(data5)
data7 = data6.most_common(10)
print(data7)
data8 = dict(data7)


#워드 클라우드 그리기
wordcloud = WordCloud(font_path="C:\\Windows\\Fonts\\LGSmHaB_v1.4_151215.ttf" , 
                      relative_scaling=0.5, background_color="white").generate_from_frequencies(data8)

plt.figure(figsize=(8,4))
plt.imshow(wordcloud)
plt.axis('off')
plt.show()




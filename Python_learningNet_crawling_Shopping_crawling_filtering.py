###pandas로 필터링하기
import pandas as pd
pd.set_option('display.max_colwidth',20)


#dataframe => 표
df = pd.read_json("청바지2.json")
#print(df.count())
#print(df.head(10) )
   

def save(df, filename):
    writer = pd.ExcelWriter(filename)
    df.to_excel(writer,'Sheet1')
    writer.save()
    
#save(df, "./청바지2.xlsx")
def printBrandCount(keyword):
    dfFiltered = df[df['title'].str.contains(keyword)]
    print(dfFiltered.count())


brands = ["리바이스","게스", "지오다노", "남자", "여자"]

#for brand in brands:
    #printBrandCount(brand)




def printPricerange(st,en):
    
    dfFiltered = df[(df['price'] <= en) &  (df['price'] >= st )]
    print(dfFiltered['price'].count())

#dfSorted = dfFiltered.sort_values(['price'], ascending=[0])
#print(dfSorted.head(10)['price'])
#print(dfSorted.tail(10)['price'])
printPricerange(10000,20000)
printPricerange(20000,30000)
printPricerange(30000,40000)
printPricerange(40000,50000)
printPricerange(50000,60000)
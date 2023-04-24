
  ###############################
 # 2023.04.13. final version  ##
###############################
# get librarys
import re
import time
import sqlite3
import requests
import numpy as np
import pandas as pd
from selenium import webdriver
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup as bsp
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
# get webdriver
driver=webdriver.Chrome(ChromeDriverManager().install())
driver.set_window_position(0,50)
#driver.set_window_size(3000,2500)
driver.maximize_window()

# define functions
# with it, you can fetch some infos and also send them easily
def sqlPrs(sql='',d=[],opt=1):
    with sqlite3.connect(dfile) as conn:
        cur=conn.cursor()
        if opt==1:
            res=cur.execute(sql).fetchall()
        elif opt==2:
            res=cur.execute(sql,d)
        else:
            cur.execute(sql)
            res=0
        conn.commit()
    return(res)
# you can click buttons
def clickIt(ssel,drv=driver):
    drv.find_element(by=By.CSS_SELECTOR,value=ssel).click()

stInfo=[]
sellerURL=input('https://smartstore.naver.com/blahblahstore와 같은 형식으로 스토어 주소를 입력해주세요: ')
# get seller's info
sellerInfo='/profile'
url=sellerURL+sellerInfo
driver.get(url)
time.sleep(2) 
# store's name
stNameSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(1) > div:nth-child(1) > div._2PXb_kpdRh'
stName=driver.find_element(by=By.CSS_SELECTOR,value=stNameSel).text
# business number check
busNumberSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(2) > div:nth-child(1) > div._2PXb_kpdRh'
busNumber=driver.find_element(by=By.CSS_SELECTOR,value=busNumberSel).text
# business address check
busAddressSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(2) > div:nth-child(2) > div._2PXb_kpdRh'
busAddress=driver.find_element(by=By.CSS_SELECTOR,value=busAddressSel).text
# from the graph you can discover visitor's gender percentile.
graph='#content > div > div._3MuEQCqxSb > div._3knY_AjPO7 > div > div'
src=driver.find_element(by=By.CSS_SELECTOR,value=graph)
txt=bsp(src.get_attribute('innerHTML'),'html.parser').text
male=txt.split('%')[0][-2:]+'%'
female=txt.split('%')[1]+'%'
attSel='#header > div > div._1Y0GXNu6q8 > div._3KDc7jvaa-'
att=driver.find_element(by=By.CSS_SELECTOR,value=attSel).text.split('\n')[0].split('수 ')[1]    
# with the help of api, you can verify infos above
busCheck='http://apis.data.go.kr/1130000/MllBsService/getMllBsInfo?serviceKey=55yUz9MpoHrSz%2B8C53zU9sLbqwDB2Rt9EIvBt9J6qk03ke9IexQYqBb50XkfXsR6H6kkByxLJkx7HJdYczbffA%3D%3D&pageNo=1&numOfRows=10&resultType=xml&bizrno='
req=requests.get(busCheck+busNumber)
html=req.text
src2=bsp(html,'html.parser')
busok=''
# check if the business legit or not
try:
    isok=src2.select('mngstatenm')[0].text
    if(isok=='정상영업'):
        busok='True Business'
        stInfo.append([stName,busNumber,busAddress,male,female,att,busok])
    else:
        busok=isok
        stInfo.append([stName,busNumber,busAddress,male,female,att,busok])
except:
    busok='Problem Occured'
    stInfo.append([stName,busNumber,busAddress,male,female,att,busok])
# 'myStoreInfo.csv' will be saved in your folder named after 'csvs'
df1=pd.DataFrame(stInfo,columns=['상호명','사업자등록번호','사업장 소재지','남성비율','여성비율','관심고객수','정상영업여부'])
df1.to_csv(f'./csvs/myStoreInfo.csv',encoding='utf-8-sig')
# now let us move to goods category page
satis='/category/ALL?cp=1'
driver.get(sellerURL+satis)
time.sleep(2)
# click a button and sort goods. And then align them in order by most reviews
clickIt('#CategoryProducts > div._3y-z4lfyMn > div.wiPgcFH7Gk > div > div._1qTYQamMQo > div._1kAIJfUNTi > div > ul > li:nth-child(3) > button')
time.sleep(2)
clickIt('#CategoryProducts > div._3y-z4lfyMn > div.wiPgcFH7Gk > div > div._3W9WvSiXP3 > ul > li:nth-child(7) > button')
time.sleep(2)

goodInfo=[]
# let us fetch 3 stuffs from the store
for j in range(1,4):
    try:
        m=2
        rstar=[]
        rdate=[]
        roption=[]
        rcomm=[]
        # click each stuff and get into the description page
        proSel='#CategoryProducts > ul > li:nth-child({}) > div > a'
        driver.find_element(by=By.CSS_SELECTOR,value=proSel.format(j)).click()
        time.sleep(2)
        # proName: product name
        proNameSel='#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3'
        proName=driver.find_element(by=By.CSS_SELECTOR,value=proNameSel).text
        # click the review menu
        revSel='#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a'
        driver.find_element(by=By.CSS_SELECTOR,value=revSel).click()
        time.sleep(2)
        # let us know about review information
        totalSel='#content > div > div._2-I30XS1lA > div.-g-2PI3RtF > div.NFNlCQC2mv'
        revinfo=driver.find_element(by=By.CSS_SELECTOR,value=totalSel).text.split('\n')[0]
        #
        goodInfo.append([stName,proName,revinfo])
        # render goodInfo to csv file
        df2=pd.DataFrame(goodInfo,columns=['스토어 이름','상품 이름','리뷰 정보'])
        df2.to_csv(f'./csvs/myGoodInfo{j}.csv',encoding='utf-8-sig')
        # queue reviews in order by low satisfaction 
        # lowRevSel='#REVIEW > div > div._180GG7_7yx > div._2PqWvCMC3e > div._3Tobq9fjVh > ul > li:nth-child(4) > a'
        # clickIt(lowRevSel)
        # time.sleep(2)
        # get ready for diving into reviews
        sel = '._1XNnRviOK8'
        revs = driver.find_elements(by=By.CSS_SELECTOR,value=sel)
        listSel='#REVIEW > div > div._180GG7_7yx > div.cv6id6JEkg > div > div > a:nth-child({})'
        revinfos=[]
        # ten lists of twenty reviews are enough!
    # unhappy reviews
    #     m=2
    #     while(m!=12):
    #         try:
    #             rcomm=[]
    #             rdate=[]
    #             roption=[]
    #             rstar=[]
    #             driver.find_element(by=By.CSS_SELECTOR,value=listSel.format(m)).click()
    #             time.sleep(2)
    #             # comms: comments, ops: options, stas: satisfaction stars, dats: date, storePick: reviews chosen by seller
    #             comms=driver.find_elements(by=By.CSS_SELECTOR,value='div.YEtwtZFLDz > span._3QDEeS6NLn')
    #             ops=driver.find_elements(by=By.CSS_SELECTOR,value='._14FigHP3K8')
    #             stas=driver.find_elements(by=By.CSS_SELECTOR,value='._15NU42F3kT')
    #             dats=driver.find_elements(by=By.CSS_SELECTOR,value='div._2FmJXrTVEX > span._3QDEeS6NLn')
    #             try:
    #                 storePick=driver.find_element(by=By.CSS_SELECTOR,value='._1WWV8t-fcI').text
    #                 if (storePick=='판매자가 직접 선정한 베스트 리뷰입니다.'):
    #                     stas=stas[6:]
    #             except:
    #                 stas=stas[4:]
    #             # preprocessing infos into comments, and dates
    #             stuffs=[]
    #             for c in comms:
    #                 rcomm.append(c.text)
    #             for d in dats:
    #                 rdate.append(d.text)
    #             for o in ops:
    #                 roption.append(o.text)
    #             for s in stas:
    #                 rstar.append(s.text)               
    #             preinfos=list(zip(rdate,rstar,roption,rcomm))
    #             revinfos+=preinfos
    #             m+=1
    #         except:
    #             m+=1
    #     df3=pd.DataFrame(revinfos,columns=['기입날짜','별점','옵션', '후기'])
    #     df3.to_csv(f'./csvs/myUnhappyItem{j}.csv',encoding='utf-8-sig')
    except:
        break
    # queue reviews in order by high satisfaction 
    highRevSel='#REVIEW > div > div._180GG7_7yx > div._2PqWvCMC3e > div._3Tobq9fjVh > ul > li:nth-child(3) > a'
    clickIt(highRevSel)
    time.sleep(2)
    # get ready for diving into reviews
    sel = '._1XNnRviOK8'
    revs = driver.find_elements(by=By.CSS_SELECTOR,value=sel)
    listSel='#REVIEW > div > div._180GG7_7yx > div.cv6id6JEkg > div > div > a:nth-child({})'
    
    #ten lists of twenty reviews are enough!
    #get happy reviews from products
    revinfos=[]
    m=2
    while(m!=12):
        try:
            rcomm=[]
            rdate=[]
            roption=[]
            rstar=[]
            driver.find_element(by=By.CSS_SELECTOR,value=listSel.format(m)).click()
            time.sleep(2)
            # comms: comments, ops: options, stas: satisfaction stars, dats: date
            comms=driver.find_elements(by=By.CSS_SELECTOR,value='div.YEtwtZFLDz > span._3QDEeS6NLn')
            ops=driver.find_elements(by=By.CSS_SELECTOR,value='._14FigHP3K8')
            stas=driver.find_elements(by=By.CSS_SELECTOR,value='._15NU42F3kT')
            dats=driver.find_elements(by=By.CSS_SELECTOR,value='div._2FmJXrTVEX > span._3QDEeS6NLn')
            try:
                storePick=driver.find_element(by=By.CSS_SELECTOR,value='._1WWV8t-fcI').text
                if (storePick=='판매자가 직접 선정한 베스트 리뷰입니다.'):
                    stas=stas[6:]
            except:
                stas=stas[4:]
            # preprocessing infos into comments, and dates
            stuffs=[]
            for c in comms:
                rcomm.append(c.text)
            for d in dats:
                rdate.append(d.text)
            for o in ops:
                roption.append(o.text)
            for s in stas:
                rstar.append(s.text)               
            preinfos=list(zip(rdate,rstar,roption,rcomm))
            revinfos+=preinfos
            m+=1
        except:
            m+=1
    df3=pd.DataFrame(revinfos,columns=['기입날짜','별점','옵션', '후기'])
    df3.to_csv(f'./csvs/myHappyItem{j}.csv',encoding='utf-8-sig')
    driver.back()
    time.sleep(2)
###########################csv합치기############################
import pandas as pd

# # 파일명 리스트 생성
# file_names = ['myUnhappyItem1.csv','myUnhappyItem2.csv','myUnhappyItem3.csv']

# # 빈 DataFrame 생성
# merged_df = pd.DataFrame()

# # 파일 읽어와서 DataFrame에 병합
# for file_name in file_names:
#     df = pd.read_csv('./csvs/'+file_name)
#     merged_df = pd.concat([merged_df, df])

# # 결과를 realTrain.csv 파일로 저장
# merged_df.to_csv('./csvs/myUnhappyReviews.csv', encoding='utf-8-sig')

# 파일명 리스트 생성
file_names = ['myHappyItem1.csv','myHappyItem2.csv','myHappyItem3.csv']

# 빈 DataFrame 생성
merged_df = pd.DataFrame()

# 파일 읽어와서 DataFrame에 병합
for file_name in file_names:
    df = pd.read_csv('./csvs/'+file_name)
    merged_df = pd.concat([merged_df, df])

# 결과를 realTrain.csv 파일로 저장
merged_df.to_csv('./csvs/myHappyReviews.csv', encoding='utf-8-sig')
#####################감성분석#############################
from sklearn.feature_extraction.text import CountVectorizer
# TF_IDF(Term Frequency - Inverse Document Frequency)
# 숫자 기반 문서 벡터 - 단어의 중요성 기반의 벡터
from sklearn.feature_extraction.text import TfidfVectorizer
from kiwipiepy import Kiwi
import pandas as pd
import re
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.metrics import accuracy_score
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
kiwi=Kiwi()

def getPos(txt='다들 고생했습니다.'):
    res=kiwi.analyze(txt)
    badwords=['메롱']
    pos=['NNG','NNP','VV','VX','VA','VC','MDT','MAG','IC','MAC']
    # pos=['NNG','NNP','VV','VX','VA','VC','MDT','MAG','IC'] 84
    # pos=['NNG','NNP','V','MDT','MAG','IC'] 83%
    #pos=['NNG','NNP','NNB','NR','NP','VV','VA','VX','VCP','VCN','MM','MA','MAJ']
    corpus=[]
    for r in res[0][0]:
        for b in badwords:
            if (list(r)[0].find(b)==-1):
                for p in pos:
                    if (list(r)[1].find(p)>-1):
                        corpus.append(list(r)[0])
    return corpus

# CBOW: 카운트기반 BOW
def getCBOW(texts=['나는 아침에 바나나 우유와 바나나 파이를 먹고 왔다.'],opt='CBOW'):
    corpus=[]
    for t in texts:
        tarr=getPos(t)
        corpus.append(' '.join(tarr))
    if opt=='CBOW':
        vec=CountVectorizer()
    else:
        vec=TfidfVectorizer()
    vtr=vec.fit_transform(corpus)
    cols=[t for t,n,in sorted(vec.vocabulary_.items())]
    return (cols,vtr.toarray())

train=pd.read_csv('./csvs/realTrain.csv')
textArrays=train['후기'].values
#정규식으로 텍스트 아닌 거 제거하기

loList=[]
for t in textArrays:
    letters_only=re.sub('[^ㄱ-힣]',' ',t)
    loList.append(letters_only)
#TFIDF
cols,data=getCBOW(loList)
vec=CountVectorizer()


df=pd.DataFrame(data,columns=cols)


test=pd.read_csv('./csvs/myHappyReviews.csv')
test.describe()
textArrays=test['후기'].values
# 정규식으로 텍스트 아닌 거 제거하기
loList=[]
for t in textArrays:
    letters_only=re.sub('[^ㄱ-힣]',' ',t)
    loList.append(letters_only)
#TFIDF
cols2,data2=getCBOW(loList)
vec=CountVectorizer()
#CB
cols2,data2=getCBOW(loList,'CBOW')
v_realTest=pd.DataFrame(data2,columns=cols2)

df2=pd.DataFrame(data2,columns=cols2)
# df와 df2의 column 이름을 가져와서 비교
columns_df = set(df.columns)
columns_df2 = set(df2.columns)

# df에만 있는 column 찾기
columns_only_in_df = columns_df - columns_df2

# df에만 있는 column을 unknown으로 대체
df.drop(columns=columns_only_in_df, inplace=True)

# df와 df2의 column 이름을 가져와서 비교
columns_df = set(df.columns)
columns_df2 = set(df2.columns)

# df에만 있는 column 찾기
columns_only_in_df2 = columns_df2 - columns_df

# df에만 있는 column을 unknown으로 대체
df2.drop(columns=columns_only_in_df2, inplace=True)
df['target']=train['sentiment'].values

et=ExtraTreesClassifier(bootstrap=False, ccp_alpha=0.0, class_weight=None,
                    criterion='gini', max_depth=None, max_features='sqrt',
                    max_leaf_nodes=None, max_samples=None,
                    min_impurity_decrease=0.0, min_samples_leaf=1,
                    min_samples_split=2, min_weight_fraction_leaf=0.0,
                    n_estimators=100, n_jobs=-1, oob_score=False,
                    random_state=0, verbose=0, warm_start=False)
et.fit(df.iloc[:,:-1],df.iloc[:,-1])
y_pred=et.predict(df2)

# positive한 리뷰 중에 지나치게 길이가 긴 거는 의심스럽다~

# 이제 지표를 가지고 등급을 매긴다~!
sco=0
for i,j in enumerate(y_pred):
    if (j==1) and (len(test['후기'].values[i].split('\n'))>3):
        sco+=1
print('의심스러운 장문의 리뷰 개수: ',sco,'개')
print('정상 영업 여부: ',isok)
upper4point8='no'
for g in goodInfo:
    if (g[2][-3:]>='4.8'):
        upper4point8='yes'
print('리뷰 별점이 한 개라도 4.8을 넘나: ',upper4point8)

# 등급 산정 프로세스
grade=''
if (isok=='정상영업'):
    if (upper4point8=='yes'):
        if (sco<10):
            grade='B'
        elif (10<sco<30):
            grade='C'
        else:
            grade='D' 
    else:
        if (sco<10):
            grade='A'
        elif (10<sco<30):
            grade='B'
        else:
            grade='C'  

else:
    grade='D'
print('해당 업체의 등급은',grade,'입니다.')
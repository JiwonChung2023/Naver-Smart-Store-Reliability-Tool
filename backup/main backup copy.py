# 라이브러리를 가져오기
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup as bsp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 웹드라이버를 가져오기
cdriver='./driver/chromedriver.exe'
driver=webdriver.Chrome(cdriver)
driver.set_window_position(0,50)
driver.set_window_size(800, 1300)

# 디비를 정의하기
dfile='./db/suspiciousStores0410.db'
# 함수를 정의하기
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
def clickIt(ssel,drv=driver):
    drv.find_element(by=By.CSS_SELECTOR,value=ssel).click()
def goScroll():
    dheight=driver.execute_script('return document.documentElement.scrollHeight')
    dheight=driver.execute_script('window.scrollTo(0,{})'.format(dheight))

# db에 있는 스토어 리스트를 가져오기
sql='select link from STLC'
res=sqlPrs(sql)

# 스토어 리스트의 길이를 가져오기
sellerLength=len(res)
li1=[]
for i in range(65,66):
    sellerURL=res[i][0]
    # 판매자 정보에서 정보를 얻기
    sellerInfo='/profile'
    url=sellerURL+sellerInfo
    driver.get(url)
    time.sleep(2) 
    # 정보 가져오기
    stNameSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(1) > div:nth-child(1) > div._2PXb_kpdRh'
    stName=driver.find_element(by=By.CSS_SELECTOR,value=stNameSel).text
    busNumberSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(2) > div:nth-child(1) > div._2PXb_kpdRh'
    busNumber=driver.find_element(by=By.CSS_SELECTOR,value=busNumberSel).text
    busAddressSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(2) > div:nth-child(2) > div._2PXb_kpdRh'
    busAddress=driver.find_element(by=By.CSS_SELECTOR,value=busAddressSel).text
    graph='#content > div > div._3MuEQCqxSb > div._3knY_AjPO7 > div > div'
    src=driver.find_element(by=By.CSS_SELECTOR,value=graph)
    txt=bsp(src.get_attribute('innerHTML'),'html.parser').text
    male=txt.split('%')[0][-2:]+'%'
    female=txt.split('%')[1]+'%'
    attSel='#header > div > div._1Y0GXNu6q8 > div._3KDc7jvaa-'
    att=driver.find_element(by=By.CSS_SELECTOR,value=attSel).text.split('\n')[0].split('수 ')[1]    
    busCheck='http://apis.data.go.kr/1130000/MllBsService/getMllBsInfo?serviceKey=55yUz9MpoHrSz%2B8C53zU9sLbqwDB2Rt9EIvBt9J6qk03ke9IexQYqBb50XkfXsR6H6kkByxLJkx7HJdYczbffA%3D%3D&pageNo=1&numOfRows=10&resultType=xml&bizrno='
    req=requests.get(busCheck+busNumber)
    html=req.text
    src2=bsp(html,'html.parser')
    busok=''
        
    try:
        isok=src2.select('mngstatenm')[0].text
        if(isok=='정상영업'):
            busok='True Business'
            li1.append([stName,busNumber,busAddress,male,female,att,busok])
        else:
            busok=isok
            li1.append([stName,busNumber,busAddress,male,female,att,busok])
    except:
        busok='사업장번호를 입력하지 않았습니다.'
        li1.append([stName,busNumber,busAddress,male,female,att,busok])

    df1=pd.DataFrame(li1,columns=['상호명','사업자등록번호','사업장 소재지','남성비율','여성비율','관심고객수','정상영업여부'])
    df1.to_csv(f'./csvs/{stName}StoreInfo.csv',encoding='utf-8-sig')

satis='/category/ALL?cp=1'
driver.get(sellerURL+satis)
time.sleep(2)
clickIt('#CategoryProducts > div._3y-z4lfyMn > div.Ii5tIcy54E > div > div._19Yfb5AYEX > ul > li:nth-child(5) > button')
time.sleep(2)
clickIt('#CategoryProducts > div._3y-z4lfyMn > div.Ii5tIcy54E > div > div.IwEWcMcLlb > div._3SdQ5ltYC7 > div > ul > li:nth-child(3) > button')
time.sleep(1)
li2=[]
jwlist2=[]

for j in range(1,6):
    try:
        m=2
        rstar=[]
        rdate=[]
        roption=[]
        rcomm=[]
        wordBox=''
        proSel='#CategoryProducts > ul > li:nth-child({}) > div > a'
        driver.find_element(by=By.CSS_SELECTOR,value=proSel.format(j)).click()
        time.sleep(2)

        proNameSel='#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3'
        proName=driver.find_element(by=By.CSS_SELECTOR,value=proNameSel).text
        revSel='#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a'
        driver.find_element(by=By.CSS_SELECTOR,value=revSel).click()
        time.sleep(2)
        totalSel='#content > div > div._2-I30XS1lA > div.-g-2PI3RtF > div.NFNlCQC2mv'
        revinfo=driver.find_element(by=By.CSS_SELECTOR,value=totalSel).text.split('\n')[0]
        li2.append([stName,proName,revinfo])
        #jwlist=scrapePerItem()
        lowRevSel='#REVIEW > div > div._180GG7_7yx > div._2PqWvCMC3e > div._3Tobq9fjVh > ul > li:nth-child(4) > a'
        clickIt(lowRevSel)
        time.sleep(1)
        sel = '._1XNnRviOK8'
        revs = driver.find_elements(by=By.CSS_SELECTOR,value=sel)
        listSel='#REVIEW > div > div._180GG7_7yx > div.cv6id6JEkg > div > div > a:nth-child({})'
        realjwlist=[]
        while(m!=7):
            try:
                driver.find_element(by=By.CSS_SELECTOR,value=listSel.format(m)).click()
                time.sleep(2)
                ####
                print('.',end='')
                ####
                #for l in listSel

                for r in revs:
                    rlist=r.text.split('\n')
                    #print(rlist)
                    rstar.append(rlist[1])
                    rdate.append(rlist[3])
                    rest=rlist[5:]
                    if ('더보기' in rest):
                        rest.remove('더보기')
                    if ('이미지 펼쳐보기' in rest):
                        rest.remove('이미지 펼쳐보기')
                    if (':' in rest[0]):
                        roption.append(rest[0])
                        rest=rest[1:]
                    if (len(rest)==1):
                        rcomm.append(rest[-1])
                    else:
                        wordBox=''
                        for n in rest:
                            wordBox+=n
                            wordBox+=' '
                        rcomm.append(wordBox)
                    jwlist=list(zip(rdate,rstar,roption,rcomm))
                    realjwlist+=jwlist
                m+=1
            except:
                m+=1

        df3=pd.DataFrame(realjwlist,columns=['기입날짜','별점','옵션', '후기'])
        df3.to_csv(f'./csvs/{stName}{proName}comdata.csv',encoding='utf-8-sig')
        driver.back()
        time.sleep(2)
    except:
        break
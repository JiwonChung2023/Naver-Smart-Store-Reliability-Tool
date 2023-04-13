  ###############################
 # 2023.04.13. final version  ##
###############################
# get librarys
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
import re

# get webdriver
cdriver='./driver/chromedriver.exe'
driver=webdriver.Chrome(cdriver)
driver.set_window_position(0,50)
driver.set_window_size(800, 1300)

# define database
dfile='./db/suspiciousStores0410.db'

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

# get a list from the table
sql='select link from STLC'
res=sqlPrs(sql)


li1=[]
# 이 부분은 나중에 손 봐야 합니다. 우리는 웹에서 주소를 입력하는 방식으로 구동할테니!
for i in range(65,66):
    sellerURL=res[i][0]
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
            li1.append([stName,busNumber,busAddress,male,female,att,busok])
        else:
            busok=isok
            li1.append([stName,busNumber,busAddress,male,female,att,busok])
    except:
        busok='Problem Occured'
        li1.append([stName,busNumber,busAddress,male,female,att,busok])
    # 'myStoreInfo.csv' will be saved in your folder named after 'csvs'
    df1=pd.DataFrame(li1,columns=['상호명','사업자등록번호','사업장 소재지','남성비율','여성비율','관심고객수','정상영업여부'])
    df1.to_csv(f'./csvs/myStoreInfo.csv',encoding='utf-8-sig')

satis='/category/ALL?cp=1'
driver.get(sellerURL+satis)
time.sleep(2)
clickIt('#CategoryProducts > div._3y-z4lfyMn > div.Ii5tIcy54E > div > div._19Yfb5AYEX > ul > li:nth-child(5) > button')
time.sleep(2)
clickIt('#CategoryProducts > div._3y-z4lfyMn > div.Ii5tIcy54E > div > div.IwEWcMcLlb > div._3SdQ5ltYC7 > div > ul > li:nth-child(3) > button')
time.sleep(1)
li2=[]
jwlist2=[]

for j in range(1,4):
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
        #지우기
        m=2
        while(m!=11):
            try:
                driver.find_element(by=By.CSS_SELECTOR,value=listSel.format(m)).click()
                time.sleep(2)
                ####
                comms = driver.find_elements(by=By.CSS_SELECTOR,value='._3QDEeS6NLn')
                ops = driver.find_elements(by=By.CSS_SELECTOR,value='._14FigHP3K8')
                stas = driver.find_elements(by=By.CSS_SELECTOR,value='._15NU42F3kT')
                #dats = driver.find_elements(by=By.CSS_SELECTOR,value='._3QDEeS6NLn')
                stuffs=[]
                for c in comms:
                    stuffs=c.text.split('\n')
                    for s in stuffs:
                        if '*' in s:
                            pass
                        else:
                            isok=re.match('[ㄱ-힣 ]',s)
                            if (isok!=None): 
                                rcomm.append(s)
                            else:
                                rdate.append(s)
                for o in ops:
                    roption.append(o.text)
                for s in stas:
                    rstar.append(s.text)               
                jwlist=list(zip(rdate,rstar,roption,rcomm))
                realjwlist+=jwlist
                print('.',end='')
                m+=1
            except:
                m+=1

        df3=pd.DataFrame(realjwlist,columns=['기입날짜','별점','옵션', '후기'])
        df3.to_csv(f'./csvs/myItem{j}.csv',encoding='utf-8-sig')
        driver.back()
        time.sleep(2)
    except:
        break

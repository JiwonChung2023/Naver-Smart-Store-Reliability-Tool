# %%
# 라이브러리 가져오기

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
# %%
# 웹드라이버 가져오기
cdriver='./driver/chromedriver.exe'
driver=webdriver.Chrome(cdriver)
driver.set_window_position(0,50)
driver.set_window_size(800, 1300)
# 디비 정의 및 함수 정의하기
# %%
dfile='./db/suspiciousStores0410.db'
# "select" 구문
def sqlPrs(sql='',d=[],opt=1):
    with sqlite3.connect(dfile) as conn:
        cur=conn.cursor()
        # select 문의 경우 실행 후 데이터 반환이 필요하다!
        if opt==1:
            res=cur.execute(sql).fetchall()
        elif opt==2:
            # insert: insert into mvreview (rid,title,href,point,user,rday,content) values(?,?,?,?,?,?,?)
            res=cur.execute(sql,d)
        else:
            cur.execute(sql)
            res=0
        conn.commit()
    return(res)
def clickIt(ssel,drv=driver):
    drv.find_element(by=By.CSS_SELECTOR,value=ssel).click()
def goScroll(level=0):
    #dheight=driver.execute_script('return document.documentElement.scrollHeight')
    dheight=driver.execute_script('window.scrollTo(0,{})'.format(level))
# %%
sql='select link from STLC'
res=sqlPrs(sql)
#print(res[0][0])
# %%
sellerLength=len(res)
j=0
for i in range(sellerLength):
    j+=1
    sellerURL=res[i][0]
    # 판매자 정보에서 정보를 얻기
    sellerInfo='/profile'
    url=sellerURL+sellerInfo
    driver.get(url)
    time.sleep(2) # 딜레이를 통해 웹이 로딩되는 시간을 기다려줌
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
    print(f'상호명: {stName}\n사업자등록번호: {busNumber}\n사업장 소재지: {busAddress}\n남성 비율: {male}\n여성 비율: {female}\n관심고객수: {att}')
    
    busCheck='http://apis.data.go.kr/1130000/MllBsService/getMllBsInfo?serviceKey=55yUz9MpoHrSz%2B8C53zU9sLbqwDB2Rt9EIvBt9J6qk03ke9IexQYqBb50XkfXsR6H6kkByxLJkx7HJdYczbffA%3D%3D&pageNo=1&numOfRows=10&resultType=xml&bizrno='
    #driver.get(busCheck+busNumber)
    req=requests.get(busCheck+busNumber)
    html=req.text
    src2=bsp(html,'html.parser')
    try:
        isok=src2.select('mngstatenm')[0].text
        if(isok=='정상영업'):
            print('True Business')
            print('-'*30)
        else:
            print(isok)
            print('-'*30)
    except:
        print('사업장번호를 입력하지 않았습니다.')
        print('-'*30)
    if(j==10):
        break



# %%

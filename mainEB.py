#%% 라이브러리를 가져오기
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as E_C #조건 지원하기
from selenium.webdriver.support.ui import WebDriverWait as WD
from bs4 import BeautifulSoup as bsp
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
#%%


#--------------------------####################
# -------------------####################
# #--------------------------####################
# #--------------------------####################  
#DB file dir
dfile='./db/suspiciousStores0410.db'
#1. DB에 연결
def sqlPrs(sql='',d=[],opt=1):
    with sqlite3.connect(dfile) as conn:
        cur=conn.cursor()
        if opt==1: #내역 전체뽑기
            res=cur.execute(sql).fetchall()
        elif opt==2:
            res=cur.execute(sql,d)
        else:
            cur.execute(sql)
            res=0
        conn.commit()
    return (res)
######################
#%%
#웹페이지 동작 버튼 기능
##클릭
def clickIt(ssel,drv=''):
    drv.find_element(by=By.CSS_SELECTOR,value=ssel).click()
##스크롤 이동    
def goScroll():
    dheight=driver.execute_script('return document.documentElement.scrollHeight')
    dheight=driver.execute_script('window.scrollTo(0,{})'.format(dheight))
######
#%%

##web driver 열기/주소에 접속하기
def openPage():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    time.sleep(5)
    # driver.set_window_size(1280,800)
    return driver
def getPage(url='https://smartstore.naver.com/zeroskin/products/5849616228?',drv=''):
    drv.get(url)
    time.sleep(3) # 딜레이로 웹이 로딩되는 시간을 기다려줌

#------------------------------------------------------------####################
# #----여기까지가 페이지 동작, db 호출 관련 기본기능-------------------####################
# #----------------------------------------------------------####################
# #----------------------------------------------------------####################    

#------아래 줄부터 스토어 사업자 정보/ 스토어 카테고리/ 스토어 판매 제품명, 제품가격을 추출하는 기능 동작--------------------####################
# #----------------------------------------------------------####################
# #----------------------------------------------------------####################
# #----------------------------------------------------------####################
#%%
# #1. 사업자정보--------------------------------------############################### 
# getSellerInfo: 사업자 정보 관리하는 테이블/인자: sql에 저장된 주소,webddriver---------------------------####################
# 기능 보완해야 할 사항: graph 없는 경우 예외처리, sql 저장하기###############################
# -------------------------------------------------############################### 
# -------------------------------------------------############################### 
# -------------------------------------------------############################### 


# link -> 사업자 정보 관리하는 테이블 
def getSellerInfo(sellink=[],drv=''):
    li1=[]
    sellerInfo='/profile'
    for i in range(len(sellink)): #나중에 sellerlength로 돌려야함
        sellerURL=sellink[i][0]
    # 판매자 정보에서 정보를 얻기
    
        url=sellerURL+sellerInfo
        drv.get(url)
        time.sleep(2) 
    # 판매자 정보 가져오기
    # 이름, 사업자등록번호,주소
        stNameSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(1) > div:nth-child(1) > div._2PXb_kpdRh'
        stName=drv.find_element(by=By.CSS_SELECTOR,value=stNameSel).text
        busNumberSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(2) > div:nth-child(1) > div._2PXb_kpdRh'
        busNumber=drv.find_element(by=By.CSS_SELECTOR,value=busNumberSel).text
        busAddressSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(2) > div:nth-child(2) > div._2PXb_kpdRh'
        busAddress=drv.find_element(by=By.CSS_SELECTOR,value=busAddressSel).text
        
        
        graph='#content > div > div._3MuEQCqxSb > div._3knY_AjPO7 > div > div'
        src=drv.find_element(by=By.CSS_SELECTOR,value=graph)
        print(src.get_attribute('innerHTML'))
        txt=bsp(src.get_attribute('innerHTML'),'html.parser').text
        male=txt.split('%')[0][-2:]+'%'
        female=txt.split('%')[1]+'%'
        attSel='#header > div > div._1Y0GXNu6q8 > div._3KDc7jvaa-'
        att=drv.find_element(by=By.CSS_SELECTOR,value=attSel).text.split('\n')[0].split('수 ')[1]    
        
        ###API에서 판매자 정보 확인
        busCheck='http://apis.data.go.kr/1130000/MllBsService/getMllBsInfo?serviceKey=55yUz9MpoHrSz%2B8C53zU9sLbqwDB2Rt9EIvBt9J6qk03ke9IexQYqBb50XkfXsR6H6kkByxLJkx7HJdYczbffA%3D%3D&pageNo=1&numOfRows=10&resultType=xml&bizrno='
        req=requests.get(busCheck+busNumber)
        html=req.text
        src2=bsp(html,'html.parser')
        busok=''
      
        try:
            isok=src2.select('mngstatenm')[0].text
            if(isok=='정상영업'):
                busok='True Business'
                li1.append([sellerURL,stName,busNumber,busAddress,male,female,att,busok])
            else:
                busok=isok
                li1.append([sellerURL,stName,busNumber,busAddress,male,female,att,busok])
        except:
            busok='사업장번호를 입력하지 않았습니다.'
            li1.append([sellerURL,stName,busNumber,busAddress,male,female,att,busok])
    #columns=['sname','regnum','slocation','mratio','wratio','attrCust','operState']
    df1=pd.DataFrame(li1,columns=['link','상호명','사업자등록번호','사업장 소재지','남성비율','여성비율','관심고객수','정상영업여부'])
    df1.to_csv(f'./csvs/StoreInfo.csv',encoding='utf-8-sig',index=False)

    ###**** sql에 저장하면 좋을 듯######
    return df1
#%%
## getSellerInfo 검증셀
driver=openPage()
# getPage(drv=driver)
sql='select link from STLC'
res=sqlPrs(sql)
stList=getSellerInfo(res,driver)  #현재는 64,65번 업체만 뽑히도록 해놨음
#실행하고 나면 './csvs/StoreInfo.csv'에 업체명, link, 정보 저장
#%%
##### 스토어 정보 필요시에 불러오기 #####################3
#### call data from file or db?################### 
#1. csv에서 링크 받아올 때 코드
tdf=pd.read_csv('./csvs/StoreInfo.csv')    

list=[link for link in tdf['link']]
list
for li in list:
    print(li)
#2. db에서 link받아올 때 코드
sql='select link from STLC'
res=sqlPrs(sql)
links=[]
for i in res:
    link=i[0]
    links.append(link)
links        

#%%

# #2. 스토어의 카테고리 & 링크 뽑기--------------------------------------############################### 
# getCatList2: 각 스토어가 가진 카테고리, 카테고리 링크 반환/인자: 스토어 main 링크,webdriver---------------------------####################
# 기능 보완해야 할 사항: all or best 는 삭제해도 될 것으로 고려됨, sql 저장하기###############################
# ---------------------------------------------------------------############################### 
# ---------------------------------------------------------------############################### 
# ---------------------------------------------------------------############################### 

##스토어의 카테고리 리스트&링크 뽑기
def getCatList2(link='https://smartstore.naver.com/mprice',drv=''):
    orgLink='https://smartstore.naver.com'
    getPage(link,drv=driver)
    link2cats=[]
    catinfo=[]
    catlist=[]
    #상단 메뉴바
    mensel='#pc-categoryMenuWidget > div > div > div > div > div > div > div > ul._3AV7RVieRB'    
     #사이드 메뉴바
    navsel='#pc-categoryMenuWidget > div > div > div > ul.category'
    tgt=drv.find_elements(By.CSS_SELECTOR,value=mensel) #메뉴탭을 타겟으로
    if(len(tgt)==0): #상단메뉴바 없으면 사이드로.
        tgt=drv.find_elements(By.CSS_SELECTOR,value=navsel)
    struct=bsp(tgt[0].get_attribute('innerHTML'),'html.parser')
    atgt=struct.find_all('a') #a tag 걸린거 리스트로 뽑기

    for i in range(len(atgt)):
        taglink=atgt[i]['href']
        cat=atgt[i].get_text()
        catLink=orgLink+taglink
        print(orgLink,catLink,sep='\n')
        link2cats.append([link,cat,catLink])    
    
    return link2cats #link2cats
#%%
# #3. 각 스토어의 값만 뽑는 getCatList2를 이용해 전체 스토어의 카테고리 정보 저장하기--------------------------------------############################### 
# getCatList: 카테고리이름,카테고리 링크 병합/인자: 스토어 main 링크,webdriver---------------------------####################
# 기능 보완해야 할 사항:  sql 저장하기----------------------------------##############################################################
# ---------------------------------------------------------------############################### 
# ---------------------------------------------------------------############################### 
# ---------------------------------------------------------------############################### 
def getCatList(): #sql에 있는 store 목록으로부터, 해당 store 내 카테고리 전부 뽑기. getCatList2 활용
    sql='select link from STLC'
    res=sqlPrs(sql)
    res=set(res)
    links=[]
    for i in res:
        link=i[0]
        links.append(link)
    links2cats=[]
    li2cats=[]
    ##중복 제거해야함!
    i=0
    for li in links:
        li2cats=getCatList2(li,driver) #[[link,cat1,catlink],[link,cat2,catlink2],..]

        for data in li2cats:
            links2cats.append(data)
    return links2cats
#%%
######getCatList 테스트 셀
#db에 있는 스토어링크로부터 스토어 내 카테고리 추출하기
shopCat=getCatList()
df=pd.DataFrame(shopCat,columns=['slink','category','catlink'])
#%%
# 상위 테스트 셀의 결과를 csv로 저장
df.to_csv('./csvs/Store2CatList.csv',encoding='utf-8-sig')
#%%

# #4. 스토어의 모든 제품을 카테고리별로 엮은 결과를 출력해주는 기능--------------------------------------############################### 
# getItemList: 보유한 category 데이터를 기반으로 category에 속한 제품명, 제품가격 저장/인자: 스토어별 dataframe(category,categirylink) 링크,webdriver---------------------------####################
# 기능 보완해야 할 사항:  ALL, Best는 제외하기/sql 저장하기/코드 간결하게 수정하기----------------------------------##############################################################
# ---------------------------------------------------------------------------------############################### 
# ---------------------------------------------------------------------------------############################### 
# ---------------------------------------------------------------------------------############################### 
# 이에이칭?
def getItemList(cdatas=[],drv=''):
    pattern=','
    drv1=drv
    templist=[]
    catlen=len(cdatas)
    print(catlen)
    for i in range(catlen): #길이만큼
        
        category=cdatas.loc[i,['category']][0]
        catlink=cdatas.loc[i,['catlink']][0]
        print(category,catlink)
        getPage(url=catlink,drv=drv1)
        orglink='https://smartstore.naver.com'
        time.sleep(2)
        ViewSel='#CategoryProducts > div._3y-z4lfyMn > div.Ii5tIcy54E > div > div.IwEWcMcLlb > div._3SdQ5ltYC7 > div > ul > li:nth-child(3) > button'
        viewdrv=drv.find_elements(by=By.CSS_SELECTOR,value=ViewSel)
        if(len(viewdrv)>0):
            clickIt('#CategoryProducts > div._3y-z4lfyMn > div.Ii5tIcy54E > div > div.IwEWcMcLlb > div._3SdQ5ltYC7 > div > ul > li:nth-child(3) > button',drv=drv)
        pgsel1='#CategoryProducts > div > a'
        pgsel='#CategoryProducts > div > a:nth-child({})'
        itemli='#CategoryProducts > ul > li'
        pricesel='#CategoryProducts > ul > li > div > a > div._1zl6cBsmdy > strong > span._2DywKu0J_8'
        #CategoryProducts > ul > li > div > a > div._2P2JGsAlZ9._1dAwNEcOik > strong._24X3qV1tN4 > span._3XLnd6iWP5

        pgtgts=drv.find_elements(by=By.CSS_SELECTOR,value=pgsel1)
        pgs=len(pgtgts)
        pglen=pgs-2
        j=2
        
        print(pgs)
        if(pgs!=0):
            if(pglen>0):
                for i in range(2,pgs):
                    clicksel=pgsel.format(i) 
                    # print(clicksel)
                    # print('{}page click processed'.format(i-1))    
                    drv.find_element(by=By.CSS_SELECTOR,value=clicksel).click() 
                    time.sleep(1) #page 넘길 때 로딩 필요

                    #item 목록 불러오기
                    tgts=drv.find_elements(by=By.CSS_SELECTOR,value=itemli)
                    print(len(tgts))
                    for tgt in tgts:
                        html=bsp(tgt.get_attribute('innerHTML'),'html.parser')
                        addlink=html.find('a')['href']
                        itemlink=orglink+addlink

                        #'div > a > div > strong > span'
                        # pricetgt=html.select('span')
                        print(html.find_all('strong'))
                        print(html.find_all('span'))
                        pricetgt=html.find_all('span')                        
                            
                        print('target으로 잡힌 수:',len(pricetgt))
                        itemprice=html.select('div > a > div > strong > span._2DywKu0J_8')[0].text
                        #span._2DywKu0J_8
                        if(len(itemprice)==0):
                            #CategoryProducts > ul > li > div > a > strong
                            print('something wrong')
                            # itemprice=html.select('div > a >strong')[0].text 
                        print(itemprice)
                        itemprice=int(re.sub(pattern,'',itemprice))
                        print(itemprice)
                        itemname=html.select('div> a > strong')[0].text
                        # print(itemlink,itemname)    
                        print(itemlink,itemname,itemprice)    
                        templist.append([category,catlink,itemlink,itemname,itemprice])
        else:
            tgts=drv.find_elements(by=By.CSS_SELECTOR,value=itemli)
            print(len(tgts))
            for tgt in tgts:  
                html=bsp(tgt.get_attribute('innerHTML'),'html.parser')
                addlink=html.find('a')['href']
                itemlink=orglink+addlink
                itemname=html.select('div> a > strong')[0].text
                # print(html.find_all('strong'))
                # print(html.find_all('span'))
                # pricetgt=html.find_all('span')
                # print('target으로 잡힌 수:',len(pricetgt))
                itemprice=html.select('div > a > div > strong > span._2DywKu0J_8')[0].text
                if(len(itemprice)==0):
                    print('something wrong')
                    #CategoryProducts > ul > li > div > a > strong
                    ##CategoryProducts > ul > li > div > a > div > strong > span
                    #CategoryProducts > ul > li> div > a > div > strong > span._2DywKu0J_8
                    # itemprice=html.select('div > a >strong')[0].text 
                itemprice=int(re.sub(pattern,'',itemprice))
                print(itemlink,itemname,itemprice)    
                templist.append([category,catlink,itemlink,itemname,itemprice])
           
    return templist        

#%%
## getItemList() 테스트 셀
ddf=pd.read_csv('./csvs/Store2CatList.csv',index_col=0)
driver=openPage()
templist=getItemList(cdatas=ddf[['category','catlink']],drv=driver)
# templist=getItemList(urls=['https://smartstore.naver.com/vldiol/category/b1069017d4564db0a8271d2b64ffd014?cp=1'],drv1=driver)

#%%


#%%
tdf=pd.DataFrame(templist,columns=['category','catlink','itemlink','itemname','itemprice'])            
tdf.to_csv('./csvs/temp_item_1.csv',encoding='utf-8-sig')
# time.sleep(1)
#CategoryProducts > ul > li:nth-child({}) > div > a'
#CategoryProducts > ul > li > div > a
#CategoryProducts > ul > li

#%%
drv=openPage()
templist=[]
#%%
datas=ddf[['category','catlink']]
ddf.loc[0:]
# print(ddf.loc[['category','catlink']])
datas=ddf.loc[0:len(ddf)-1,['category','catlink']]
datas=ddf.loc[0:len(ddf)-1]
# tdf=datas[['category','catlink']][0:]
#%%
datas
#%%
# for data in datas:
#     i=0
#     print(data.iloc[i,['category']])
for i in range(len(datas)):
    print(datas.loc[i,['category']])
#페이지수 받아오기

#%%

#%%
# 스토어 리스트의 길이를 가져오기
# sellerLength=len(res)
# li1=[]
# for i in range(65,66): #나중에 sellerlength로 돌려야함
#     sellerURL=res[i][0]
#     # 판매자 정보에서 정보를 얻기
#     sellerInfo='/profile'
#     url=sellerURL+sellerInfo
#     driver.get(url)
#     time.sleep(2) 
#     # 판매자 정보 가져오기
#     stNameSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(1) > div:nth-child(1) > div._2PXb_kpdRh'
#     stName=driver.find_element(by=By.CSS_SELECTOR,value=stNameSel).text
#     busNumberSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(2) > div:nth-child(1) > div._2PXb_kpdRh'
#     busNumber=driver.find_element(by=By.CSS_SELECTOR,value=busNumberSel).text
#     busAddressSel='#content > div > div._3MuEQCqxSb > div._2i91yA8LnF > div.oSdeQo13Wd > div > div:nth-child(2) > div:nth-child(2) > div._2PXb_kpdRh'
#     busAddress=driver.find_element(by=By.CSS_SELECTOR,value=busAddressSel).text
#     graph='#content > div > div._3MuEQCqxSb > div._3knY_AjPO7 > div > div'
#     src=driver.find_element(by=By.CSS_SELECTOR,value=graph)
#     txt=bsp(src.get_attribute('innerHTML'),'html.parser').text
#     male=txt.split('%')[0][-2:]+'%'
#     female=txt.split('%')[1]+'%'
#     attSel='#header > div > div._1Y0GXNu6q8 > div._3KDc7jvaa-'
#     att=driver.find_element(by=By.CSS_SELECTOR,value=attSel).text.split('\n')[0].split('수 ')[1]    
#     busCheck='http://apis.data.go.kr/1130000/MllBsService/getMllBsInfo?serviceKey=55yUz9MpoHrSz%2B8C53zU9sLbqwDB2Rt9EIvBt9J6qk03ke9IexQYqBb50XkfXsR6H6kkByxLJkx7HJdYczbffA%3D%3D&pageNo=1&numOfRows=10&resultType=xml&bizrno='
#     req=requests.get(busCheck+busNumber)
#     html=req.text
#     src2=bsp(html,'html.parser')
#     busok=''
#     ###API에서 판매자정보 확인    
#     try:
#         isok=src2.select('mngstatenm')[0].text
#         if(isok=='정상영업'):
#             busok='True Business'
#             li1.append([stName,busNumber,busAddress,male,female,att,busok])
#         else:
#             busok=isok
#             li1.append([stName,busNumber,busAddress,male,female,att,busok])
#     except:
#         busok='사업장번호를 입력하지 않았습니다.'
#         li1.append([stName,busNumber,busAddress,male,female,att,busok])
#     #columns=['sname','regnum','slocation','mratio','wratio','attrCust','operState']
#     df1=pd.DataFrame(li1,columns=['상호명','사업자등록번호','사업장 소재지','남성비율','여성비율','관심고객수','정상영업여부'])
#     df1.to_csv(f'./csvs/{stName}StoreInfo.csv',encoding='utf-8-sig')
    
# satis='/category/ALL?cp=1' #카테고리로 접근
# driver.get(sellerURL+satis)
# time.sleep(2)
# clickIt('#CategoryProducts > div._3y-z4lfyMn > div.Ii5tIcy54E > div > div._19Yfb5AYEX > ul > li:nth-child(5) > button')
# time.sleep(2)
# clickIt('#CategoryProducts > div._3y-z4lfyMn > div.Ii5tIcy54E > div > div.IwEWcMcLlb > div._3SdQ5ltYC7 > div > ul > li:nth-child(3) > button')
# time.sleep(1)
# li2=[]
# jwlist2=[]


# for j in range(1,6):
#     try:
#         m=2
#         rstar=[]
#         rdate=[]
#         roption=[]
#         rcomm=[]
#         wordBox=''
#         proSel='#CategoryProducts > ul > li:nth-child({}) > div > a'
#         driver.find_element(by=By.CSS_SELECTOR,value=proSel.format(j)).click()
#         time.sleep(2)

#         proNameSel='#content > div > div._2-I30XS1lA > div._2QCa6wHHPy > fieldset > div._3k440DUKzy > div._1eddO7u4UC > h3'
#         proName=driver.find_element(by=By.CSS_SELECTOR,value=proNameSel).text
#         revSel='#content > div > div.z7cS6-TO7X > div._27jmWaPaKy > ul > li:nth-child(2) > a'
#         driver.find_element(by=By.CSS_SELECTOR,value=revSel).click()
#         time.sleep(2)
#         totalSel='#content > div > div._2-I30XS1lA > div.-g-2PI3RtF > div.NFNlCQC2mv'
#         revinfo=driver.find_element(by=By.CSS_SELECTOR,value=totalSel).text.split('\n')[0]
#         li2.append([stName,proName,revinfo])
#         #jwlist=scrapePerItem()
#         lowRevSel='#REVIEW > div > div._180GG7_7yx > div._2PqWvCMC3e > div._3Tobq9fjVh > ul > li:nth-child(4) > a'
#         clickIt(lowRevSel)
#         time.sleep(1)
#         sel = '._1XNnRviOK8'
#         revs = driver.find_elements(by=By.CSS_SELECTOR,value=sel)
#         listSel='#REVIEW > div > div._180GG7_7yx > div.cv6id6JEkg > div > div > a:nth-child({})'
#         realjwlist=[]
#         while(m!=7):
#             try:
#                 driver.find_element(by=By.CSS_SELECTOR,value=listSel.format(m)).click()
#                 time.sleep(2)
#                 ####
#                 print('.',end='')
#                 ####
#                 #for l in listSel

#                 for r in revs:
#                     rlist=r.text.split('\n')
#                     #print(rlist)
#                     rstar.append(rlist[1])
#                     rdate.append(rlist[3])
#                     rest=rlist[5:]
#                     if ('더보기' in rest):
#                         rest.remove('더보기')
#                     if ('이미지 펼쳐보기' in rest):
#                         rest.remove('이미지 펼쳐보기')
#                     if (':' in rest[0]):
#                         roption.append(rest[0])
#                         rest=rest[1:]
#                     if (len(rest)==1):
#                         rcomm.append(rest[-1])
#                     else:
#                         wordBox=''
#                         for n in rest:
#                             wordBox+=n
#                             wordBox+=' '
#                         rcomm.append(wordBox)
#                     jwlist=list(zip(rdate,rstar,roption,rcomm))
#                     realjwlist+=jwlist
#                 m+=1
#             except:
#                 m+=1

#         df3=pd.DataFrame(realjwlist,columns=['기입날짜','별점','옵션', '후기'])
#         df3.to_csv(f'./csvs/{stName}{proName}comdata.csv',encoding='utf-8-sig')
#         driver.back()
#         time.sleep(2)
#     except:
#         break


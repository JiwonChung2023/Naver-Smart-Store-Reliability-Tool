#%%
from sklearn.feature_extraction.text import CountVectorizer
# TF_IDF(Term Frequency - Inverse Document Frequency)
# 숫자 기반 문서 벡터 - 단어의 중요성 기반의 벡터
from sklearn.feature_extraction.text import TfidfVectorizer
from kiwipiepy import Kiwi
import pandas as pd
kiwi=Kiwi()
#%%
def getPos(txt='다들 고생했습니다.'):
    res=kiwi.analyze(txt)
    badwords=['메롱']
    pos=['NNG','NNP','VV','VX','VA','VC','MDT','MAG','IC','EC','MAC']
    # pos=['NNG','NNP','VV','VX','VA','VC','MDT','MAG','IC'] 84
    # pos=['NNG','NNP','V','MDT','MAG','IC'] 83%
#    pos=['NNG','NNP','NNB','NR','NP','VV','VA','VX','VCP','VCN','MM','MA','MAJ']
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

train=pd.read_excel('./csvs/realTrain.xlsx')
#%%
train.describe()
train['sentiment'].value_counts()
#%%
textArrays=train['후기'].values
print(textArrays)
#%% 정규식으로 텍스트 아닌 거 제거하기
import re
loList=[]
for t in textArrays:
    letters_only=re.sub('[^ㄱ-힣]',' ',t)
    loList.append(letters_only)

#%%
#TFIDF
cols,data=getCBOW(loList)
print(pd.DataFrame(data,columns=cols))
vec=CountVectorizer()
# %%
#CB
cols,data=getCBOW(loList,'CBOW')
v_realTrain=pd.DataFrame(data,columns=cols)
# %%
print(data)
###################################################################
# %%
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
#%%
from sklearn.model_selection import train_test_split # 트레이닝셋과 테스트셋으로 분리
import pycaret
#%%
df=pd.DataFrame(data,columns=cols)
# df['target']=train['sentiment'].values
#%%
from pycaret.classification import *
from sklearn.metrics import accuracy_score
#%%
test=pd.read_csv('./csvs/myHappyReviews.csv')
#%%
test.describe()
#test['sentiment'].value_counts()
#%%
textArrays=test['후기'].values
print(textArrays)
#%% 정규식으로 텍스트 아닌 거 제거하기
import re
loList=[]
for t in textArrays:
    letters_only=re.sub('[^ㄱ-힣]',' ',t)
    loList.append(letters_only)
#%%
#TFIDF
cols2,data2=getCBOW(loList)
print(pd.DataFrame(data2,columns=cols2))
vec=CountVectorizer()
# %%
#CB
cols2,data2=getCBOW(loList,'CBOW')
v_realTest=pd.DataFrame(data2,columns=cols2)

# %%
df2=pd.DataFrame(data2,columns=cols2)
# %%
# df와 df2의 column 이름을 가져와서 비교
columns_df = set(df.columns)
columns_df2 = set(df2.columns)

# df에만 있는 column 찾기
columns_only_in_df = columns_df - columns_df2

# df에만 있는 column을 unknown으로 대체
df.drop(columns=columns_only_in_df, inplace=True)
# %%
# df와 df2의 column 이름을 가져와서 비교
columns_df = set(df.columns)
columns_df2 = set(df2.columns)

# df에만 있는 column 찾기
columns_only_in_df2 = columns_df2 - columns_df

# df에만 있는 column을 unknown으로 대체
df2.drop(columns=columns_only_in_df2, inplace=True)
df['target']=train['sentiment'].values
# %%
from sklearn.ensemble import ExtraTreesClassifier
et=ExtraTreesClassifier(bootstrap=False, ccp_alpha=0.0, class_weight=None,
                      criterion='gini', max_depth=None, max_features='sqrt',
                      max_leaf_nodes=None, max_samples=None,
                      min_impurity_decrease=0.0, min_samples_leaf=1,
                      min_samples_split=2, min_weight_fraction_leaf=0.0,
                      n_estimators=100, n_jobs=-1, oob_score=False,
                      random_state=0, verbose=0, warm_start=False)
#%%
et.fit(df.iloc[:,:-1],df.iloc[:,-1])
y_pred=et.predict(df2)
y_pred

#%%
# 굿 리뷰 중에 불만족이 차지하는 비율!
tot=len(y_pred)
co=0
for j in y_pred:
    if j==0:
        co+=1
print('불만족 리뷰 비율: ',(co/tot)*100,'%')
# %% 만족 리뷰 중에 지나치게 길이가 긴 거는 의심스럽다~
sco=0
for i,j in enumerate(y_pred):
    if (j==1) and (len(test['후기'].values[i].split('\n'))>3):
        print(test['후기'].values[i])
        print('*'*10)
        sco+=1
print('의심스러운 장문의 리뷰 비율: ',(sco/tot)*100,'%')
#%%########################################이제 불만족 리뷰 중에서 만족하는 비율을 알아보자!!######

#%%
test=pd.read_csv('./csvs/myUnhappyReviews.csv')
#%%
test.describe()
#test['sentiment'].value_counts()
#%%
textArrays=test['후기'].values
print(textArrays)
#%% 정규식으로 텍스트 아닌 거 제거하기
import re
loList=[]
for t in textArrays:
    letters_only=re.sub('[^ㄱ-힣]',' ',t)
    loList.append(letters_only)
#%%
#TFIDF
cols2,data2=getCBOW(loList)
print(pd.DataFrame(data2,columns=cols2))
vec=CountVectorizer()
# %%
#CB
cols2,data2=getCBOW(loList,'CBOW')
v_realTest=pd.DataFrame(data2,columns=cols2)

# %%
df2=pd.DataFrame(data2,columns=cols2)
# %%
# df와 df2의 column 이름을 가져와서 비교
columns_df = set(df.columns)
columns_df2 = set(df2.columns)

# df에만 있는 column 찾기
columns_only_in_df = columns_df - columns_df2

# df에만 있는 column을 unknown으로 대체
df.drop(columns=columns_only_in_df, inplace=True)
# %%
# df와 df2의 column 이름을 가져와서 비교
columns_df = set(df.columns)
columns_df2 = set(df2.columns)

# df에만 있는 column 찾기
columns_only_in_df2 = columns_df2 - columns_df

# df에만 있는 column을 unknown으로 대체
df2.drop(columns=columns_only_in_df2, inplace=True)
df['target']=train['sentiment'].values
# %%
from sklearn.ensemble import ExtraTreesClassifier
et=ExtraTreesClassifier(bootstrap=False, ccp_alpha=0.0, class_weight=None,
                      criterion='gini', max_depth=None, max_features='sqrt',
                      max_leaf_nodes=None, max_samples=None,
                      min_impurity_decrease=0.0, min_samples_leaf=1,
                      min_samples_split=2, min_weight_fraction_leaf=0.0,
                      n_estimators=100, n_jobs=-1, oob_score=False,
                      random_state=0, verbose=0, warm_start=False)
#%%
et.fit(df.iloc[:,:-1],df.iloc[:,-1])
y_pred=et.predict(df2)
y_pred
#%%
# 불만족 리뷰 중에 만족이 차지하는 비율!
tot=len(y_pred)
co=0
for j in y_pred:
    if j==1:
        co+=1
print('불만족 리뷰 중 만족이 차지하는 비율: ',(co/tot)*100,'%')

# %%

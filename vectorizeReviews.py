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
    pos=['NNG','NNP','NNB','NR','NP','VV','VA','VX','VCP','VCN','MM','MA','MAJ']
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

train=pd.read_csv('./csvs/train1.csv')
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
print(pd.DataFrame(data,columns=cols))
# %%


#%%
import pandas as pd
train=pd.read_csv('./csvs/train1.csv')
test=pd.read_csv('./csvs/test1.csv')
train.shape
#%%
train.describe()
train['sentiment'].value_counts()
#%%
textArrays=train['후기'].values
#%% 정규식으로 텍스트 아닌 거 제거하기
import re
loList=[]
for t in textArrays:
    letters_only=re.sub('[^ㄱ-힣]',' ',t)
    loList.append(letters_only)
print(loList)
#%%
#토큰화
tokens=[]
for l in loList:
    print(l)
    stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']
    words=[w for w in words if w not in stopwords('korean')]
    
    token=l.split()
    tokens.append(token)
#print(tokens)
#%%

# 불용어 제거
stopwords = ['의','가','이','은','들','는','좀','잘','걍','과','도','를','으로','자','에','와','한','하다']

words=[w for w in words if w not in stopwords('korean')]

# 카운터벡터라이저


# %%

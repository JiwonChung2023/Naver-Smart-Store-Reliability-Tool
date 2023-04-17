#%%
#C:\ProgramData\anaconda3 밑에 아나콘다를 깔고
#environments에서 llvmlite 제거하기!
#numpy랑 pandas 이런 거 일일이 설치해야함
#%%
## Auto -ML
!pip install pycaret[full] --user
#%%
import sqlite3
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import re
import seaborn as sns
#%%
from sklearn.model_selection import train_test_split # 트레이닝셋과 테스트셋으로 분리
from sklearn.datasets import load_breast_cancer
import pycaret
#%%
cancer=load_breast_cancer()
cancer
#%%
df=pd.DataFrame(cancer.data,columns=cancer.feature_names)
df['target']=cancer.target
#%%
from pycaret.classification import *
#%%
# setup
clf=setup(data=df,target='target',train_size=0.8,session_id=0)
#%%
bestmodel=compare_models()
#%%
bestmodel=compare_models(sort='Accuracy',n_select=3,fold=3)
#%%
bestmodel
#%%
blended=blend_models(estimator_list=bestmodel,fold=3,method='soft')
#%%
plot_model(blended)
#%%
pred=predict_model(blended)
#%%
# auc 그래프
plot_model(blended,'auc')
#%%
# 오차 행렬
plot_model(blended,'confusion_matrix')
#%%
# 모델 1개를 최적화하였을 때 
plot_model(blended,'feature')
#%%
## 기초모델 생성
etm=create_model('et',fold=5)
#%%
## 튜닝
t_etm=tune_model(etm,fold=5,optimize='Accuracy')
t_etm
#%%
plot_model(t_etm,'feature')
#%%
t_etm
#%%
# 최종 모델 확정
fmodel=finalize_model(blended)
#%%
test=get_config('test')
#%%
# 다른 데이터로 데스트하기
ypred=predict_model(fmodel,data=df.iloc[:,:])
ypred
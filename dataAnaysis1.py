#%%
import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud

DATA_PATH = './csvs/' # 데이터경로 설정
print('파일 크기: ')
for file in os.listdir(DATA_PATH):
  if 'csv' in file:
    print(file.ljust(30)+str(round(os.path.getsize(DATA_PATH+ file) / 100000,2))+'MB')
#%%
#트레인 파일 불러오기
train_data = pd.read_csv(DATA_PATH + 'myTrain1.csv',encoding='cp949')
train_data.head()
#%%
print('학습데이터 전체 개수: {}'.format(len(train_data)))
# %%
#리뷰 전체길이 확인
train_length = train_data['후기'].astype(str).apply(len)
train_length.head()
# %%
#리뷰 통계 정보
print('리뷰 길이 최댓값: {}'.format(np.max(train_length)))
print('리뷰 길이 최솟값: {}'.format(np.min(train_length)))
print('리뷰 길이 평균값: {:.2f}'.format(np.mean(train_length)))
print('리뷰 길이 표준편차: {:.2f}'.format(np.std(train_length)))
print('리뷰 길이 중간값: {}'.format(np.median(train_length)))
print('리뷰 길이 제1사분위: {}'.format(np.percentile(train_length,25)))
print('리뷰 길이 제3사분위: {}'.format(np.percentile(train_length,75)))

# %%
train_review = [review for review in train_data['후기'] if type(review) is str]
train_review
# %%
#긍정2, 애매 1, 부정 0
print('긍정 리뷰 갯수: {}'.format(train_data['label'].value_counts()[2]))
print('애매 리뷰 갯수: {}'.format(train_data['label'].value_counts()[1]))
print('부정 리뷰 갯수: {}'.format(train_data['label'].value_counts()[0]))

# %%

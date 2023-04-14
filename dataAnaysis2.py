#%%
import pandas as pd
train=pd.read_csv('./csvs/@.csv')
test=pd.read_csv('./csvs/@.csv')
train.shape
#%%
train.describe()
train['sentiment'].value_counts()
#%%

#%%
import numpy as np
import pandas as pd
import re
import json
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer

DATA_PATH = '/content/sample_data/DATA/' # 데이터 경로 설정
train_data = pd.read_csv(DATA_PATH+'myTrain1.csv', header = 0, delimiter='\t', quoting=3)

train_data['document'][:5]
#%%

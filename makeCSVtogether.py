import pandas as pd

# 파일명 리스트 생성
file_names = ['test01.csv','test02.csv']

# 빈 DataFrame 생성
merged_df = pd.DataFrame()

# 파일 읽어와서 DataFrame에 병합
for file_name in file_names:
    df = pd.read_csv('./csvs/'+file_name)
    merged_df = pd.concat([merged_df, df])

# 결과를 realTrain.csv 파일로 저장
merged_df.to_csv('./csvs/realTest.csv', encoding='utf-8-sig')


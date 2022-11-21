import pandas as pd
import os

def filter_input(df , col_dict):
    for col in col_dict.keys():
        df['TF'] = df[col].apply(lambda x: x not in col_dict[col])
    filter_df = df[df['TF']==True]
    del filter_df['TF']
    return filter_df

def trans_to_score(filter_df):
    filter_df['SCORE'] = filter_df['sentiment'].apply(lambda x: 1 if x=='POS' else -1 if x=='NEG' else 0)
    return sum(filter_df['SCORE'])

file_list = os.listdir('C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/'.format('AAPL-US'))
for file in file_list:
    df = pd.read_excel(
        'C:/Users/hyojeong_kim/Desktop/FDSLoader-Windows-2.13.5.0/XML/{}/{}'.format('AAPL-US', file),
        index_col=0)
    col_dict = {
        'type': ['MD_operator', 'QA_operator', 'QA_q'],

    }
    filter_df = filter_input(df, col_dict)

    score = trans_to_score(filter_df)

    print(file, '-----', score)

print(1)
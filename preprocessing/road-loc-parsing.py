import pandas as pd
import numpy as np

df = pd.DataFrame()

f = open('data/entrc_daegu.txt')
for line in f.readlines():
    line = line.replace('\n', '')
    line = line.split('|')

    df_tmp = pd.DataFrame(columns = ['법정동코드','도로명코드','지하여부','건물본번','건물부번','우편번호','X좌표','Y좌표'])
    for index, col in enumerate(np.array([2, 6, 8, 9, 10, 12, 16, 17])):
        df_tmp[df_tmp.columns[index]] = [line[col]]

    df = pd.concat([df, df_tmp], axis=0, ignore_index=True)

df.to_csv('data/xyloc.csv',index=False)
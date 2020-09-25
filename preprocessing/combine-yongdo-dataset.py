import pandas as pd

#%%
path = 'D:/ISP/14. 프로젝트/대구 빅데이터/데이터/지번_건물명데이터/'
file1 = pd.read_csv(path + 'yongdo_1.csv',encoding= 'utf-8')
file2 = pd.read_csv(path + 'yongdo_2.csv',encoding= 'utf-8')

tmp = file1.merge(file2, how='outer')

tmp.to_csv(path + 'yongdo.csv',encoding='utf-8-sig', index=False)


import pandas as pd

path = 'D:/ISP/14. 프로젝트/대구 빅데이터/데이터/지번_건물명데이터/'
jiga = pd.read_csv(path+'jiga_12700.csv')
yongdo = pd.read_csv(path+'yongdo_12700.csv')
energy = pd.read_csv(path+'building_energy_12700.csv',dtype={'시군구코드':int, '법정동코드':int,
                                                             '번':int,'지':int})
energy.drop(columns=['Year','Month'], inplace=True)
jiga = jiga.merge(yongdo, how='inner')
jiga = jiga.merge(energy, how='inner')


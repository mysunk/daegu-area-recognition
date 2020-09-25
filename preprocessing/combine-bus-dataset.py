import pandas as pd
import numpy as np

path = 'D:/ISP/14. 프로젝트/대구 빅데이터/데이터/'

bus_file1 = pd.read_csv(path + '교통/대구광역시 시내버스 정류소 위치정보(2019년 12월말 기준).csv',encoding= 'cp949')
bus_file2 = pd.read_csv(path + '인구/월별 시내버스 정류소별 이용객 수(2018년).csv',encoding= 'cp949')
bus_file1.drop(columns = ['경유노선'], inplace = True)
loc_len = bus_file1.shape[0]
bus_file1['승차'] = [''] * loc_len
bus_file1['하차'] = [''] * loc_len

station_names = np.unique(bus_file1['정류소명'])
for i, station_name in enumerate(station_names):
    index = bus_file2['정류소명'] == station_name
    if index.sum() != 0:
        up = int(np.array([int(s.replace(",", "")) for s in np.ravel(bus_file2.iloc[:, 2][index].values)]).mean())
        down = int(np.array([int(s.replace(",", "")) for s in np.ravel(bus_file2.iloc[:, 3][index].values)]).mean())
        bus_file1.iloc[i, -2:] = [up, down]

    if i % 1000 == 0:
        print(f'Current {i}...')


bus_file1.to_csv(path + '버스데이터_병합본.csv', index=False, encoding='utf-8-sig')

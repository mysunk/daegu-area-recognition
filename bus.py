import requests
import os
from requests import get
import datetime
import time
import re
import json
# import scipy.interpolate as spi
import numpy as np
from pandas import DataFrame, Series
import pandas as pd
from datetime import timedelta
import csv
import smtplib
from email.mime.text import MIMEText
import statistics
import ast
from time import sleep

threshold = 1 # 1km
file_lists = ['data_고산동.csv','data_중구.csv','data_신당동.csv','data_38030.csv'] # 사용할 파일
file = file_lists[3]
save_file_name = 'data_38030_bus병합.csv'

#%% load dataset
path = 'D:/ISP/14. 프로젝트/대구 빅데이터/데이터/'

## 빌딩
building = pd.read_csv(path+'지번_건물명데이터/병합본/'+file, encoding='utf-8')

## 용도
building['용도지역'] = building['jijiguCdNm'].copy()
nan_idx = pd.isnull(building['용도지역']).values
# building.loc[nan_idx, '용도지역'] = building.loc[nan_idx, 'etcJijigu'].copy()
num_of_building = building.shape[0]

## 버스
bus = pd.read_csv(path+'버스데이터_gps.csv')
bus.dropna(inplace=True)
bus = bus.reset_index(drop=True)
bus['용도지역'] = [''] * bus.shape[0]
# New feature
building['정류소여부'] = [''] * num_of_building
building['승하차수'] = [''] * num_of_building
# building['정류소명'] = [''] * num_of_building

#%% bus의 용도지역 mapping
"""
빌딩의 loc_x, loc_y를 버스정류소의 loc_x, loc_y와 비교하여 
1km 이내에 버스정류소가 있는지 확인 
"""
from tqdm import tqdm
from haversine import haversine

for i in tqdm(range(num_of_building)):
    loc_building = building.loc[i, 'loc_x':'loc_y'].values
    loc_bus = bus.loc[:,'X좌표':'Y좌표'].values
    num_of_busstop = loc_bus.shape[0]
    loc_building = np.repeat(loc_building.reshape(-1,2),num_of_busstop, axis=0)
    dists = np.zeros(num_of_busstop)
    # 위도, 경도를 이용해서 distance 계산 (단위:km)
    for j in range(num_of_busstop):
        dists[j] = haversine(loc_bus[j,:], loc_building[j,:])
    building.loc[i, '정류소여부'] = np.sum(dists < 1).astype(bool).astype(int)
    bus_idx = np.argmin(dists)
    min_dist = np.min(dists)
    # threshold를 넘을 시 가장 가까운 정류소의 정보 넣어줌
    if min_dist < threshold:
        building.loc[i, '승하차수'] = bus.loc[bus_idx,'승차':'하차'].sum().astype(int)
        # building.loc[i, '정류소명'] = bus.loc[bus_idx,'정류소명']
    else:
        building.loc[i, '승하차수'] = 0
    # print(min_dist)

#%% save
building.to_csv(path + save_file_name, index = False,encoding='utf-8-sig')

#%% dumbs

""" PNU코드로 용도지역 직접 받아오는 부분
    sigunguCd, bjdongCd = ref.loc[min_idx, '시군구코드':'법정동코드']
    service_key = "xuUwX9IzFsaeNti4Fq9%2Banwxl6Aue2IUyiAVrR2188EZdCj8sqgOPRhgl6zWt0WmzH1aVqmFldSnu1Yq%2Bqzgcw%3D%3D"
    url_API2 = "http://apis.data.go.kr/1611000/BldRgstService/getBrJijiguInfo?sigunguCd=" + sigunguCd + "&bjdongCd=" + bjdongCd + "&bun=" + bun + "&ji=" + ji + "&ServiceKey=" + service_key

    data_API2 = requests.get(url_API2)
    data_contents2 = data_API2.text

    for item in ['jijiguGbCdNm','etcJijigu']:
        if data_contents2.find('<' + item + '>') != -1:
            index_value_s = data_contents2.find('<' + item + '>')
            index_value_e = data_contents2.find('</' + item + '>')
            val = data_contents2[index_value_s + len('<' + item + '>'):index_value_e]
            bus.loc[i,item] = val
            print('HI')
    """
# ref = pd.read_csv(path + '지번_건물명데이터/지가.csv', dtype={'시군구코드': str, '법정동코드': str, '번': str, '지': str})
# ref = ref.loc[:,['시군구코드','법정동코드','번','지','loc_x','loc_y']]
# ref.dropna(axis='rows',inplace=True)

""" 좌표계 변환 (WTM 좌표 => WGS84)
from pyproj import Proj, transform, CRS
# ??? 좌표계 모름..
proj_bef = Proj(init='epsg:5174')

# WGS1984
proj_WGS84 = Proj(init='epsg:4326') # Wgs84 경도/위도, GPS사용 전지구 좌표

# transform
x1 = bus['Y좌표'].values
y1 = bus['Y좌표'].values

x2, y2 = transform(proj_bef,proj_WGS84,x1,y1)

print(x2, y2)
"""
# 지역별 건물 병합
# datas = []
# for file in file_lists:
#     datas.append(pd.read_csv(path+'지번_건물명데이터/병합본/'+file, encoding='utf-8'))
# datas = pd.concat(datas, axis=0).reset_index(drop=True)
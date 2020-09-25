# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 20:46:30 2020
지적도 API
-법정동 코드를 통한 하기 output 데이터 수집

input
: 시도군/법정동/번/지 코드
output1
:건축물 건축제한 규정, 에너지 등급, 세대수 , 새주소 등
ref.: 건축물 대장 API 활용가이드의 3) 건축물대장 표제부 조회 오퍼레이션 명세 참고
output2
: 용도지역
ref.: 건축물 대장 API 활용가이드의 10) 건축물대장 지역지구구역 조회 오퍼레이션 명세
@author: ISP
"""

import requests
import os
from requests import get 
import datetime
import time
import re
import json
import scipy.interpolate as spi
import numpy as np
from pandas import DataFrame, Series
import pandas as pd
from datetime import timedelta
import csv
import smtplib
from email.mime.text import MIMEText
import statistics

path = 'D:/ISP/14. 프로젝트/대구 빅데이터/데이터/지번_건물명데이터/'
loc_list = pd.read_csv(path + 'data_10500.csv', dtype={'시군구코드': str, '법정동코드': str, '번': str, '지': str})
idx = loc_list['법정동코드']=='12700'
idx = idx.values
loc_list = loc_list.iloc[idx,:].reset_index(drop=True)
loc_len = loc_list.shape[0]

item_list1 = pd.read_excel(path + '1. 좌표_용도지역/표제부.xlsx')
for item in item_list1['item'].values:
    loc_list[item] = [''] * loc_len
item_list2 = pd.read_excel(path + '1. 좌표_용도지역/지역지구.xlsx')
for item in item_list2['item'].values:
    loc_list[item] = [''] * loc_len

# sigunguCd = "11680"
# bjdongCd = "10300"
# bun = "0012"
# ji = "0000"

tic = time.perf_counter()
service_key= "xuUwX9IzFsaeNti4Fq9%2Banwxl6Aue2IUyiAVrR2188EZdCj8sqgOPRhgl6zWt0WmzH1aVqmFldSnu1Yq%2Bqzgcw%3D%3D"

for i in range(724, loc_len):
    sigunguCd = loc_list.loc[i,'시군구코드']
    bjdongCd = loc_list.loc[i, '법정동코드']
    bun = loc_list.loc[i,'번'].zfill(4)
    ji = loc_list.loc[i, '지'].zfill(4)

    url_API1 = "http://apis.data.go.kr/1611000/BldRgstService/getBrTitleInfo?sigunguCd="+sigunguCd+"&bjdongCd="+bjdongCd+"&bun="+bun+"&ji="+ji+"&ServiceKey="+service_key
    url_API2 = "http://apis.data.go.kr/1611000/BldRgstService/getBrJijiguInfo?sigunguCd=" + sigunguCd + "&bjdongCd=" + bjdongCd + "&bun=" + bun + "&ji=" + ji + "&ServiceKey=" + service_key

    data_API1 = requests.get(url_API1)
    data_contents1 = data_API1.text
    data_API2 = requests.get(url_API2)
    data_contents2 = data_API2.text

    # for data_contents 1
    for item in item_list1['item'].values:
        if data_contents1.find('<' + item + '>') != -1:
            index_value_s = data_contents1.find('<' + item + '>')
            index_value_e = data_contents1.find('</' + item + '>')
            val = data_contents1[index_value_s+len('<' + item + '>'):index_value_e]
            loc_list.loc[i,item] = val

    # for data_contents 2
    for item in item_list2['item'].values:
        if data_contents2.find('<' + item + '>') != -1:
            index_value_s = data_contents2.find('<' + item + '>')
            index_value_e = data_contents2.find('</' + item + '>')
            val = data_contents2[index_value_s + len('<' + item + '>'):index_value_e]
            loc_list.loc[i, item] = val
    
    if i % 100 == 0:
        toc = time.perf_counter()
        print(f'Current i is {i}...')
        print(f'Current progress is  {i/loc_len*100} %...')
        print(f'Current time is  {toc - tic} sec...')
loc_list.to_csv(path + 'yongdo_12700.csv',index=False,encoding='utf-8-sig')
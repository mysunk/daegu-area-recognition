# -*- coding: utf-8 -*-
"""
Params.

sigunguCd: 시군구코드 - 11680
bjdongCd: 법정동코드 - 10300
bun: 번 - 0012
ji: 지 - 0000
useYm: 사용년월 - 201501

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

def Filtering_data(data_contents):
    index_value_s = data_contents.find("</sigunguCd><useQty>")
    index_value_e = data_contents.find("</useQty><useYm>")
    if data_contents.find('</sigunguCd><useQty>') != -1:
        value = np.float64(data_contents[index_value_s+len("</sigunguCd><useQty>"):index_value_e])
    else:
        print(data_contents)
        value = 0
    return(value)

#API input
service_key= "xuUwX9IzFsaeNti4Fq9%2Banwxl6Aue2IUyiAVrR2188EZdCj8sqgOPRhgl6zWt0WmzH1aVqmFldSnu1Yq%2Bqzgcw%3D%3D"
# service_key = 'PRGaiqrEJbWS%2FZU1AsNxFXk4HHYxG7WXPHp%2BWI3F6nu7EaqlvzRerwUEwZIcmvSwOyW65tOTjYUckpwPaP143Q%3D%3D'

# sigunguCd = "11680"
# bjdongCd = "10300"
# bun = "0139"
# ji = "0000"

path = 'D:/ISP/14. 프로젝트/대구 빅데이터/데이터/지번_건물명데이터/'
loc_list = pd.read_csv(path + '대구.csv', dtype={'시군구코드': str, '법정동코드': str, '번': str, '지': str})
idx = loc_list['법정동코드']=='12700'
idx = idx.values
loc_list = loc_list.iloc[idx,:].reset_index(drop=True)
loc_len = loc_list.shape[0]

#Data collection
data_list = []
tic = time.perf_counter()
data = np.zeros((loc_len, 2+4+2))

for i in range(487, loc_len):
    sigunguCd = loc_list.loc[i, '시군구코드']
    bjdongCd = loc_list.loc[i, '법정동코드']
    bun = loc_list.loc[i, '번'].zfill(4)
    ji = loc_list.loc[i, '지'].zfill(4)

    data[i, 0] = sigunguCd
    data[i, 1] = bjdongCd
    data[i, 2] = bun
    data[i, 3] = ji
    data[i, 4] = '2019'
    data[i, 5] = '12'
    useYm = '201912'

    url_power = "http://apis.data.go.kr/1611000/BldEngyService/getBeElctyUsgInfo?sigunguCd="+sigunguCd+"&bjdongCd="+bjdongCd+"&bun="+bun+"&ji="+ji+"&useYm="+useYm+"&ServiceKey="+service_key
    url_gas = "http://apis.data.go.kr/1611000/BldEngyService/getBeGasUsgInfo?sigunguCd="+sigunguCd+"&bjdongCd="+bjdongCd+"&bun="+bun+"&ji="+ji+"&useYm="+useYm+"&ServiceKey="+service_key

    #API request
    data_API_power = requests.get(url_power)
    data_API_gas = requests.get(url_gas)
    if data_API_power and data_API_gas:
        data_contents_power = data_API_power.text
        data_contents_gas = data_API_gas.text
    else:
        print('Not normal request')
        break

    value_power = Filtering_data(data_contents_power)
    value_gas = Filtering_data(data_contents_gas)

    print(f'value_power: {value_power} and value_gas: {value_gas}')

    data[i, 6] = value_power
    data[i, 7] = value_gas

    if i % 100==0:
        toc = time.perf_counter()
        print('Current i: {} /// progress: {:.2f}% /// time: {:.1f}'.format(i, i / loc_len * 100, toc - tic))

data_fin = pd.DataFrame(data = data)
data_fin.columns = ['시군구코드', '법정동코드', '번', '지',"Year","Month","Power","Gas"]

data_fin.to_csv(path + "building_energy_12700.csv", index=False)

# -*- coding: utf-8 -*-
"""
Created on Sat Sep  5 20:46:30 2020
지적도 API
-법정동 코드를 통한 하기 output 데이터 수집

input
: PNU코드
output
: 좌표, 지가

@author: ISP
"""

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


path = 'D:/ISP/14. 프로젝트/대구 빅데이터/데이터/지번_건물명데이터/'
loc_list = pd.read_csv(path + '대구.csv', dtype={'시군구코드': str, '법정동코드': str, '번': str, '지': str})
idx = loc_list['법정동코드']=='12700'
idx = idx.values
loc_list = loc_list.iloc[idx,:].reset_index(drop=True)
loc_len = loc_list.shape[0]


# geomFilter ="LINESTRING(14130997.097823 4496665.2259572,14130720.013596 4496698.667157)"
# attrFilter = "1111010100100020001"

from tqdm.notebook import tqdm
loc_list['gosi_year'], loc_list['gosi_month'], loc_list['jiga'], loc_list['loc_x'], loc_list['loc_y']  \
        = [''] *loc_len , ['']*loc_len, ['']*loc_len, ['']*loc_len, ['']*loc_len

service_key= "64C994B5-0D66-3873-B944-C4B2B56256AF"
domain = "http:// http://api.vworld.kr/req/data"

for i in tqdm(range(loc_len)):
    attrFilter = loc_list.loc[i,'시군구코드'] + loc_list.loc[i,'법정동코드']+ '1' + loc_list.loc[i,'번'].zfill(4) + loc_list.loc[i,'지'].zfill(4)

    url_base ="http://api.vworld.kr/req/data?service=data&request=GetFeature&data=LP_PA_CBND_BUBUN"
    url_sub_key = "&key="+service_key
    url_sub_domain = "&domain="+domain
    # url_sub_geomFilter = "&geomFilter="+geomFilter
    url_sub_attrFilter = "&attrFilter=pnu:=:"+attrFilter

    url_API = url_base+url_sub_key+url_sub_domain+url_sub_attrFilter
    data_API = requests.get(url_API)

    data_contents = data_API.text
    data_dict = ast.literal_eval(data_contents)

    if data_dict['response']['status'] == 'OK':
        gosi_year = data_dict['response']['result']['featureCollection']['features'][0]['properties']['gosi_year']
        gosi_month = data_dict['response']['result']['featureCollection']['features'][0]['properties']['gosi_month']
        jiga = data_dict['response']['result']['featureCollection']['features'][0]['properties']['jiga']
        loc = np.array(data_dict['response']['result']['featureCollection']['features'][0]['geometry']['coordinates'][0][0][0])
        loc_x = loc[0]
        loc_y = loc[1]
        loc_list.loc[i,'gosi_year'] = gosi_year
        loc_list.loc[i, 'gosi_month'] = gosi_month
        loc_list.loc[i, 'jiga'] = jiga
        loc_list.loc[i, 'loc_x'] = loc_x
        loc_list.loc[i, 'loc_y'] = loc_y
    else:
        print(data_contents)

loc_list.to_csv(path + 'jiga_12700.csv',index=False, encoding='utf-8-sig')
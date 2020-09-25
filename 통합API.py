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
save_file_name = 'data_신당동.csv'

#%% 대상 구역 지정
loc_list = pd.read_csv(path + '대구.csv', dtype={'시군구코드': str, '법정동코드': str, '번': str, '지': str})
idx = (loc_list['시군구코드']=='27290').values * (loc_list['법정동코드'] >= '10400').values * (loc_list['법정동코드'] <= '10700').values
loc_list = loc_list.iloc[idx,:].reset_index(drop = True)
loc_len = loc_list.shape[0]
#
# # 지가
jiga_list = loc_list.copy()
jiga_list['gosi_year'], jiga_list['gosi_month'], jiga_list['jiga'], jiga_list['loc_x'], jiga_list['loc_y'] \
        = [''] * loc_len, [''] * loc_len, [''] * loc_len, [''] * loc_len, [''] * loc_len
# 용도
yongdo_list = loc_list.copy()
item_list1 = pd.read_excel(path + '1. 좌표_용도지역/표제부.xlsx')
for item in item_list1['item'].values:
    yongdo_list[item] = [''] * loc_len
item_list2 = pd.read_excel(path + '1. 좌표_용도지역/지역지구.xlsx')
for item in item_list2['item'].values:
    yongdo_list[item] = [''] * loc_len
#
# # 에너지
building_energy_list = loc_list.copy()
building_energy_list['Power'], building_energy_list['Gas'] \
        = [''] * loc_len, [''] * loc_len

#%%
def Filtering_data(data_contents):
    index_value_s = data_contents.find("</sigunguCd><useQty>")
    index_value_e = data_contents.find("</useQty><useYm>")
    if data_contents.find('</sigunguCd><useQty>') != -1:
        value = np.float64(data_contents[index_value_s+len("</sigunguCd><useQty>"):index_value_e])
    else:
        print(data_contents)
        value = 0
    return(value)

for i in range(2524, loc_len):
    ##################### 지가 #####################
    service_key = "64C994B5-0D66-3873-B944-C4B2B56256AF"
    domain = "http:// http://api.vworld.kr/req/data"

    attrFilter = loc_list.loc[i, '시군구코드'] + loc_list.loc[i, '법정동코드'] + '1' + loc_list.loc[i, '번'].zfill(4) + \
                 loc_list.loc[i, '지'].zfill(4)

    url_base = "http://api.vworld.kr/req/data?service=data&request=GetFeature&data=LP_PA_CBND_BUBUN"
    url_sub_key = "&key=" + service_key
    url_sub_domain = "&domain=" + domain
    url_sub_attrFilter = "&attrFilter=pnu:=:" + attrFilter

    url_API = url_base + url_sub_key + url_sub_domain + url_sub_attrFilter
    data_API = requests.get(url_API)

    data_contents = data_API.text
    data_dict = ast.literal_eval(data_contents)

    if data_dict['response']['status'] == 'OK':
        gosi_year = data_dict['response']['result']['featureCollection']['features'][0]['properties']['gosi_year']
        gosi_month = data_dict['response']['result']['featureCollection']['features'][0]['properties']['gosi_month']
        jiga = data_dict['response']['result']['featureCollection']['features'][0]['properties']['jiga']
        loc = np.array(
            data_dict['response']['result']['featureCollection']['features'][0]['geometry']['coordinates'][0][0][0])
        loc_x = loc[0]
        loc_y = loc[1]
        jiga_list.loc[i, 'gosi_year'] = gosi_year
        jiga_list.loc[i, 'gosi_month'] = gosi_month
        jiga_list.loc[i, 'jiga'] = jiga
        jiga_list.loc[i, 'loc_x'] = loc_x
        jiga_list.loc[i, 'loc_y'] = loc_y
    else:
        print(data_contents)

    ##################### 용도 #####################
    service_key = "xuUwX9IzFsaeNti4Fq9%2Banwxl6Aue2IUyiAVrR2188EZdCj8sqgOPRhgl6zWt0WmzH1aVqmFldSnu1Yq%2Bqzgcw%3D%3D"
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
            yongdo_list.loc[i,item] = val

    # for data_contents 2
    for item in item_list2['item'].values:
        if data_contents2.find('<' + item + '>') != -1:
            index_value_s = data_contents2.find('<' + item + '>')
            index_value_e = data_contents2.find('</' + item + '>')
            val = data_contents2[index_value_s + len('<' + item + '>'):index_value_e]
            yongdo_list.loc[i, item] = val

    ##################### 에너지 #####################
    # service_key = "xuUwX9IzFsaeNti4Fq9%2Banwxl6Aue2IUyiAVrR2188EZdCj8sqgOPRhgl6zWt0WmzH1aVqmFldSnu1Yq%2Bqzgcw%3D%3D"
    service_key = 'PRGaiqrEJbWS%2FZU1AsNxFXk4HHYxG7WXPHp%2BWI3F6nu7EaqlvzRerwUEwZIcmvSwOyW65tOTjYUckpwPaP143Q%3D%3D'
    useYm = '201912'

    url_power = "http://apis.data.go.kr/1611000/BldEngyService/getBeElctyUsgInfo?sigunguCd=" + sigunguCd + "&bjdongCd=" + bjdongCd + "&bun=" + bun + "&ji=" + ji + "&useYm=" + useYm + "&ServiceKey=" + service_key
    url_gas = "http://apis.data.go.kr/1611000/BldEngyService/getBeGasUsgInfo?sigunguCd=" + sigunguCd + "&bjdongCd=" + bjdongCd + "&bun=" + bun + "&ji=" + ji + "&useYm=" + useYm + "&ServiceKey=" + service_key

    # API request
    data_API_power = requests.get(url_power)
    if data_API_power:
        data_contents_power = data_API_power.text
    else:
        print('Not normal request')
        break
    data_API_gas = requests.get(url_gas)
    if data_API_gas:
        data_contents_gas = data_API_gas.text
    else:
        print('Not normal request')
        break

    value_power = Filtering_data(data_contents_power)
    value_gas = Filtering_data(data_contents_gas)

    print(f'For {i}th iteration::: value_power: {value_power} and value_gas: {value_gas}')

    building_energy_list.loc[i, 'Power'] = value_power
    building_energy_list.loc[i, 'Gas'] = value_gas

#%% save
data = jiga_list.copy()
data = data.merge(yongdo_list, how='inner')
data = data.merge(building_energy_list, how='inner')
data.to_csv(path + save_file_name, index=False, encoding='utf-8-sig')

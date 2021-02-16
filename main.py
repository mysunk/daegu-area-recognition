import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pickle

#%%  Input
# data 지정 => bus / building
path = 'D:/ISP/14. 프로젝트/대구 빅데이터/데이터/지번_건물명데이터/병합본/'
data = pd.read_csv(path + 'data_신당동_bus병합.csv', dtype={'시군구코드': str, '법정동코드': str, '번': str, '지': str},
                   encoding='utf-8')
# data = pd.read_csv('data_pr/data_10500.csv', encoding='cp949')

#%% 전처리
data = data.loc[:,['jiga','loc_x','loc_y',
       'jijiguCdNm', 'Power', 'bcRat',
       'vlRat', 'hhldCnt', 'fmlyCnt','grndFlrCnt','정류소여부','승하차수']]

# 구역, 지구 삭제
for i, l in enumerate(data['jijiguCdNm'].values):
    if type(l) != str:
        continue
    if l[-2:] != '지역':
        data.loc[i, 'jijiguCdNm'] = np.nan
    if l in ['제1종일반주거지역', '제2종일반주거지역', '제3종일반주거지역']:
        data.loc[i, 'jijiguCdNm'] = '일반주거지역'

# interpolation
# label.fillna(method='ffill',inplace=True)
# label.fillna(method='bfill',inplace=True)

# nan processing
idx = data['Power'] == 0
data.loc[idx.values,'Power'] = np.nan
# idx = data['Gas'] == 0
# data.loc[idx.values,'Gas'] = np.nan
# data['Energy'] = np.nanmean(data.loc[:,'Power':'Gas'], axis=1)
data.dropna(subset=['Power'], inplace = True, axis='rows')
data = data.reset_index(drop=True)

# make label
data.dropna(inplace = True, axis='rows')
data = data.reset_index(drop=True)
label = data['jijiguCdNm'].copy()
data.drop(columns = ['jijiguCdNm'], inplace = True)

# feature, class 지정
features = data.columns
n_features = features.shape[0]
class_type = np.unique(label)

#%% corr
corrs = np.zeros((n_features, len(class_type))) # row: feature, col: 용도구역
for i in range(n_features):
    for j, c in enumerate(class_type):
        corrs[i,j] = np.corrcoef((label == c).astype(int), data.iloc[:,i])[1,0]

#%% importance score
importances = np.zeros((n_features, len(class_type))) # row: feature, col: 용도구역
import lightgbm as lgb
for j, c in enumerate(class_type):
    dtrain = lgb.Dataset(data, label=(label == c).astype(int).values)
    param = {'metric': 'l1', 'n_jobs': -1, 'colsample_bytree': 1.0, 'learning_rate': 0.01,
             'verbose':-1}
    model = lgb.train(param, train_set=dtrain ,num_boost_round=1000)
    y_pred = model.predict(data.values)
    importances[:,j] = model.feature_importance()

#%% plot
import seaborn as sns
# correlation
plt.figure(figsize=(10,5))
sns.heatmap(corrs.T)
# plt.xticks(range(n_features), features, rotation=30)
plt.title('Correlation')
plt.show()
plt.show()

# importance score
plt.figure(figsize=(10,5))
plt.plot(importances)
# plt.xticks(range(n_features), features, rotation=30)
plt.title('Feature importance score')
plt.show()
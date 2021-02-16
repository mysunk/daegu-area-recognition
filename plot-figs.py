import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams["font.size"] = 12
plt.rcParams["font.family"] = 'Malgun Gothic'
plt.rcParams['xtick.labelsize'] = 12.
plt.rcParams['ytick.labelsize'] = 12.

path = 'label_yongdoconcat_new_data_total/'
feature_label = ['지가','경도','위도','건폐율','용적률','세대수','가구수','지상층수','전력사용량','가스사용량','버스정류장여부','버스이용객수']
# area_label = ['근린상업지역','도시지역','일반상업지역','일반주거지역','전용주거지역','준주거지역','중심상업지역']

#%% plot
file_name = 'corr_concat_new_data_total'
file_name2 = 'importance_concat_new_data_total'
area_label = pd.read_csv(path + 'label_yongdoconcat_new_data_total.csv', engine='python',header=None).values
area_label = np.ravel(area_label)

data = pd.read_csv(path + file_name + '.csv', header=None).values
df = pd.DataFrame(columns=area_label, index=feature_label, data=data)
df.dropna(inplace=True)
f, ax = plt.subplots(figsize =(10, 4))
sns.heatmap(df.T, ax = ax, cmap ="YlGnBu", linewidths = 0.1)
# plt.title('Correlation 분석')
plt.xticks(rotation=20)
f.tight_layout()
# plt.savefig('D:/GITHUB/python_projects/Daegu_bigdata/figs/' + file_name + '.png')
plt.show()
df.to_csv('corr.csv',index=True)

# Importance score
sns.color_palette('GnBu_d')
c = sns.cubehelix_palette(area_label.shape[0], start=.5, rot=-.7)
data = pd.read_csv(path + file_name2 + '.csv', header=None).values
df = pd.DataFrame(columns=area_label, index=feature_label, data=data)
df[df == 0] = np.nan
df.dropna(inplace=True)
df.plot.bar(stacked=True,color = c)
plt.xticks(rotation=20)
# plt.savefig('D:/GITHUB/python_projects/Daegu_bigdata/figs/' + file_name2 + '.png')
plt.show()

df.to_csv('importance.csv',index=True)
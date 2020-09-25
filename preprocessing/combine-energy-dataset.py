import pandas as pd

#%%
path = 'data/'
file1 = pd.read_csv(path + 'building_energy.csv',encoding= 'utf-8')
file2 = pd.read_csv(path + 'building_energy_gas.csv',encoding= 'utf-8')
file3 = pd.read_csv(path + 'building_energy_power.csv',encoding= 'utf-8')
file4 = pd.read_csv(path + 'building_energy_power_2.csv',encoding= 'utf-8')
file5 = pd.read_csv(path + 'building_energy_common.csv',encoding= 'utf-8')
file6 = pd.read_csv(path + 'building_energy_power_fill.csv',encoding= 'utf-8')


file1.drop(columns = file1.columns[0], inplace = True)
file2.drop(columns = file2.columns[0], inplace = True)
file3.drop(columns = file3.columns[0], inplace = True)
file4.drop(columns = file4.columns[0], inplace = True)
file5.drop(columns = file5.columns[0], inplace = True)
file6.drop(columns = file6.columns[0], inplace = True)


#%%
file1 = pd.concat([file1, file5], axis=0).reset_index(drop=True)
del file5
file3 = pd.concat([file3, file6], axis=0).reset_index(drop=True)
del file6
file3 = pd.concat([file3, file4], axis=0).reset_index(drop=True)

file2 = file2.iloc[:75642,:]
file2 = file2.merge(file3, how='inner').reset_index(drop=True)
file2 = pd.concat([file3, file2.iloc[:,-1]], axis=1)
total_files = pd.concat([file1, file2], axis=0).reset_index(drop=True)

# tmp = file3.merge(file4, how='outer')
# tmp = file1.merge(file2, how='outer')
# tmp.to_csv(path + 'yongdo.csv',encoding='utf-8-sig', index=False)


total_files.to_csv('data/bulding_energy_part1.csv',index=False,encoding='utf-8-sig')

#%%
file1 = pd.read_csv('data/bulding_energy_part1.csv')
file2 = pd.read_csv('data/building_energy_part2.csv')
file2.drop(columns=file2.columns[0], inplace=True)

#%%
concat_file = pd.concat([file1, file2], axis=0)
concat_file.to_csv('data/building_energy_0916.csv',index=False)

#%%
loc_list = pd.read_csv('data/data_code_n_name.csv')
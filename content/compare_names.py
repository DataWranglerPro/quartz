import pandas as pd

df1 = pd.read_excel('master.xlsx', usecols=0)
df1 = df1.sort_values(by='assessee1_full_name').drop_duplicates().reset_index(drop=True)

df2 = pd.read_excel('new.xlsx', usecols=0)
df2 = df2.sort_values(by='assessee1_full_name').drop_duplicates().reset_index(drop=True)

missing = ~df1.iloc[:,0].isin(df2.iloc[:,0])
df_missing = df1[missing]
df_missing['cat'] = 'dropped_off_list'

new = ~df2.iloc[:,0].isin(df1.iloc[:,0])
df_new = df2[new]
df_new['cat'] = 'new_to_list'

joined = pd.concat([df_missing, df_new])
joined.to_excel('compare.xlsx', index=False)
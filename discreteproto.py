


import pandas as pd
import sys

# # Protoype dataframe
filename = sys.argv[1]
output_file = sys.argv[2]
focal_col_name = sys.argv[3]
cite_col_name = sys.argv[4]

df = pd.read_csv(filename)
print('imported file')


df['first_seen'] = 0



## Sorting by year is essential to keeping index
df = df.sort_values('priority_date').reset_index(drop=True)



# selects all the first occurences of class pair
w = df[[cite_col_name,focal_col_name]].apply(sorted, axis = 1, result_type='expand').drop_duplicates().index
df.loc[w, 'first_seen'] = 1
print('just marked first seen')


# moving on to finding simultanious inventions
#resetting index again for future indexing
df.reset_index(drop=True, inplace=True)

# column_dict = {cite_col_name:'sorted_class1',focal_col_name:'sorted_class2'}

#sorting classes so they can be reciprocal
# df1 = df[[cite_col_name,focal_col_name]].apply(sorted, axis=1).rename(index=str, columns=column_dict)
df1 = df[[cite_col_name,focal_col_name]].apply(sorted, axis=1, result_type='expand').rename({0:'sorted_class1', 1:'sorted_class2'}, axis='columns') 
df1 = df1.reset_index(drop=True)



#add sorted to original
intermediate = pd.concat([df, df1], axis=1, join_axes=[df1.index])
print('just made intermediate df')

cols = ['priority_date','sorted_class1','sorted_class2']
seen = intermediate.loc[intermediate['first_seen'] == 1][cols]

# converting dfs into series of strings for easy matching that does not rely on the index
a = intermediate[cols].astype(str).sum(1)
b = seen.astype(str).sum(1)
also_seen = intermediate.loc[a.isin(b)].index


df.loc[also_seen, 'first_seen'] = 1
print('just marked concurrent')

df.to_csv(output_file, index_label=False)


print('hello world')

import pandas as pd
import numpy as np


# # Protoype dataframe

# In[3]:

df = pd.read_csv('d2u.csv')



df['first_seen'] = 0

# In[6]:

## Sortinng by year is essential to keeping index
df = df.sort_values('priority_date')


# In[7]:

# selects all the first occurences of class pair
w =df[['cite_subclass','focal_subclass']].apply(sorted, axis = 1).drop_duplicates().index
df.loc[w, 'first_seen'] = 1
print('just marked first seen')


# In[8]:

# moving on to finding simultanious inventions
#resetting index again for future indexing
df.reset_index(drop=True, inplace=True)


# In[9]:

#sorting classes so they can be reciprocal
df1 = df[['cite_subclass','focal_subclass']].apply(sorted, axis=1).rename(index=str, columns={'cite_subclass':'sorted_class1','focal_subclass':'sorted_class2'})
df1 =df1.reset_index(drop=True)


# In[10]:

#add sorted to original
test = pd.concat([df, df1], axis=1, join_axes=[df1.index])
# test


# In[11]:

# finding out what patents have the same year and class combination
test1 = test.loc[test.duplicated(subset=['priority_date','sorted_class1','sorted_class2'],keep=False)]
print('found dupes for year and class 1 and class2')
# test1


# In[12]:

#selecting combinations that have been confirmed to be seen
h = test1.loc[test.first_seen == 1]
print('filter by year')
# h


# In[13]:

# only select the patents with duplicated pairs that have years that correspond with the first seen instance
b =test1.loc[test1['priority_date'].isin(h['priority_date'])].index
df.loc[b, 'first_seen'] = 1
# print(df)
df.to_csv('d2u_marked.csv', index_label=False)

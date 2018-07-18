print('hello world')

import pandas as pd
import numpy as np


# # Protoype dataframe

# In[3]:

data = [('D111119',2010, 'E','F'),('D111111',2000, 'A','B'),('D222222', 2001, 'B', 'A'),('D333333',2000,'B','A'),('D444443',2005, 'A','B'),('D444444',2005, 'B','A'), ('D555555',2000,'C','D'),('D555555',2000,'D','C'),('D556555',2000,'C','D'),('D666666',2010,'D','C'),('D777777',2005
,'B','B'),('D999999',2000,'C','C')]
cols = ['id', 'year','class1','class2']


# In[4]:

df = pd.DataFrame.from_records(data, columns=cols)


# In[5]:

df['first_seen'] = 0

# In[6]:

## Sortinng by year is essential to keeping index
df = df.sort_values('year')


# In[7]:

# selects all the first occurences of class pair
w =df[['class1','class2']].apply(sorted, axis = 1).drop_duplicates().index
df.loc[w, 'first_seen'] = 1
# print(df)


# In[8]:

# moving on to finding simultanious inventions
#resetting index again for future indexing
df.reset_index(drop=True, inplace=True)


# In[9]:

#sorting classes so they can be reciprocal
df1 = df[['class1','class2']].apply(sorted, axis=1).rename(index=str, columns={'class1':'sorted_class1','class2':'sorted_class2'})
df1 =df1.reset_index(drop=True)


# In[10]:

#add sorted to original
test = pd.concat([df, df1], axis=1, join_axes=[df1.index])
# test


# In[11]:

# finding out what patents have the same year and class combination
test1 = test.loc[test.duplicated(subset=['year','sorted_class1','sorted_class2'],keep=False)]
# test1


# In[12]:

#selecting combinations that have been confirmed to be seen
h = test1.loc[test.first_seen == 1]
# h


# In[13]:

# only select the patents with duplicated pairs that have years that correspond with the first seen instance
b =test1.loc[test1['year'].isin(h['year'])].index
df.loc[b, 'first_seen'] = 1
print(df)
df.to_csv('test.csv,', index_label=False)

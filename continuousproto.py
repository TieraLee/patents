
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter
import sys




# Example instructions if we are focusing on design (focal) to utility (cited)
# 1. retrieve all design patents 
# 2. retrieve all design patent classes for each focal design patent and all technology classes for the utility patents cited in the focal patent
# 3. list all pairwise combinations between design-utility classes (from the focal patent and its references) for each design patent
# 4. record the priority year t for each design patent
# 5. pool together all design-utility class pairs of design patents applied in the same year to construct a universe of patent class pairs for each year. 


filename = sys.argv[1]
output_file = sys.argv[2]
focal_col_name = sys.argv[3]
cite_col_name = sys.argv[4]


df = pd.read_csv(filename)
print('imported file')


df['first_seen'] = 0
# In[2]:


# Nt = Number of all journal pairs that year
def calc_nt(df, column_name):
    Nt_count = df.groupby(['priority_date'])[column_name].count()
    df['Nt'] = df.apply(lambda x: Nt_count[x['priority_date']], axis=1)
    return df


# In[20]:

#Nijt = number of i-j pairs in Ut
def calc_nijt(df, focal_class, cite_class):
    Nijt_count = df.groupby(['priority_date',focal_class,cite_class])['patent_number'].count()
    df['Nijt'] = df.apply(lambda x: Nijt_count.loc[x['priority_date'],x[focal_class],x[cite_class]],axis=1)
    return df

def calc_ni_nj(df, focal_class, cite_class):
    count_class = pd.DataFrame(df.groupby('priority_date').apply(lambda x: pd.Series(Counter(x[focal_class].tolist() + x[cite_class].tolist()))))
    df['Nit'] = df.apply(lambda x: count_class.loc[x['priority_date'],x[focal_class]], axis=1)
    df['Nij'] = df.apply(lambda x: count_class.loc[x['priority_date'],x[cite_class]], axis=1)
    return df



def commonness(row):
    return (row['Nijt'] * row['Nt'])/(row['Nit'] * row['Nij'])




df.reset_index(drop=True, inplace=True)
df = calc_nt(df, cite_col_name)
print('calculated Nt')

df = calc_nijt(df,focal_col_name,cite_col_name)
print('calculated nijt')


df = calc_ni_nj(df,focal_col_name,cite_col_name)
print('calculated ni and nj')

df['commonness'] = df.apply(commonness, axis=1)
print('calculated commonness')
# 
df.to_csv(output_file, index_label=False)



# # Subclass aggregation, design citing utility

# In[98]:


# d2u_sub = final.loc[(~final.cited_patent_number.str.contains('D')) & (~final.cite_mainclass.str.contains('D'))]
# d2u_sub.head()


# In[99]:


# #cleaning up duplicates
# d2u_sub = d2u_sub.drop(labels=['cited_patent_number','cite_mainclass','focal_mainclass'], axis=1).drop_duplicates()
# d2u_sub.head()


# In[100]:


# print(d2u_sub.shape, d2u_sub.patent_number.nunique())


# In[101]:


# d2u_sub.reset_index(drop=True, inplace=True)
# d2u_sub = calc_nt(d2u_sub, 'cite_subclass')
# d2u_sub = calc_nijt(d2u_sub,'focal_subclass','cite_subclass')
# d2u_sub = calc_ni_nj(d2u_sub,'focal_subclass','cite_subclass')
# d2u_sub['commonness'] = d2u_sub.apply(commonness, axis=1)
# d2u_sub.head()
# d2u_sub.to_csv('data/d2u_sub.csv', index_label=False)


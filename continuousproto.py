
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter


# Example instructions if we are focusing on design (focal) to utility (cited)
# 1. retrieve all design patents 
# 2. retrieve all design patent classes for each focal design patent and all technology classes for the utility patents cited in the focal patent
# 3. list all pairwise combinations between design-utility classes (from the focal patent and its references) for each design patent
# 4. record the priority year t for each design patent
# 5. pool together all design-utility class pairs of design patents applied in the same year to construct a universe of patent class pairs for each year. 

# In[2]:


# final = pd.read_csv('data/final_no_drops.csv')
# final.head()


# In[3]:


# final.patent_number.nunique()


# # Mainclass aggregation, design citing utility

# In[4]:


# d2u_main = final.loc[(~final.cited_patent_number.str.contains('D')) & (~final.cite_mainclass.str.contains('D'))]
# d2u_main.head()


# In[5]:


# print(d2u_main.shape, d2u_main.patent_number.nunique())


# In[6]:


# #cleaning up duplicates
# d2u_main = d2u_main.drop(labels=['cited_patent_number','cite_subclass','focal_subclass'], axis=1).drop_duplicates()
# d2u_main.head()


# In[7]:


# print(d2u_main.shape, d2u_main.patent_number.nunique())


# design patents, with design classes, that cites utility patents, with utility classes: 309,304

# In[14]:


# d2u_main.reset_index(drop=True, inplace=True)


# In[18]:


# Nt = Number of all journal pairs that year
def calc_nt(df, column_name):
    Nt_count = df.groupby(['priority_date'])[column_name].count()
    df['Nt'] = df.apply(lambda x: Nt_count[x['priority_date']], axis=1)
    return df


# In[20]:


d2u_main = calc_nt(d2u_main, 'cite_mainclass')
d2u_main.head()


# In[25]:


#Nijt = number of i-j pairs in Ut
def calc_nijt(df, focal_class, cite_class):
    Nijt_count = df.groupby(['priority_date',focal_class,cite_class])['patent_number'].count()
    df['Nijt'] = df.apply(lambda x: Nijt_count.loc[x['priority_date'],x[focal_class],x[cite_class]],axis=1)
    return df


# In[37]:


# d2u_main = calc_nijt(d2u_main,'focal_mainclass','cite_mainclass')
# d2u_main.head()


# In[51]:


def calc_ni_nj(df, focal_class, cite_class):
    count_class = pd.DataFrame(df.groupby('priority_date').apply(lambda x: pd.Series(Counter(x[focal_class].tolist() + x[cite_class].tolist()))))
    df['Nit'] = df.apply(lambda x: count_class.loc[x['priority_date'],x[focal_class]], axis=1)
    df['Nij'] = df.apply(lambda x: count_class.loc[x['priority_date'],x[cite_class]], axis=1)
    return df


# In[61]:


# d2u_main = calc_ni_nj(d2u_main,'focal_mainclass','cite_mainclass')


# In[62]:


# d2u_main_main.head()


# In[63]:


def commonness(row):
    return (row['Nijt'] * row['Nt'])/(row['Nit'] * row['Nij'])


# In[65]:


# d2u_main['commonness'] = d2u_main.apply(commonness, axis=1)
# d2u_main.head()


# # Mainclass aggregation, design citing design

# In[76]:


# d2d_main = final.loc[(final.cited_patent_number.str.contains('D')) & (final.cite_mainclass.str.contains('D'))]
# d2d_main.head()


# In[77]:


# print(d2d_main.shape, d2d_main.patent_number.nunique())


# In[78]:


# #cleaning up duplicates
# d2d_main = d2d_main.drop(labels=['cited_patent_number','cite_subclass','focal_subclass'], axis=1).drop_duplicates()
# d2d_main.head()


# In[79]:


# print(d2d_main.shape, d2d_main.patent_number.nunique())


# In[80]:


# d2d_main.reset_index(drop=True, inplace=True)


# In[81]:


# d2d_main = calc_nt(d2d_main, 'cite_mainclass')
# d2d_main = calc_nijt(d2d_main,'focal_mainclass','cite_mainclass')
# d2d_main = calc_ni_nj(d2d_main,'focal_mainclass','cite_mainclass')
# d2d_main['commonness'] = d2d_main.apply(commonness, axis=1)
# d2d_main.head()


# In[86]:


# #save what we have so far

# d2d_main.to_csv('data/d2d_main.csv', index_label=False)
# d2u_main.to_csv('data/d2u_main.csv', index_label=False)


# # Subclass aggregation, design citing design

# In[94]:


# d2d_sub = final.loc[(final.cited_patent_number.str.contains('D')) & (final.cite_mainclass.str.contains('D'))]
# d2d_sub.head()


# In[95]:


# #cleaning up duplicates
# d2d_sub = d2d_sub.drop(labels=['cited_patent_number','cite_mainclass','focal_mainclass'], axis=1).drop_duplicates()
# d2d_sub.head()


# In[96]:


# print(d2d_sub.shape, d2d_sub.patent_number.nunique())


# In[97]:


d2d_sub.reset_index(drop=True, inplace=True)
d2d_sub = calc_nt(d2d_sub, 'cite_subclass')
d2d_sub = calc_nijt(d2d_sub,'focal_subclass','cite_subclass')
d2d_sub = calc_ni_nj(d2d_sub,'focal_subclass','cite_subclass')
d2d_sub['commonness'] = d2d_sub.apply(commonness, axis=1)
d2d_sub.head()
d2d_sub.to_csv('data/d2d_sub.csv', index_label=False)


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


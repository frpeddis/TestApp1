#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import requests


url= 'https://github.com/frpeddis/TestApp1/blob/22d66352a78bd73d3bead8c14d93a14540dbc73b/Hist_events.xlsx'
myfile = requests.get(url)

df=pd.read_excel(myfile.content)
print(df)


# In[ ]:





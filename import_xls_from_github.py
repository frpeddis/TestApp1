#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

# URL to the raw Excel file
url = "https://github.com/frpeddis/TestApp1/raw/849ac8d55141d9d4f472ec456127705d315e30eb/Hist_events.xlsx"

# Load the Excel file into a Pandas DataFrame
df = pd.read_excel(url)

# Now you can work with the DataFrame 'df'
print(df.head())  # Display the first few rows of the DataFrame


# In[5]:


df.size


# In[8]:


df.shape


# In[9]:


len(df)


# In[10]:


df.columns


# In[22]:


df[['YEAR','EVENT']]


# In[ ]:





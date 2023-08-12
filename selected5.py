#!/usr/bin/env python
# coding: utf-8

# In[2]:


import calendar
import streamlit as st
from datetime import datetime

import pandas as pd
import requests


url= 'https://github.com/frpeddis/TestApp1/blob/22d66352a78bd73d3bead8c14d93a14540dbc73b/Hist_events.xlsx'
myfile = requests.get(url)

df=pd.read_excel(myfile.content)






# Apply custom CSS for dark theme
st.markdown(
    """
    <style>
    body {
        background-color: black;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Streamlit app title
st.title("What day was it? - Please select :sunglasses:")

# Get user input for year, month, and day
selected_year = st.number_input("Select a year:", min_value=1582, max_value=2099, value=2023)
selected_month = st.number_input("Select a month:", min_value=1, max_value=12, value=8)
selected_day = st.number_input("Select a day:", min_value=1, max_value=31, value=12)

# Check for consistency among months and days
invalid_date = False

if selected_month in [4, 6, 9, 11] and selected_day == 31:
    invalid_date = True
elif selected_month == 2:
    if (selected_year % 4 == 0 and selected_year % 100 != 0) or (selected_year % 400 == 0):
        max_days = 29  # Leap year
    else:
        max_days = 28  # Non-leap year
    if selected_day > max_days:
        invalid_date = True
elif selected_day > 31:
    invalid_date = True

# Create a datetime object based on user input
if not invalid_date:
    selected_date = datetime(selected_year, selected_month, selected_day)
    # Display the selected date in bold and with formatting
    st.markdown(f"**Selected Date:** {selected_date.strftime('%d-%b-%Y')}", unsafe_allow_html=True)
    # Get the day of the week for the selected date
    day_of_week = calendar.day_name[selected_date.weekday()]
else:
    st.markdown("<font color='red'>Invalid date</font>", unsafe_allow_html=True)

# Prompt the user to select the expected day of the week from a dropdown list
expected_day_of_week = st.selectbox("Select the expected day of the week:", list(calendar.day_name))

# Add a "Check" button to confirm the selection
check_button = st.button("Check")

if check_button and not invalid_date:
    # Compare the user-selected day of the week with the actual day of the week
    if day_of_week == expected_day_of_week:
        st.success(day_of_week + " OK")
    else:
        st.error(day_of_week + " WRONG!!!")
        
        
rslt_df = df.loc[df['YEAR'] == selected_year]
  
st.write('\nResult dataframe :\n', rslt_df)



# In[ ]:





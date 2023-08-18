#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import datetime

# Function to get the day of the week
def get_day_of_week(year, month, day):
    return datetime.date(year, month, day).strftime("%A")

# Streamlit app
def main():
    st.title("Date Selector")

    # Date slider with date range limits
    min_date = datetime.date(1582, 10, 15)
    max_date = datetime.date(2099, 12, 31)
    selected_date = st.date_input("Select Date", min_value=min_date, max_value=max_date)

    selected_year = selected_date.year
    selected_month = selected_date.month
    selected_day = selected_date.day

    # Determine the day of the week for the selected date
    actual_day_of_week = get_day_of_week(selected_year, selected_month, selected_day)

    # Dropdown for user to select the day of the week
    options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    user_selected_day = st.selectbox("What day of the week was it?", options)

    # Check button to verify user's selection
    check_button = st.button("Check")

    # Check if user pressed the check button and show result
    if check_button:
        if user_selected_day == actual_day_of_week:
            st.write("OK")
        else:
            st.write("Not correct. The correct day of the week was:", actual_day_of_week)

if __name__ == "__main__":
    main()


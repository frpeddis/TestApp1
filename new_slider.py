#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import streamlit as st
import datetime

# Function to check if a year is a leap year
def is_leap_year(year):
    if year % 4 == 0:
        if year % 100 == 0:
            if year % 400 == 0:
                return True
            else:
                return False
        else:
            return True
    return False

# Function to get the day of the week
def get_day_of_week(year, month, day):
    return datetime.date(year, month, day).strftime("%A")

# Streamlit app
def main():
    st.title(" :sunglasses: What day was it? - Please select ")

    # Year slider
    selected_year = st.slider("Select Year", 1582, 2099)

    # Month slider
    selected_month = st.slider("Select Month", 1, 12)

    # Day slider based on selected month
    if selected_month in [4, 6, 9, 11]:
        days_in_month = 30
    elif selected_month == 2:
        days_in_month = 29 if is_leap_year(selected_year) else 28
    else:
        days_in_month = 31
    selected_day = st.slider("Select Day", 1, days_in_month)

    selected_date = f"{selected_day:02d}-{selected_month:02d}-{selected_year}"
    st.write("**Selected Date:** {}".format(selected_date))

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
            st.write(":thumbsup:OK")
        else:
            st.write("Not correct. The correct day of the week was:", actual_day_of_week)

if __name__ == "__main__":
    main()



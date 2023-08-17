#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import calendar
import streamlit as st
from datetime import datetime
import openai

openai.api_key = st.secrets["API_KEY"]

def generate_news(selected_date):
    prompt = f"What happened on {selected_date}?\nGive me a good news with a 😄, a neutral news with a 😐, and a bad news with a 😔. Insert related Wikipedia links."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].text.strip()


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

# Streamlit app
def main():
    st.title("Date Selector")

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

# Streamlit app
def main():
    st.title("Date Selector")

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

    selected_date = f"{selected_year}-{selected_month:02d}-{selected_day:02d}"
    st.write("Selected Date: {}".format(selected_date))
    # Streamlit app title
    
    st.title("What day was it? - Please select :sunglasses:")

    
    selected_date = datetime(selected_day, selected_month, selected_day)
    # Display the selected date in bold and with formatting
    st.markdown(f"**Selected Date:** {selected_date.strftime('%d-%b-%Y')}", unsafe_allow_html=True)
    # Get the day of the week for the selected date
    day_of_week = calendar.day_name[selected_date.weekday()]

    # Prompt the user to select the expected day of the week from a dropdown list
    expected_day_of_week = st.selectbox("Select the expected day of the week:", list(calendar.day_name))

    # Add a "Check" button to confirm the selection
    check_button = st.button("Check")

    if check_button and not invalid_date:
        # Compare the user-selected day of the week with the actual day of the week
        if day_of_week == expected_day_of_week:
            st.success(day_of_week + " OK")
            news_summary = generate_news(selected_date)
            st.title("According to ChatGPT that day...")
            st.write(news_summary) 
        else:
            st.error(day_of_week + " is the correct answer!!!")
            news_summary = generate_news(selected_date)
            st.title("According to ChatGPT that day...")
            st.write(news_summary) 
        
if __name__ == "__main__":
    main()


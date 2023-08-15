#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import random
import calendar
import streamlit as st
from datetime import datetime, timedelta
import openai

openai.api_key = st.secrets["API_KEY"]

def generate_news(selected_date):
    prompt = f"What happened on {selected_date}?\nGive me a good news with a 😄, a neutral news with a 😐, and a bad news with a 😔. Do not mention if it ia good, neutral or bad news. Only use the icons. Do not mention again the date. Insert related Wikipedia links."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].text.strip()



# Streamlit app title
st.title("What day was it ? - Random choice:sunglasses:")

# Function to calculate a random date
def calculate_random_date():
    start_date = datetime(1582, 10, 15)
    end_date = datetime(2099, 12, 31)
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Check if random_date and start_time are in session state, if not, calculate and store them
if 'random_date' not in st.session_state:
    st.session_state.random_date = calculate_random_date()
    

if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()

if 'check_pressed' not in st.session_state:
    st.session_state.check_pressed = False

if 'time_taken' not in st.session_state:
    st.session_state.time_taken = 0

# Display the date in the format dd-mmm-yyyy
st.write("Random Date:", st.session_state.random_date.strftime("%d-%b-%Y"))
selected_date = st.session_state.random_date.strftime("%d-%b-%Y")

# Calculate time taken
if not st.session_state.check_pressed:
    time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
    display_time_taken = False
else:
    time_taken = st.session_state.time_taken
    display_time_taken = True

# Prompt the user to select the day of the week from a dropdown list
selected_day_of_week = st.selectbox("Select the day of the week:", list(calendar.day_name))

# Add a "Check" button to confirm the selection
check_button = st.button("Check")

if check_button:
    st.session_state.check_pressed = True

    # Confirm the day of the week selected by the user
    day_of_week = calendar.day_name[st.session_state.random_date.weekday()]

    if selected_day_of_week == day_of_week:
        st.success(day_of_week + " OK")
        news_summary = generate_news(selected_date)
        st.title("According to ChatGPT that day...")
        st.write(news_summary) 
    else:
        st.error(day_of_week + " WRONG!!!")
        news_summary = generate_news(selected_date)
        st.title("According to ChatGPT that day...")
        st.write(news_summary) 

    # Calculate time taken to make the selection
    st.session_state.time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
    time_taken = st.session_state.time_taken
    display_time_taken = True

# Show the amount of seconds taken
if display_time_taken:
    st.write("Time taken to check:", round(time_taken, 2), "seconds")


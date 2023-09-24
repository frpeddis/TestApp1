# Import necessary modules and packages
import random
import calendar
import streamlit as st
from datetime import datetime, timedelta
import openai
import time
import requests
from PIL import Image
from io import BytesIO
import pandas as pd

# Initialize session state for best_time
if 'best_time' not in st.session_state:
    st.session_state.best_time = float('inf')

# Checkbox to toggle image display
openai.api_key = st.secrets["API_KEY"]
st.set_page_config(page_title="🌀 WeekDay Whiz")

# Streamlit app title
st.title(":sunglasses: What day is it? Random date 🎲")
show_images = st.checkbox("Show me how to calculate ! ")

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

# Display the date
description = "**Random Date:**"
value = st.session_state.random_date.strftime("%d-%b-%Y")
st.markdown(f"{description} {value}")

# Calculate time taken
if not st.session_state.check_pressed:
    time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
    display_time_taken = False
else:
    time_taken = st.session_state.time_taken
    display_time_taken = True

# Show the amount of seconds taken and update best_time
if display_time_taken:
    if time_taken < st.session_state.best_time:
        st.session_state.best_time = time_taken
    st.write(f"Best time so far: {st.session_state.best_time} seconds")

# Prompt the user to select the day of the week from a dropdown list
selected_day_of_week = st.selectbox("Select the day of the week:", list(calendar.day_name))

# Add a "Check" button to confirm the selection
check_button = st.button("Check")

# Your existing logic for checking the selected day and providing feedback ...

# Add any other features or logic you have in your original code here

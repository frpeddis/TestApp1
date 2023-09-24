
import random
import calendar
import streamlit as st
from datetime import datetime, timedelta
import openai
import time
import streamlit.components.v1 as com
import requests
from PIL import Image
from io import BytesIO
import pandas as pd

# Function to calculate a random date
def calculate_random_date():
    start_date = datetime(1582, 10, 15)
    end_date = datetime(2099, 12, 31)
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Initialize session state variables if not already initialized
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0

if 'lowest_time_record' not in st.session_state:
    st.session_state.lowest_time_record = 1e6  # 1 million seconds as an initial high value

if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()

if 'random_date' not in st.session_state:
    st.session_state.random_date = calculate_random_date()

# If 5 questions are answered, reset the session
if st.session_state.question_count >= 5:
    st.session_state.question_count = 0
    st.session_state.start_time = datetime.now()
    st.session_state.random_date = calculate_random_date()
    st.write("Starting a new round of questions.")

# Display the random date
description = "**Random Date:**"
value = st.session_state.random_date.strftime("%d-%b-%Y")
st.markdown(f"{description} {value}")

# Prompt the user to select the day of the week from a dropdown list
selected_day_of_week = st.selectbox(f"Select the day of the week for question {st.session_state.question_count + 1}:", list(calendar.day_name))

# Add a "Check" button to confirm the selection
check_button = st.button(f"Check for question {st.session_state.question_count + 1}")

# Logic for checking the answer
if check_button:
    # Increment the question count
    st.session_state.question_count += 1

    # Generate a new random date for the next question
    st.session_state.random_date = calculate_random_date()

    # Confirm the day of the week selected by the user
    day_of_week = calendar.day_name[st.session_state.random_date.weekday()]
    
    if selected_day_of_week == day_of_week:
        st.balloons()
        st.success(day_of_week + " is OK! :thumbsup:")
    else:
        com.iframe("https://lottie.host/?file=380d3ff9-0c30-4a96-b25b-7eeb8868bfeb/vnvhMZFQ8j.json")
        st.error(day_of_week + " is the right day! :coffee: That's why...")

    # Calculate the total time taken to complete all questions so far
    time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
    
    # Check if the time taken is less than the current lowest time record
    if time_taken < st.session_state.lowest_time_record:
        # Update the lowest time record
        st.session_state.lowest_time_record = time_taken
        st.write(f"New record! Lowest time taken: {st.session_state.lowest_time_record} seconds")
    else:
        st.write(f"Time taken: {time_taken} seconds")

    # Display the total time taken and the lowest time record
    st.write(f"Total time taken to complete questions so far: {time_taken} seconds")
    st.write(f"Lowest time record: {st.session_state.lowest_time_record} seconds")

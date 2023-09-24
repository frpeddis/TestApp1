
import random
import calendar
import streamlit as st
from datetime import datetime, timedelta
import time

# Function to calculate a random date
def calculate_random_date():
    start_date = datetime(1582, 10, 15)
    end_date = datetime(2099, 12, 31)
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Initialize session state variables if not already initialized
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0

if 'total_time' not in st.session_state:
    st.session_state.total_time = 0.0

if 'question_start_time' not in st.session_state:
    st.session_state.question_start_time = datetime.now()

if 'random_date' not in st.session_state:
    st.session_state.random_date = calculate_random_date()

if 'button_label' not in st.session_state:
    st.session_state.button_label = "Check"

if 'time_list' not in st.session_state:
    st.session_state.time_list = []

# Reset the session if 5 questions are answered
if st.session_state.question_count >= 5:
    st.session_state.question_count = 0
    st.session_state.total_time = 0.0
    st.session_state.button_label = "Check"
    st.session_state.time_list = []
    st.session_state.random_date = calculate_random_date()
    st.session_state.question_start_time = datetime.now()
    st.write("Starting a new round of questions.")

# Display the random date
description = "**Random Date:**"
value = st.session_state.random_date.strftime("%d-%b-%Y")
st.markdown(f"{description} {value}")

# Prompt the user to select the day of the week from a dropdown list
selected_day_of_week = st.selectbox(f"Select the day of the week for question {st.session_state.question_count + 1}:", list(calendar.day_name))

# Add a button to confirm the selection, label changes based on session state
check_button = st.button(st.session_state.button_label)

# Logic for checking the answer
if check_button:
    if st.session_state.button_label == "Check":
        # Confirm the day of the week selected by the user
        day_of_week = calendar.day_name[st.session_state.random_date.weekday()]
        
        if selected_day_of_week == day_of_week:
            st.balloons()
            st.success(day_of_week + " is OK! :thumbsup:")
            
            # Calculate the time taken for this question
            question_time_taken = (datetime.now() - st.session_state.question_start_time).total_seconds()
            st.write(f"Time taken for this question: {round(question_time_taken, 2)} seconds")
            
            # Update the total time
            st.session_state.total_time += question_time_taken
            
            # Add the time to the list
            st.session_state.time_list.append(question_time_taken)
            
            # Change the button label to "NEXT"
            st.session_state.button_label = "Next"
        
        else:
            st.error(day_of_week + " is the right day! :coffee: That's why...")

    elif st.session_state.button_label == "Next":
        # Change the button label back to "Check"
        st.session_state.button_label = "Check"
        
        # Generate a new random date for the next question
        st.session_state.random_date = calculate_random_date()
        
        # Increment the question count
        st.session_state.question_count += 1
        
        # Reset the question start time
        st.session_state.question_start_time = datetime.now()

    if st.session_state.question_count >= 5:
        st.write(f"Total time taken for all 5 questions: {round(st.session_state.total_time, 2)} seconds")
        st.write(f"Shortest time taken: {round(min(st.session_state.time_list), 2)} seconds")
        st.write(f"Longest time taken: {round(max(st.session_state.time_list), 2)} seconds")

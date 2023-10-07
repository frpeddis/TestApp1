
import random
import calendar
import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt  # Importing matplotlib for plotting
from gtts import gTTS
from num2words import num2words
import os

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='it')  # Language set to Italian
    filename = 'temp_audio.mp3'
    tts.save(filename)
    return filename

# Function to convert date to Italian words
def date_to_italian_words(date):
    day = int(date.strftime("%d"))
    month = date.strftime("%B")
    year = int(date.strftime("%Y"))

    day_words = num2words(day, lang='it')
    year_words = num2words(year, lang='it')

    month_map = {
        'January': 'gennaio',
        'February': 'febbraio',
        'March': 'marzo',
        'April': 'aprile',
        'May': 'maggio',
        'June': 'giugno',
        'July': 'luglio',
        'August': 'agosto',
        'September': 'settembre',
        'October': 'ottobre',
        'November': 'novembre',
        'December': 'dicembre'
    }
    
    month_words = month_map.get(month, '')
    return f"{day_words} {month_words} {year_words}"




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
    st.session_state.button_label = "Check Question 1"

if 'time_list' not in st.session_state:
    st.session_state.time_list = []

if 'show_summary' not in st.session_state:  # New session state to control the summary display
    st.session_state.show_summary = False


description = ""







# Display the random date
description = "**Random Date:**"
value = st.session_state.random_date.strftime("%d-%b-%Y")
#st.markdown(f"{description} {value}")

# Convert the date to Italian words
date_words = date_to_italian_words(st.session_state.random_date)

# Text to speech
audio_file_path = text_to_speech(f"{date_words}")

# Streamlit audio player
audio_file = open(audio_file_path, 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3')






# Prompt the user to select the day of the week from a dropdown list
selected_day_of_week = st.selectbox(f"Select the day of the week for question {st.session_state.question_count + 1}:", list(calendar.day_name))

# Add a button to confirm the selection, label changes based on session state
check_button = st.button(st.session_state.button_label)

# Logic for checking the answer
if check_button:
    # Confirm the day of the week selected by the user
    day_of_week = calendar.day_name[st.session_state.random_date.weekday()]
    
    if selected_day_of_week == day_of_week:
        st.balloons()
        st.markdown(f"{description} {value}")
        st.success(f"{day_of_week} is OK! :thumbsup:")

        # Calculate the time taken for this question
        question_time_taken = (datetime.now() - st.session_state.question_start_time).total_seconds()
        st.session_state.total_time += question_time_taken
        st.session_state.time_list.append(question_time_taken)

        # Update for the next question
        st.session_state.question_count += 1
        st.session_state.question_start_time = datetime.now()
        st.session_state.random_date = calculate_random_date()
        st.session_state.button_label = f"Check Question {st.session_state.question_count + 1}"
    
    else:
        st.success(f"{day_of_week} is OK! :thumbsup:")
        st.error(f"{day_of_week} is the right day! :coffee:")

# Cleanup
os.remove(audio_file_path)

# Actions after 5 questions
if st.session_state.question_count >= 5:
    st.session_state.show_summary = True  # Show the summary

# Display the summary and the plot if show_summary is True
if st.session_state.show_summary:
    # Calculate and display the statistics
    average_time = st.session_state.total_time / 5
    st.markdown(f"### Summary:")
    st.write(f"Total time taken for all 5 questions: {round(st.session_state.total_time, 2)} seconds")
    st.write(f"Shortest time taken: {round(min(st.session_state.time_list), 2)} seconds")
    st.markdown(f'<p style="color:red;">Average time taken: {round(average_time, 2)} seconds</p>', unsafe_allow_html=True)
    #st.write(f"Average time taken: {round(average_time, 2)} seconds")
    st.write(f"Longest time taken: {round(max(st.session_state.time_list), 2)} seconds")
    
    
    # Directly display the plot
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 6), st.session_state.time_list, marker='o', linestyle='--')
    plt.axhline(y=average_time, color='r', linestyle='-')
    plt.xlabel('Question Number')
    plt.ylabel('Time Taken (s)')
    plt.xticks(range(1, 6))  # Adjusted this line to remove decimal points on the x-axis
    plt.ylim(bottom=0)  # Make the y-axis start from 0
    plt.title('Time Taken for Each Question')
    plt.legend(['Time Taken', 'Average Time'])
    st.pyplot(plt)
    
    # Add a button to restart a new session
    if st.button("Restart"):  # New button
        st.session_state.question_count = 0
        st.session_state.total_time = 0.0
        st.session_state.time_list = []
        st.session_state.button_label = "Check Question 1"
        st.session_state.show_summary = False  # Reset the summary display
        st.experimental_rerun()  # Rerun the app to reset the display

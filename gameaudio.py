import random
import calendar
import streamlit as st
from datetime import datetime, timedelta
from gtts import gTTS
from num2words import num2words
import os
import base64

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='it')
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

# Function to generate audio
def generate_audio():
    date_words = date_to_italian_words(st.session_state.random_date)
    audio_file_path = text_to_speech(date_words)

    audio_file = open(audio_file_path, 'rb')
    audio_bytes = audio_file.read()

    audio_base64 = base64.b64encode(audio_bytes).decode()
    audio_html = f'<audio controls><source src="data:audio/mp3;base64,{audio_base64}" type="audio/mpeg"></audio>'
    st.markdown(audio_html, unsafe_allow_html=True)

    os.remove(audio_file_path)

# Initialize session state variables
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
if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

st.title(":sunglasses: What day is it? Random date 🎲")

# Generate the initial audio
generate_audio()

# Prompt the user to select the day of the week from a dropdown list
selected_day_of_week = st.selectbox(f"Select the day of the week for question {st.session_state.question_count + 1}:", list(calendar.day_name))

# Add a button to confirm the selection, label changes based on session state
check_button = st.button(st.session_state.button_label)

# Logic for checking the answer
if check_button:
    day_of_week = calendar.day_name[st.session_state.random_date.weekday()]
    
    if selected_day_of_week == day_of_week:
        st.balloons()
        st.success(f"{day_of_week} is OK! :thumbsup:")
        question_time_taken = (datetime.now() - st.session_state.question_start_time).total_seconds()
        st.session_state.total_time += question_time_taken
        st.session_state.time_list.append(question_time_taken)
        st.session_state.question_count += 1
        st.session_state.question_start_time = datetime.now()
        st.session_state.random_date = calculate_random_date()
        st.session_state.button_label = f"Check Question {st.session_state.question_count + 1}"

        # Clear and replace the audio bar
        st.markdown("", unsafe_allow_html=True)
        generate_audio()
    else:
        st.error(f"{day_of_week} is the right day! :coffee:")

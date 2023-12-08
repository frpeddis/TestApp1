import random
import calendar
import tempfile
import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from gtts import gTTS
from num2words import num2words
from io import BytesIO

# Function to convert text to speech
def text_to_speech(text, random_date):
    today = datetime.now()
    if random_date < today - timedelta(days=1):
        prefix = "Che giorno era il "
    else:
        prefix = "Che giorno sarà il "
    
    tts = gTTS(text=f"{prefix} {text}", lang='it')
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp:
        tts.save(temp.name)
        temp.seek(0)
        audio_data = temp.read()
    audio_io = BytesIO(audio_data)
    audio_io.seek(0)
    return audio_io

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
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )

# Initialize session state variables
if 'selected_day_of_week' not in st.session_state:
    st.session_state.selected_day_of_week = None
if 'random_date' not in st.session_state:
    st.session_state.random_date = calculate_random_date()

# Streamlit app title
st.title(":sunglasses: What day is it? Random date 🎲")

# Convert the date to Italian words
date_words = date_to_italian_words(st.session_state.random_date)

# Text to speech with the modified function
audio_io = text_to_speech(date_words, st.session_state.random_date)

# Streamlit audio player
audio_io.seek(0)
audio_bytes = audio_io.read()
st.audio(audio_bytes, format='audio/wav')

# Creating a row of buttons for each day of the week
days = list(calendar.day_name)
for day in days:
    if st.button(day):
        st.session_state.selected_day_of_week = day

# Button to confirm the selection
if st.session_state.selected_day_of_week is not None:
    day_of_week = calendar.day_name[st.session_state.random_date.weekday()]
    if st.session_state.selected_day_of_week == day_of_week:
        st.balloons()
        st.success(f"{day_of_week} is OK! :thumbsup:")
    else:
        st.error(f"{day_of_week} is the right day! :coffee:")

    # Prepare for next question
    st.session_state.selected_day_of_week = None
    st.session_state.random_date = calculate_random_date()
# Initialize other session state variables for summary and restart
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'error_count_list' not in st.session_state:
    st.session_state.error_count_list = [0] * 7
if 'total_time' not in st.session_state:
    st.session_state.total_time = 0.0
if 'time_list' not in st.session_state:
    st.session_state.time_list = []
if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# Update counters and timings after each question
if st.session_state.selected_day_of_week is not None:
    st.session_state.question_count += 1
    question_time_taken = (datetime.now() - st.session_state.random_date).total_seconds()
    st.session_state.total_time += question_time_taken
    st.session_state.time_list.append(question_time_taken)

    if st.session_state.question_count >= 7:
        st.session_state.show_summary = True
        st.session_state.selected_day_of_week = None

# Display summary after 7 questions
if st.session_state.show_summary:
    average_time = st.session_state.total_time / 7
    st.write(f"Total time taken for all 7 questions: {round(st.session_state.total_time, 2)} seconds")
    st.write(f"Average time taken: {round(average_time, 2)} seconds")

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 8), st.session_state.time_list, marker='o', linestyle='--', color='blue')
    plt.xlabel('Question Number')
    plt.ylabel('Time Taken (seconds)')
    plt.title('Performance Overview')
    plt.grid(True)
    st.pyplot(plt)

    if st.button("Restart"):
        st.session_state.question_count = 0
        st.session_state.error_count_list = [0] * 7
        st.session_state.total_time = 0.0
        st.session_state.time_list = []
        st.session_state.show_summary = False
        st.session_state.random_date = calculate_random_date()

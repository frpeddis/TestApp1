from gtts import gTTS
from num2words import num2words
import streamlit as st
from datetime import datetime
import random
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

# Initialize Streamlit
#st.title("App Data Casuale")

# Generate a random date (just as an example)
random_date = datetime(2023, random.randint(1, 12), random.randint(1, 28))
st.session_state.random_date = random_date
value = st.session_state.random_date.strftime("%d-%b-%Y")
description = ""

# Display the date
#st.markdown(f"{description} {value}")

# Convert the date to Italian words
date_words = date_to_italian_words(st.session_state.random_date)

# Text to speech
audio_file_path = text_to_speech(f"La data casuale è: {date_words}")

# Streamlit audio player
audio_file = open(audio_file_path, 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3')

# Cleanup
os.remove(audio_file_path)

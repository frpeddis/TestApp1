from gtts import gTTS
from num2words import num2words
import streamlit as st
from datetime import datetime
import random
import os
import base64

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
st.title("App Data Casuale")

# Generate a random date
random_date = datetime(2023, random.randint(1, 12), random.randint(1, 28))
st.session_state.random_date = random_date
value = st.session_state.random_date.strftime("%d-%b-%Y")
description = ""

# Display the date
st.markdown(f"{description} {value}")

# Convert the date to Italian words
date_words = date_to_italian_words(st.session_state.random_date)

# Text to speech
audio_file_path = text_to_speech(f"La data casuale è: {date_words}")

# Read the file and encode it
with open(audio_file_path, "rb") as f:
    audio_bytes = f.read()
audio_b64 = base64.b64encode(audio_bytes).decode()

# HTML to add audio with custom playback speed
audio_html = f'''
<audio id="audio" controls>
    <source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3">
</audio>
<script>
    var audio = document.getElementById("audio");
    audio.playbackRate = 1.5;
</script>
'''

# Streamlit audio player with custom playback speed
st.markdown(audio_html, unsafe_allow_html=True)

# Cleanup
os.remove(audio_file_path)

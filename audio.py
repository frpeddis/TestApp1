from gtts import gTTS
import streamlit as st
from datetime import datetime
import random
import os

# Function to convert text to speech
def text_to_speech(text):
    tts = gTTS(text=text, lang='en')
    filename = 'temp_audio.mp3'
    tts.save(filename)
    return filename

# Initialize Streamlit
st.title("Random Date App")

# Generate a random date (just as an example)
random_date = datetime(2023, random.randint(1, 12), random.randint(1, 28))
st.session_state.random_date = random_date
value = st.session_state.random_date.strftime("%d-%b-%Y")
description = "The random date is:"

# Display the date
st.markdown(f"{description} {value}")

# Text to speech
audio_file_path = text_to_speech(f"{description} {value}")

# Streamlit audio player
audio_file = open(audio_file_path, 'rb')
audio_bytes = audio_file.read()
st.audio(audio_bytes, format='audio/mp3')

# Cleanup
os.remove(audio_file_path)

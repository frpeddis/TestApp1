import random
import calendar
import tempfile
import streamlit as st
from datetime import datetime, timedelta
from gtts import gTTS
from num2words import num2words
from io import BytesIO
import plotly.graph_objects as go

# Funzione per convertire il testo in parlato usando gTTS
def text_to_speech(text, random_date):
    today = datetime.now()
    prefix = "Che giorno era il " if random_date < today - timedelta(days=1) else "Che giorno sarà il "
    
    # Seleziona una lingua diversa casualmente
    languages = ['it', 'fr', 'es', 'en']  # Puoi aggiungere altre lingue se lo desideri
    selected_lang = random.choice(languages)
    
    tts = gTTS(text=f"{prefix} {text}", lang=selected_lang)
    
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp:
        tts.save(temp.name)
        temp.seek(0)
        audio_data = temp.read()
    
    audio_io = BytesIO(audio_data)
    audio_io.seek(0)
    return audio_io
    # Funzione per convertire la data in parole italiane
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

# Funzione per calcolare una data casuale
def calculate_random_date():
    start_date = datetime(1582, 10, 15)
    end_date = datetime(2099, 12, 31)
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )

# Inizializza le variabili di stato della sessione
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0
if 'error_count_list' not in st.session_state:
    st.session_state.error_count_list = [0] * 5
if 'total_time' not in st.session_state:
    st.session_state.total_time = 0.0
if 'question_start_time' not in st.session_state:
    st.session_state.question_start_time = datetime.now()
if 'random_date' not in st.session_state:
    st.session_state.random_date = calculate_random_date()
if 'selected_day_of_week' not in st.session_state:
    st.session_state.selected_day_of_week = None
if 'button_label' not in st.session_state:
    st.session_state.button_label = "Check Question 1/NEXT"
if 'time_list' not in st.session_state:
    st.session_state.time_list = []
if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# Streamlit app title
st.title(":sunglasses: What's the day? 🎲")

# Convert the date to Italian words
date_words = date_to_italian_words(st.session_state.random_date)

# Text to speech with the modified function
audio_io = text_to_speech(date_words, st.session_state.random_date)

# Streamlit audio player
audio_io.seek(0)
audio_bytes = audio_io.read()
st.audio(audio_bytes, format='audio/wav')

# Function to create the pie chart
def create_pie_chart(selected_day, correct_day=None):
    days_short = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    full_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    colors = ['lightgray'] * 7

    if correct_day is not None:
        day_index = full_days.index(correct_day)
        colors[day_index] = 'green' if correct_day == selected_day else 'red'

    fig = go.Figure(data=[go.Pie(labels=days_short, values=[1]*7, marker=dict(colors=colors), hole=.3, direction='clockwise')])
    fig.update_traces(textinfo='label', textfont_size=20)
    fig.update_layout(showlegend=False)

    return fig

# User selection for day of the week (with radio buttons)
day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
selected_day = st.radio("Seleziona un giorno della settimana:", day_options)

# Button to confirm the selection and check the answer
check_button = st.button(st.session_state.button_label)

# Logic for checking the answer and updating the pie chart
if check_button and selected_day:
    day_of_week = calendar.day_name[st.session_state.random_date.weekday()]
    fig = create_pie_chart(selected_day, day_of_week)
    st.plotly_chart(fig, use_container_width=True)

    if selected_day == day_of_week:
        st.balloons()
        st.success(f"{day_of_week} è corretto! :thumbsup:")
    else:
        st.session_state.error_count_list[st.session_state.question_count] += 1
        st.error(f"{day_of_week} è il giorno giusto! :coffee:")

    question_time_taken = (
        datetime.now() - st.session_state.question_start_time
    ).total_seconds()
    st.session_state.total_time += question_time_taken
    st.session_state.time_list.append(question_time_taken)
    st.session_state.question_count += 1
    st.session_state.question_start_time = datetime.now()
    st.session_state.random_date = calculate_random_date()
    st.session_state.button_label = f"Controlla Domanda {st.session_state.question_count + 1} / NEXT"

# Show summary after 5 questions
if st.session_state.question_count >= 5:
    st.session_state.show_summary = True

if st.session_state.show_summary:
    average_time = st.session_state.total_time / 5
    st.write(f"Tempo totale impiegato per tutte le 5 domande: {round(st.session_state.total_time, 2)} secondi")
    st.write(f"Tempo più breve impiegato: {round(min(st.session_state.time_list), 2)} secondi")
    st.markdown(f'<p style="color:fuchsia;">Tempo medio impiegato: {round(average_time, 2)} secondi</p>', unsafe_allow_html=True)
    st.write(f"Tempo più lungo impiegato: {round(max(st.session_state.time_list), 2)} secondi")

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 6), st.session_state.time_list, marker='o', linestyle='--', label='Tempo Impiegato')
    
    for i, (time_taken, error_count) in enumerate(zip(st.session_state.time_list, st.session_state.error_count_list)):
        color = 'g' if error_count == 0 else 'r'
        plt.scatter(i+1, time_taken, color=color, zorder=5, s=100, label=None)
    
    plt.axhline(y=average_time, color='fuchsia', linestyle='-', label='Tempo Medio')
    plt.xlabel('Numero Domanda')
    plt.ylabel('Tempo Impiegato (s)')
    plt.xticks(range(1, 6))
    plt.ylim(bottom=0)
    plt.title('Tempo Impiegato per Ogni Domanda')
    plt.legend()
    st.pyplot(plt)

    if st.button("Ricomincia"):
        st.session_state.question_count = 0
        st.session_state.total_time = 0.0
        st.session_state.time_list = []
        st.session_state.button_label = "Controlla Domanda 1/NEXT"
        st.session_state.show_summary = False
        st.experimental_rerun()


import random
import matplotlib.pyplot as plt
import calendar
import tempfile
import streamlit as st
from datetime import datetime, timedelta
from gtts import gTTS
from num2words import num2words
from io import BytesIO
import plotly.graph_objects as go

# Function to convert the date to Italian words
def date_to_italian_words(date):
    day = date.strftime("%d")
    month = date.strftime("%m")
    year = date.strftime("%Y")
    return f"{day}/{month}/{year}"

# Function to calculate a random date
def calculate_random_date():
    start_date = datetime(1582, 10, 15)
    end_date = datetime(2099, 12, 31)
    return start_date + timedelta(
        seconds=random.randint(0, int((end_date - start_date).total_seconds()))
    )

# Initialize session state variables
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
    st.session_state.button_label = "👉 Check Question 1/NEXT"
if 'time_list' not in st.session_state:
    st.session_state.time_list = []
if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# Streamlit app title
st.title("What's the day? :sunglasses: ")

# Adding an option for "Silent mode"
silent_mode = st.checkbox("Silent mode")
if not silent_mode:
    # Function to convert text to speech using gTTS
    def text_to_speech(text, random_date):
        today = datetime.now()
        prefix = "Che giorno era il " if random_date < today - timedelta(days=1) else "Che giorno sarà il "
        
        # Always select Italian as the language
        selected_lang = 'it'
        
        tts = gTTS(text=f"{prefix} {text}", lang=selected_lang)
        
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=True) as temp:
            tts.save(temp.name)
            temp.seek(0)
            audio_data = temp.read()
        
        audio_io = BytesIO(audio_data)
        audio_io.seek(0)
        return audio_io

    # Convert the date to Italian words
    date_words = date_to_italian_words(st.session_state.random_date)

    # Text to speech with the modified function
    audio_io = text_to_speech(date_words, st.session_state.random_date)

    # Streamlit audio player
    audio_io.seek(0)
    audio_bytes = audio_io.read()
    st.audio(audio_bytes, format='audio/wav')

# Display the random date only in "Silent mode" and in the format "dd/mm/yyyy"
if silent_mode:
    date_displayed = date_to_italian_words(st.session_state.random_date)
    st.write(f"Random date: {date_displayed}")

# Creating two columns for the layout
left_column, right_column = st.columns(2)

# In the left column, place the day selection radio buttons
with left_column:
    day_options = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    st.session_state.selected_day_of_week = st.radio("Seleziona:", day_options, key="day_radio")

    # Button to confirm the selection and check the answer
    # Display the button only if question_count is less than 5
    if st.session_state.question_count < 5:
        check_button = st.button(st.session_state.button_label)
    else:
        check_button = False

# Function to create the pie chart
def create_pie_chart(selected_day, correct_day=None, is_checked=False):
    days_short = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    full_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    colors = ['lightgray'] * 7

    if selected_day:
        selected_day_index = full_days.index(selected_day)
        colors[selected_day_index] = 'violet'

        if is_checked:
            if correct_day == selected_day:
                colors[selected_day_index] = 'lightgreen'
            else:
                colors[selected_day_index] = 'red'
                correct_day_index = full_days.index(correct_day)
                colors[correct_day_index] = 'lightgreen'

    fig = go.Figure(data=[go.Pie(labels=days_short, values=[1]*7, marker=dict(colors=colors), hole=.4, direction='clockwise')])
    fig.update_traces(textinfo='label', textfont_size=15, hoverinfo='none')
    fig.update_layout(
        showlegend=False,
        height=160,
        width=160,
        margin=dict(l=8, r=8, t=8, b=8)
    )

    return fig

# In the right column, display the pie chart
with right_column:
    day_of_week = calendar.day_name[st.session_state.random_date.weekday()]
    fig = create_pie_chart(st.session_state.selected_day_of_week, day_of_week if check_button else None, check_button)
    st.plotly_chart(fig, use_container_width=True)

    if check_button:
        if st.session_state.selected_day_of_week == day_of_week:
            st.balloons()
            st.success(f"{day_of_week} is right! :thumbsup:")
        else:
            st.session_state.error_count_list[st.session_state.question_count] += 1
            st.error(f"{day_of_week} was right! :coffee:")

        question_time_taken = (
            datetime.now() - st.session_state.question_start_time
        ).total_seconds()
        st.session_state.total_time += question_time_taken
        st.session_state.time_list.append(question_time_taken)
        st.session_state.question_count += 1
        st.session_state.question_start_time = datetime.now()
        st.session_state.random_date = calculate_random_date()
        st.session_state.button_label = f"👉 Check Question {st.session_state.question_count + 1}/NEXT"

# Show summary after 5 questions
if st.session_state.question_count >= 5:
    st.session_state.show_summary = True

if st.session_state.show_summary:
    
    average_time = st.session_state.total_time / 5
    st.write(f"Total time taken for all 5 questions: {round(st.session_state.total_time, 2)} seconds")
    st.write(f"Shortest time taken: {round(min(st.session_state.time_list), 2)} seconds")
    st.markdown(f'<p style="color:fuchsia;">Average time taken: {round(average_time, 2)} seconds</p>', unsafe_allow_html=True)
    st.write(f"Longest time taken: {round(max(st.session_state.time_list), 2)} seconds")

    plt.figure(figsize=(10, 6))
    plt.plot(range(1, 6), st.session_state.time_list, marker='o', linestyle='--', label='Time Taken')
    
    for i, (time_taken, error_count) in enumerate(zip(st.session_state.time_list, st.session_state.error_count_list)):
        color = 'g' if error_count == 0 else 'r'
        plt.scatter(i+1, time_taken, color=color, zorder=5, s=100, label=None)
    
    plt.axhline(y=average_time, color='fuchsia', linestyle='-', label='Average Time')
    plt.xlabel('Question Number')
    plt.ylabel('Time Taken (s)')
    plt.xticks(range(1, 6))
    plt.ylim(bottom=0)
    plt.title('Time Taken for Each Question')
    plt.legend()
    st.pyplot(plt)

    if st.button("Restart"):
        st.session_state.question_count = 0
        st.session_state.total_time = 0.0
        st.session_state.time_list = []
        st.session_state.button_label = "👉 Check Question 1/NEXT"
        st.session_state.show_summary = False
        st.experimental_rerun()

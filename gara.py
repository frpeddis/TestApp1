import random
import calendar
import streamlit as st
from datetime import datetime, timedelta
import matplotlib.pyplot as plt  # Importing matplotlib for plotting

#  Function to calculate a random date
def calculate_random_date():
    start_date = datetime(1582, 10, 15)
    end_date = datetime(2099, 12, 31)
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

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
if 'button_label' not in st.session_state:
    st.session_state.button_label = "Check Question 1"
if 'time_list' not in st.session_state:
    st.session_state.time_list = []
if 'show_summary' not in st.session_state:
    st.session_state.show_summary = False

# Streamlit app title
st.title(":sunglasses: What day is it? Random date 🎲")

# Display the random date
description = "**Random Date:**"
value = st.session_state.random_date.strftime("%d-%b-%Y")
value = st.session_state.random_date.strftime("%d/%m/%Y") 
st.markdown(f"{description} {value}")



######################

# User selection for day of the week
selected_day_of_week = st.selectbox(
    f"Select the day of the week for question {st.session_state.question_count + 1}:",
    list(calendar.day_name),
)

# Button to confirm the selection
check_button = st.button(st.session_state.button_label)

# Logic for checking the answer
if check_button:
    day_of_week = calendar.day_name[st.session_state.random_date.weekday()]
    if selected_day_of_week == day_of_week:
        st.balloons()
        st.success(f"{day_of_week} is OK! :thumbsup:")
    else:
        st.session_state.error_count_list[st.session_state.question_count] += 1
        st.error(f"{day_of_week} is the right day! :coffee:")

    question_time_taken = (
        datetime.now() - st.session_state.question_start_time
    ).total_seconds()
    st.session_state.total_time += question_time_taken
    st.session_state.time_list.append(question_time_taken)
    st.session_state.question_count += 1
    st.session_state.question_start_time = datetime.now()
    st.session_state.random_date = calculate_random_date()
    st.session_state.button_label = f"Check Question {st.session_state.question_count + 1} / Next"

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

        
    if st.button("Restart"):  # New button
        st.session_state.question_count = 0
        st.session_state.total_time = 0.0
        st.session_state.time_list = []
        st.session_state.button_label = "Check Question 1"
        st.session_state.show_summary = False  # Reset the summary display
        st.experimental_rerun()  # Rerun the app to reset the display

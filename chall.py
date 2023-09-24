
import random
import calendar
import streamlit as st
from datetime import datetime, timedelta
import openai
import time
import streamlit.components.v1 as com
import requests
from PIL import Image
from io import BytesIO
import pandas as pd

# Checkbox to toggle image display
openai.api_key = st.secrets["API_KEY"]
st.set_page_config(page_title="🌀 WeekDay Whiz")

def generate_news(selected_date):
    prompt = f"What happens on {selected_date}?\nGive me a good news simply with an initial 😄, a neutral news simply with an initial 😐, and a bad news simply with an initial 😔. Do not mention if it is good, neutral or bad news, just use the icons. Do not mention any date in your answer. jump a line forevery news. Insert related Wikipedia links."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )
    return response.choices[0].text.strip()

# Streamlit app title
st.title(":sunglasses: What day is it? Random date 🎲")
show_images = st.checkbox("Show me how to calculate ! ")

if show_images:
    image_links = [
        "https://raw.githubusercontent.com/frpeddis/TestApp1/1ce97d47cedac010c814496ef6e34773a748cff6/MAGIC%20DAY%20CALCULATOR_1.jpeg",
        "https://raw.githubusercontent.com/frpeddis/TestApp1/1ce97d47cedac010c814496ef6e34773a748cff6/MAGIC%20DAY%20CALCULATOR_2.jpeg",
        "https://raw.githubusercontent.com/frpeddis/TestApp1/1ce97d47cedac010c814496ef6e34773a748cff6/MAGIC%20DAY%20CALCULATOR_3.jpeg",
        "https://raw.githubusercontent.com/frpeddis/TestApp1/1ce97d47cedac010c814496ef6e34773a748cff6/MAGIC%20DAY%20CALCULATOR_4.jpeg"
    ]
    for i, link in enumerate(image_links):
        response = requests.get(link)
        img = Image.open(BytesIO(response.content))
        st.image(img, use_column_width=True)

# Function to calculate a random date
def calculate_random_date():
    start_date = datetime(1582, 10, 15)
    end_date = datetime(2099, 12, 31)
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Initialize a variable to store the lowest time record, setting it to a high value initially
lowest_time_record = 1e6  # 1 million seconds as an initial high value

# Initialize a variable to store the start time
start_time = datetime.now()

# Initialize a loop to ask questions 5 times
for i in range(5):
    # Generate a random date
    random_date = calculate_random_date()
    
    # Display the random date
    description = "**Random Date:**"
    value = random_date.strftime("%d-%b-%Y")
    st.markdown(f"{description} {value}")
    
    # Prompt the user to select the day of the week from a dropdown list
    selected_day_of_week = st.selectbox(f"Select the day of the week for question {i+1}:", list(calendar.day_name))
    
    # Add a "Check" button to confirm the selection
    check_button = st.button(f"Check for question {i+1}")
    
    # Logic for checking the answer
    if check_button:
        # Confirm the day of the week selected by the user
        day_of_week = calendar.day_name[random_date.weekday()]
        if selected_day_of_week == day_of_week:
            st.balloons()
            st.success(day_of_week + " is OK! :thumbsup:")
        else:
            com.iframe("https://lottie.host/?file=380d3ff9-0c30-4a96-b25b-7eeb8868bfeb/vnvhMZFQ8j.json")
            st.error(day_of_week + " is the right day! :coffee: That's why...")

# Calculate the total time taken to complete all 5 questions
time_taken = (datetime.now() - start_time).total_seconds()

# Check if the time taken is less than the current lowest time record
if time_taken < lowest_time_record:
    # Update the lowest time record
    lowest_time_record = time_taken
    st.write(f"New record! Lowest time taken: {lowest_time_record} seconds")
else:
    st.write(f"Time taken: {time_taken} seconds")

# Display the total time taken and the lowest time record
st.write(f"Total time taken to complete all 5 questions: {time_taken} seconds")
st.write(f"Lowest time record: {lowest_time_record} seconds")

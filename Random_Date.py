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

# Checkbox to toggle image display
show_images = st.checkbox("Show me how to calculate!")

if show_images:
    # First image
    url1 = "https://raw.githubusercontent.com/frpeddis/TestApp1/8e0d72dc7d773c2061ab58791b4c7bc3fd3332ea/MAGIC%20DAY%20CALCULATOR%20ADVENTURE%201.jpg"
    response1 = requests.get(url1)
    img1 = Image.open(BytesIO(response1.content))
    st.image(img1, use_column_width=True)

    # Second image
    url2 = "https://raw.githubusercontent.com/frpeddis/TestApp1/7f1918029c103ff0eaf318cb1e692a688f94fdbd/MAGIC%20DAY%20CALCULATOR%20ADVENTURE%202.jpg"
    response2 = requests.get(url2)
    img2 = Image.open(BytesIO(response2.content))
    st.image(img2, use_column_width=True)

openai.api_key = st.secrets["API_KEY"]

def generate_news(selected_date):
    prompt = f"What happened on {selected_date}?\nGive me a good news simply with an initial 😄, a neutral news simply with an initial 😐, and a bad news simply with an initial 😔. Do not mention if it is good, neutral or bad news, just use the icons. Do not mention any date in your answer. jump a line forevery news. Insert related Wikipedia links."

    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=200,
        temperature=0.7
    )

    return response.choices[0].text.strip()



# Streamlit app title
st.title(":sunglasses: What day was it?")

# Function to calculate a random date
def calculate_random_date():
    start_date = datetime(1582, 10, 15)
    end_date = datetime(2099, 12, 31)
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Check if random_date and start_time are in session state, if not, calculate and store them
if 'random_date' not in st.session_state:
    st.session_state.random_date = calculate_random_date()
    

if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()

if 'check_pressed' not in st.session_state:
    st.session_state.check_pressed = False

if 'time_taken' not in st.session_state:
    st.session_state.time_taken = 0

# Display the date in the format dd-mmm-yyyy
st.write("Random Date:", st.session_state.random_date.strftime("%d-%b-%Y"))
selected_date = st.session_state.random_date.strftime("%d-%b-%Y")
#com.iframe("https://lottie.host/?file=380d3ff9-0c30-4a96-b25b-7eeb8868bfeb/vnvhMZFQ8j.json")


# Calculate time taken
if not st.session_state.check_pressed:
    time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
    display_time_taken = False
else:
    time_taken = st.session_state.time_taken
    display_time_taken = True

# Prompt the user to select the day of the week from a dropdown list
selected_day_of_week = st.selectbox("Select the day of the week:", list(calendar.day_name))

# Add a "Check" button to confirm the selection
check_button = st.button("Check")



if check_button:
    st.session_state.check_pressed = True

    # Confirm the day of the week selected by the user
    day_of_week = calendar.day_name[st.session_state.random_date.weekday()]

    if selected_day_of_week == day_of_week:
        st.balloons()
        st.success(day_of_week + " is OK! :thumbsup:")
                
    else:
        st.error(day_of_week + " was the right day! :coffee: Try again...")
        com.iframe("https://lottie.host/?file=380d3ff9-0c30-4a96-b25b-7eeb8868bfeb/vnvhMZFQ8j.json")
        
    
        #pdf_url = "https://github.com/frpeddis/TestApp1/raw/9a5249fa93ebbb3d724c139f48c27476c30d0cd4/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"
        #st.markdown(f"[Download MAGIC DAY CALCULATOR ADVENTURE!]({pdf_url})")



        
        

    # Calculate time taken to make the selection
    st.session_state.time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
    time_taken = st.session_state.time_taken
    display_time_taken = True

# Show the amount of seconds taken
if display_time_taken:
    st.write(":hourglass: Time taken to check:", round(time_taken, 2), "seconds")

    if st.button("In that period..."):
            news_summary = generate_news(selected_date)
            st.header("Please verify, but according to ChatGPT in that period... ")
            st.write(news_summary)

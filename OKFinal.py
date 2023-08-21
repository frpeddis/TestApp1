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

openai.api_key = st.secrets["API_KEY"]

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
st.title(":sunglasses: What day is it?")
show_images = st.checkbox("Show me how to calculate !")

if show_images:
    image_links = [
        "https://raw.githubusercontent.com/frpeddis/TestApp1/1ce97d47cedac010c814496ef6e34773a748cff6/MAGIC%20DAY%20CALCULATOR_1.jpeg",
        "https://raw.githubusercontent.com/frpeddis/TestApp1/1ce97d47cedac010c814496ef6e34773a748cff6/MAGIC%20DAY%20CALCULATOR_2.jpeg",
        "https://raw.githubusercontent.com/frpeddis/TestApp1/1ce97d47cedac010c814496ef6e34773a748cff6/MAGIC%20DAY%20CALCULATOR_3.jpeg",
        "https://raw.githubusercontent.com/frpeddis/TestApp1/1ce97d47cedac010c814496ef6e34773a748cff6/MAGIC%20DAY%20CALCULATOR_4.jpeg"    ]
    
    for i, link in enumerate(image_links):
        response = requests.get(link)
        img = Image.open(BytesIO(response.content))
        st.image(img, use_column_width=True)


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
description = "**Random Date:**"
value = "**" + st.session_state.random_date.strftime("%d-%b-%Y") + "**"
st.markdown(f"{description} {value}")
#st.write("**Random Date:**", st.session_state.random_date.strftime("%d-%b-%Y"))
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
        st.error(day_of_week + " is the right day! :coffee: Try again...")
        com.iframe("https://lottie.host/?file=380d3ff9-0c30-4a96-b25b-7eeb8868bfeb/vnvhMZFQ8j.json")
        
        selected_date = st.session_state.random_date
        
        if selected_date:
            st.write("Date:", selected_date.strftime("%d-%b-%Y"))
        
            # Step 2: Take the last 2 digits of the year
            year_last_2_digits = selected_date.year % 100
        
            # Step 3: Divide the year number by 4 and add it
            year_divided_by_4 = year_last_2_digits // 4
            subtotal = year_last_2_digits + year_divided_by_4
        
            # Step 4: Add the "Century Correction"
            century_correction_table = {
                "Century": [1500, 1600, 1700, 1800, 1900, 2000],
                "Correction": [0, 6, 4, 2, 0, -1]
            }
            century = (selected_date.year // 100) * 100
            century_correction_value = century_correction_table["Correction"][century_correction_table["Century"].index(century)]
            subtotal += century_correction_value
        
            # Step 5: Add the "Month Coefficient"
            month_coefficients = {
                "January": 1 if not (selected_date.year % 4 == 0 and selected_date.month <= 2) else 0,
                "February": 4 if not (selected_date.year % 4 == 0 and selected_date.month <= 2) else 3,
                "March": 4, "April": 0, "May": 2, "June": 5,
                "July": 0, "August": 3, "September": 6,
                "October": 1, "November": 4, "December": 6
            }
            month = selected_date.strftime("%B")
            month_coefficient = month_coefficients[month]
            subtotal += month_coefficient
        
            # Step 6: Add the day of the month
            day_of_month = selected_date.day
            subtotal += day_of_month
        
            # Step 7: Divide the subtotal by 7 and find the remainder
            remainder = subtotal % 7
        
            # Display calculated string
            calculated_string = f"{year_last_2_digits} + {year_divided_by_4} + {century_correction_value} + {month_coefficient} + {day_of_month}"
            st.write("Magic Sum: ", calculated_string, " = ", f"<span style='font-size:18px; font-weight:bold;'>{subtotal}</span>", unsafe_allow_html=True)
            #st.write("Magic Sum: ", calculated_string, " = ", subtotal)
            
            
            # Step 2: Take the last 2 digits of the year (continued)
            st.write(year_last_2_digits, ": Last 2 digits of the year")
        
            # Step 3: Divide the year number by 4 and add it (continued)
            st.write(year_divided_by_4, ": Integer part of year YY divided by 4")
            
            # Step 4: Add the "Century Correction" (continued)
            st.write(century_correction_value, ": Century Correction")
          
            # Step 5: Add the "Month Coefficient" (continued)
            st.write(month_coefficient, ": Month Coefficient")
        
            # Step 6: Add the day of the month (continued)
            st.write(day_of_month, ": Day of the month")
            
            # Step 7: Divide the subtotal by 7 and find the remainder (continued)
            st.write("Remainder after dividing ", subtotal, "  by 7:", remainder)
            
            

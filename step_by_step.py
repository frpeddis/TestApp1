import streamlit as st
from datetime import datetime, timedelta
import requests
from PIL import Image
from io import BytesIO
import calendar

# Streamlit app title
st.title(":sunglasses: What day is it?")
show_calculation = st.checkbox("Show me how to calculate the day of the week")

if show_calculation:
    # Step 1: Use selected_date variable as a starting point
    selected_date = st.date_input("Select a date:")
    
    # Step 2: Take the last 2 digits of the year
    year_last_two_digits = selected_date.year % 100
    
    # Step 3: Divide the year number by 4, without the remainder, and add it
    year_divided_by_4 = year_last_two_digits // 4
    subtotal = year_last_two_digits + year_divided_by_4
    
    # Step 4: Add the "Century Correction"
    century_correction = {1500: 0, 1600: 6, 1700: 4, 1800: 2, 1900: 0, 2000: -1}
    century = (selected_date.year // 100) * 100
    subtotal += century_correction.get(century, 0)
    
    # Step 5: Add the "Month Coefficient"
    month_coefficients = [1, 4, 4, 0, 2, 5, 0, 3, 6, 1, 4, 6]
    month_coefficient = month_coefficients[selected_date.month - 1]
    if selected_date.month <= 2 and (selected_date.year % 4 == 0 and (selected_date.year % 100 != 0 or selected_date.year % 400 == 0)):
        month_coefficient -= 1  # Leap year adjustment
    subtotal += month_coefficient
    
    # Step 6: Add the day of the month
    day_of_month = selected_date.day
    subtotal += day_of_month
    
    # Step 7: Divide the subtotal by 7 and find the remainder
    remainder = subtotal % 7
    
    # Step 8: Look at the remainder and find the day of the week
    days_of_week = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    day_of_week = days_of_week[remainder]
    
    st.markdown(f"**Calculation Steps:**\n"
                f"1. Use selected_date: {selected_date}\n"
                f"2. Take the last 2 digits of the year: {year_last_two_digits}\n"
                f"3. Divide the year number by 4 and add it: {subtotal - year_last_two_digits}\n"
                f"4. Add the 'Century Correction': {subtotal - year_divided_by_4}\n"
                f"5. Add the 'Month Coefficient': {subtotal - century_correction.get(century, 0)}\n"
                f"6. Add the day of the month: {subtotal - month_coefficient}\n"
                f"7. Divide the subtotal by 7 and find the remainder: {remainder}\n"
                f"8. Look at the remainder and find the day of the week: {day_of_week}")
    
    st.markdown(f"**Day of the Week Calculation:**\n"
                f"The day of the week for {selected_date.strftime('%B %d, %Y')} is **{day_of_week}**.")

# Rest of your code...

#openai.api_key = st.secrets["API_KEY"]

# Function to generate news based on the selected date
#def generate_news(selected_date):
    # Your news generation logic here...
 #   pass

# Rest of your code for displaying images and getting user inputs...

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
        # Rest of your error handling logic...

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





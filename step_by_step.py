import random
import calendar
import streamlit as st
from datetime import datetime, timedelta

# Streamlit app title
st.title("What day was it ? - Random choice:sunglasses:")

# Function to calculate a random date
def calculate_random_date():
    start_date = datetime(1582, 10, 15)
    end_date = datetime(2099, 12, 31)
    return start_date + timedelta(seconds=random.randint(0, int((end_date - start_date).total_seconds())))

# Check if random_date and start_time are in session state, if not, calculate and store them
if 'random_date' not in st.session_state:
    st.session_state.random_date = calculate_random_date()
    selected_date = st.session_state.random_date
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()

if 'check_pressed' not in st.session_state:
    st.session_state.check_pressed = False

if 'time_taken' not in st.session_state:
    st.session_state.time_taken = 0

# Display the date in the format dd-mmm-yyyy
st.write("Random Date:", st.session_state.random_date.strftime("%d-%b-%Y"))

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
        st.success(day_of_week + " OK")
    else:
        st.error(day_of_week + " WRONG!!!")
               
            st.write("Step 1: Selected Date:", selected_date.strftime("%d-%b-%Y"))
        
            # Step 2: Take the last 2 digits of the year
            year_last_2_digits = selected_date.year % 100
            st.write("Step 2: Last 2 digits of the year:", year_last_2_digits)
        
            # Step 3: Divide the year number by 4 and add it
            year_divided_by_4 = year_last_2_digits // 4
            st.write("Step 3: Integer part of year divided by 4:", year_divided_by_4)
            subtotal = year_last_2_digits + year_divided_by_4
            st.write("    Subtotal after year division:", subtotal)
        
            # Display Century Correction Table
            century_correction_table = {
                "Century": [1500, 1600, 1700, 1800, 1900, 2000],
                "Correction": [0, 6, 4, 2, 0, -1]
            }
            st.write("Step 4: Century Correction Table:")
            formatted_century_correction_table = [
                ["Century", "Correction"],
                *[[f"**{century}**", f"**{correction}**"] if century == (selected_date.year // 100) * 100 else [century, correction]
                  for century, correction in zip(century_correction_table["Century"], century_correction_table["Correction"])]
            ]
            st.table(formatted_century_correction_table)
        
            # Step 4: Add the "Century Correction"
            century = (selected_date.year // 100) * 100
            century_correction_value = century_correction_table["Correction"][century_correction_table["Century"].index(century)]
            st.write("Step 4: Century Correction value:", century_correction_value)
            subtotal += century_correction_value
            st.write("    Subtotal after century correction:", subtotal)
        
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
            st.write("Step 5: Month Coefficient value:", month_coefficient)
            subtotal += month_coefficient
            st.write("    Subtotal after month coefficient:", subtotal)
        
            # Display Month Coefficient Table
            st.write("Step 5: Month Coefficient Table:")
            formatted_month_coefficients_table = [
                ["Month", "Coefficient"],
                *[[f"**{month}**", f"**{coeff}**"] if month == selected_date.strftime("%B") else [month, coeff]
                  for month, coeff in month_coefficients.items()]
            ]
            st.table(formatted_month_coefficients_table)
        
            # Step 6: Add the day of the month
            day_of_month = selected_date.day
            st.write("Step 6: Day of the month:", day_of_month)
            subtotal += day_of_month
            st.write("    Subtotal after adding day of the month:", subtotal)
        
            # Step 7: Divide the subtotal by 7 and find the remainder
            remainder = subtotal % 7
            st.write("Step 7: Remainder after dividing by 7:", remainder)
        
            # Display Correspondence Table
            st.write("Correspondence between Remainders and Days of the Week:")
            correspondence_table = {
                "Remainder": list(range(7)),
                "Day of the Week": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
            }
            formatted_correspondence_table = [
                ["Remainder", "Day of the Week"],
                *[[f"**{remainder}**", f"**{day}**"] if remainder == remainder else [remainder, day]
                  for remainder, day in zip(correspondence_table["Remainder"], correspondence_table["Day of the Week"])]
            ]
            st.table(formatted_correspondence_table)


    # Calculate time taken to make the selection
    st.session_state.time_taken = (datetime.now() - st.session_state.start_time).total_seconds()
    time_taken = st.session_state.time_taken
    display_time_taken = True

# Show the amount of seconds taken
if display_time_taken:
    st.write("Time taken to check:", round(time_taken, 2), "seconds")

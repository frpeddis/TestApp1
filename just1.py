import streamlit as st
from datetime import datetime

# Streamlit app title
st.title("Calculate Day of the Week")

# Step 1: User selects a date
selected_date = st.date_input("Select a date")

if selected_date:
    st.write("Selected Date:", selected_date.strftime("%d-%b-%Y"))

    # Step 2: Take the last 2 digits of the year
    year_last_2_digits = selected_date.year % 100

    # Step 3: Divide the year number by 4 and add it
    year_divided_by_4 = year_last_2_digits // 4
    subtotal = year_last_2_digits + year_divided_by_4

    # Step 4: Add the "Century Correction"
    century_correction = {
        1500: 0,
        1600: 6,
        1700: 4,
        1800: 2,
        1900: 0,
        2000: -1
    }
    century = (selected_date.year // 100) * 100
    century_correction_value = century_correction.get(century, 0)
    subtotal += century_correction_value

    # Step 5: Add the "Month Coefficient"
    month_coefficients = {
        1: 1 if not (selected_date.year % 4 == 0 and selected_date.month <= 2) else 0,
        2: 4 if not (selected_date.year % 4 == 0 and selected_date.month <= 2) else 3,
        3: 4,
        4: 0,
        5: 2,
        6: 5,
        7: 0,
        8: 3,
        9: 6,
        10: 1,
        11: 4,
        12: 6
    }
    month_coefficient = month_coefficients[selected_date.month]
    subtotal += month_coefficient

    # Step 6: Add the day of the month
    day_of_month = selected_date.day
    subtotal += day_of_month

    # Step 7: Divide the subtotal by 7 and find the remainder
    remainder = subtotal % 7

    # Step 8: Find the day of the week
    days_of_week = [
        "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
    ]
    day_of_week = days_of_week[remainder]

    # Display the calculated day of the week
    st.write("Calculated Day of the Week:", day_of_week)

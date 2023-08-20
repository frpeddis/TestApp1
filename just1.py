import streamlit as st
from datetime import datetime

# Streamlit app title
st.title("Calculate Day of the Week")

# Step 1: User selects a date
selected_date = st.date_input("Step 1: Select a date")

if selected_date:
    st.write("Step 1: Selected Date:", selected_date.strftime("%d-%b-%Y"))

    # Step 2: Take the last 2 digits of the year
    year_last_2_digits = selected_date.year % 100
    st.write("Step 2: Last 2 digits of the year:", year_last_2_digits)

    # Step 3: Divide the year number by 4 and add it
    year_divided_by_4 = year_last_2_digits // 4
    st.write("Step 3: Integer part of year divided by 4:", year_divided_by_4)
    subtotal = year_last_2_digits + year_divided_by_4
    st.write("    Subtotal after year division:", subtotal)

    # Step 4: Add the "Century Correction"
    century_correction = {
        1500: 0, 1600: 6, 1700: 4, 1800: 2, 1900: 0, 2000: -1
    }
    century = (selected_date.year // 100) * 100
    century_correction_value = century_correction.get(century, 0)
    st.write("Step 4: Century Correction value:", century_correction_value)
    subtotal += century_correction_value
    st.write("    Subtotal after century correction:", subtotal)
    
    # Display Century Correction Table
    st.write("    Century Correction Table:")
    st.table(century_correction)

    # Step 5: Add the "Month Coefficient"
    month_coefficients = {
        1: 1 if not (selected_date.year % 4 == 0 and selected_date.month <= 2) else 0,
        2: 4 if not (selected_date.year % 4 == 0 and selected_date.month <= 2) else 3,
        3: 4, 4: 0, 5: 2, 6: 5, 7: 0, 8: 3, 9: 6, 10: 1, 11: 4, 12: 6
    }
    month_coefficient = month_coefficients[selected_date.month]
    st.write("Step 5: Month Coefficient value:", month_coefficient)
    subtotal += month_coefficient
    st.write("    Subtotal after month coefficient:", subtotal)
    
    # Display Month Coefficient Table
    st.write("    Month Coefficient Table:")
    st.table(month_coefficients)

    # Step 6: Add the day of the month
    day_of_month = selected_date.day
    st.write("Step 6: Day of the month:", day_of_month)
    subtotal += day_of_month
    st.write("    Subtotal after adding day of the month:", subtotal)

    # Step 7: Divide the subtotal by 7 and find the remainder
    remainder = subtotal % 7
    st.write("Step 7: Remainder after dividing by 7:", remainder)

    # Step 8: Find the day of the week
    days_of_week = [
        "Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"
    ]
    day_of_week = days_of_week[remainder]
    st.write("Step 8: Calculated Day of the Week:", day_of_week)
    
    # Display Correspondence Table
    correspondence_table = {
        "Remainder": list(range(7)),
        "Day of the Week": days_of_week
    }
    st.write("Correspondence between Remainders and Days of the Week:")
    st.table(correspondence_table)



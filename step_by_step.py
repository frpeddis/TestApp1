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

# ... (rest of the code remains the same)

# Display Century Correction Table
st.write("Century Correction:")
formatted_century_correction_table = []
for century, correction in zip(century_correction_table["Century"], century_correction_table["Correction"]):
    if century == (selected_date.year // 100) * 100:
        formatted_century_correction_table.append(["**" + str(century) + "**", "**" + str(correction) + "**"])
    else:
        formatted_century_correction_table.append([str(century), str(correction)])
st.table(formatted_century_correction_table, header=["Century", "Value"])

# ... (rest of the code remains the same)

# Display Month Coefficient Table (continued)
st.write("Month Coefficients:")
formatted_month_coefficients_table = []
for month, coeff in month_coefficients.items():
    if month == selected_date.strftime("%B"):
        formatted_month_coefficients_table.append(["**" + month + "**", "**" + str(coeff) + "**"])
    else:
        formatted_month_coefficients_table.append([month, str(coeff)])
st.table(formatted_month_coefficients_table, header=["Month", "Value"])

# ... (rest of the code remains the same)

# Display Correspondence Table
st.write("Correspondence between Remainders and Days of the Week:")
correspondence_table = {
    "Remainder": list(range(7)),
    "Day of the Week": ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
}
formatted_correspondence_table = []
for r, d in zip(correspondence_table["Remainder"], correspondence_table["Day of the Week"]):
    if r == remainder:
        formatted_correspondence_table.append(["**" + str(r) + "**", "**" + d + "**"])
    else:
        formatted_correspondence_table.append([str(r), d])
st.table(formatted_correspondence_table, header=["Reminder", "Day of the week"])

import streamlit as st
import pandas as pd

# Title of the app
st.title('CSV File Upload and Display')

# Instruction
st.markdown('**Please upload a CSV file to view its content.**')

# File uploader allows user to add their own CSV
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

# Check if there is a file uploaded
if uploaded_file is not None:
    # Read the CSV file
    df = pd.read_csv(uploaded_file)
    
    # Show the content of the CSV file
    st.write(df)

# If no file is uploaded, show a message
else:
    st.write("Please upload a CSV file to proceed.")

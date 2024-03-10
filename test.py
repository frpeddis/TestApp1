import streamlit as st
import pandas as pd

# URL of the CSV file
csv_url = 'https://raw.githubusercontent.com/frpeddis/TestApp1/main/events366.csv'

# Function to load data from URL
def load_data(url):
    try:
        data = pd.read_csv(url)
        return data
    except Exception as e:
        st.error(f"An error occurred while loading the data: {e}")
        return None

# Load data
data = load_data(csv_url)

# Display the loaded data
if data is not None:
    st.write("## CSV Data:")
    st.write(data)

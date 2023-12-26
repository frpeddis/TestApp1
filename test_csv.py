# app.py, run with 'streamlit run app.py'
import pandas as pd
import streamlit as st


df = pd.read_csv("https://raw.githubusercontent.com/frpeddis/TestApp1/main/Invenzioni.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
# df = pd.read_excel(...)  # will work for Excel files

st.title("Hello world!")  # add a title
st.write(df)  # visualize my dataframe in the Streamlit app






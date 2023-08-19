import streamlit as st
import requests
from PIL import Image
from io import BytesIO

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

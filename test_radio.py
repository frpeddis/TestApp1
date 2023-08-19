import streamlit as st
import requests
from PIL import Image
from io import BytesIO

url = "https://raw.githubusercontent.com/frpeddis/TestApp1/8e0d72dc7d773c2061ab58791b4c7bc3fd3332ea/MAGIC%20DAY%20CALCULATOR%20ADVENTURE%201.jpg"

response = requests.get(url)
img = Image.open(BytesIO(response.content))

st.image(img, caption='Image Caption', use_column_width=True)

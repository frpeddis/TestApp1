import streamlit as st
from PIL import Image
import requests
from io import BytesIO

url = "https://github.com/frpeddis/TestApp1/blob/8e0d72dc7d773c2061ab58791b4c7bc3fd3332ea/MAGIC%20DAY%20CALCULATOR%20ADVENTURE%201.jpg"

response = requests.get(url)
img = Image.open(BytesIO(response.content))

st.image(img, caption='Image Caption', use_column_width=True)

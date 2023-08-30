import os
import streamlit as st
import numpy as np
import pytesseract 
from PIL import Image 

# Use an environment variable to get the Tesseract path, or set a default.
tesseract_path = os.environ.get('TESSERACT_PATH', 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe')
pytesseract.pytesseract.tesseract_cmd = tesseract_path

st.title("Our OCR APP")
st.text("Upload an image that contains English text")

upload_image = st.sidebar.file_uploader('Choose an image for conversion', type=["jpg", "png", "jpeg"])

if upload_image is not None:
    try:
        img = Image.open(upload_image)
        st.image(upload_image, caption="Uploaded Image")
        
        if st.button("Extract Text"):
            st.write("Extracted Text")
            output_text = pytesseract.image_to_string(img)
            st.write(output_text)
    except Exception as e:
        st.write("An error occurred: ", str(e))

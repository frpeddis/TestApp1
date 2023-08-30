import streamlit as st
from PIL import Image
import pytesseract

st.title("OCR App")

uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image", use_column_width=True)
    st.write("")

    st.write("Recognized Text")

    # Perform OCR
    text = pytesseract.image_to_string(image)
    st.write(text)

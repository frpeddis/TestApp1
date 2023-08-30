import streamlit as st
import pytesseract
from PIL import Image

st.title("Our OCR APP")
st.text("Upload an image that contains English text")

upload_image = st.sidebar.file_uploader('Choose an image for conversion', type=["jpg", "png", "jpeg"])

if upload_image is not None:
    try:
        img = Image.open(upload_image)
        st.image(upload_image, caption="Uploaded Image")

        if st.button("Extract Text"):
            st.write("Extracted Text")
            output_text = pytesseract.image_to_string(img, lang='eng', config='--psm 6')
            st.write(output_text)
    except Exception as e:
        st.write("An error occurred: ", str(e))



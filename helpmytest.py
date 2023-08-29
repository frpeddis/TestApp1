import pytesseract
import streamlit as st
import openai
import time
import streamlit.components.v1 as com
import requests
from PIL import Image
from io import BytesIO
import pandas as pd


openai.api_key = st.secrets["API_KEY"]



# Initialize Streamlit app
st.title("OCR and GPT-based Multi-choice Test Answering")

# Step 1: Upload Image
uploaded_image = st.file_uploader("Upload an image containing the multi-choice test question", type=["jpg", "png", "jpeg"])

if uploaded_image:
    # Display the uploaded image
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)
  
    # Open the uploaded image with PIL for OCR
    image = Image.open(uploaded_image)
  
    # Step 2: OCR to Extract Text
    ocr_result = pytesseract.image_to_string(image)
    st.write("Extracted Text: ", ocr_result)
  
    # Step 3: Send OCR Result to OpenAI GPT API
    GPT_API_KEY = st.secrets["API_KEY"]
    headers = {"Authorization": f"Bearer {GPT_API_KEY}"}
  
    data = {
        "prompt": f"The question is: {ocr_result}. What is the answer?",
        "max_tokens": 200
    }
  
    response = requests.post("https://api.openai.com/v1/engines/davinci-codex/completions", headers=headers, json=data)
  
    # Extract the answer from the API response
    if response.status_code == 200:
        answer = response.json()['choices'][0]['text'].strip()
        # Step 4: Display Answer
        st.write("Answer from GPT: ", answer)
    else:
        st.write("Could not get an answer from the API. Please try again.")


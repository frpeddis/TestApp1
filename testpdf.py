import streamlit as st
import PyPDF2
import io
from PIL import Image

# Title
st.title("PDF Viewer")

# PDF URL
pdf_url = "https://github.com/frpeddis/TestApp1/raw/93b1fee0e377a121c753ff8d33c46227d11616b4/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"

# Function to convert PDF page to image
def pdf_page_to_image(pdf_bytes, page_num):
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    page = pdf_reader.pages[page_num - 1]
    xObject = page['/Resources']['/XObject'].get_object()
    img = xObject[list(xObject.keys())[0]].get_object()
    img_stream = img['/Filter'][1].get_object()
    return img_stream

# Load PDF page as image
page_number = st.number_input("Enter page number:", min_value=1, max_value=10, value=1)  # Adjust max_value as needed
pdf_response = st.download_button("Download PDF", pdf_url)
if pdf_response is not None:
    pdf_image = pdf_page_to_image(pdf_response.read(), page_number)
    img = Image.open(io.BytesIO(pdf_image))
    st.image(img)



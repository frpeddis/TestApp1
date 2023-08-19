import streamlit as st
import fitz  # PyMuPDF

# Title
st.title("PDF Viewer")

# PDF URL
pdf_url = "https://github.com/frpeddis/TestApp1/raw/93b1fee0e377a121c753ff8d33c46227d11616b4/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"

# Display PDF using PyMuPDF
pdf_document = fitz.open(pdf_url, filetype="pdf")
num_pages = pdf_document.page_count
page_number = st.number_input("Enter page number:", min_value=1, max_value=num_pages, value=1)

page = pdf_document.load_page(page_number - 1)
image = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # Adjust the matrix values for zoom

st.image(image)




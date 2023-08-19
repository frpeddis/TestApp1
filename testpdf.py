import streamlit as st

# Title
st.title("PDF Viewer")

# PDF URL
pdf_url = "https://github.com/frpeddis/TestApp1/raw/93b1fee0e377a121c753ff8d33c46227d11616b4/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"

# Display PDF using iframe
st.markdown(f'<iframe src="{pdf_url}" width="800" height="600"></iframe>', unsafe_allow_html=True)



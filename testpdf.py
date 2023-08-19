import streamlit as st

# Title
st.title("PDF Viewer")

# Link to PDF
pdf_url = "https://github.com/frpeddis/TestApp1/blob/93b1fee0e377a121c753ff8d33c46227d11616b4/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"
st.markdown(f"Download [file.pdf]({pdf_url})")

# Open PDF in Streamlit
if st.button("How to"):
    st.write("Here's the PDF:")
    st.write(f"Download [file.pdf]({pdf_url}) and follow the instructions.")
    st.markdown(f'<iframe src="{pdf_url}" width="100%" height="600px"></iframe>', unsafe_allow_html=True)


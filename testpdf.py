import streamlit as st
import requests
from io import BytesIO

def main():
    st.title("PDF Viewer")

    pdf_url = "https://github.com/frpeddis/TestApp1/raw/ad57d944ad9141a2b973d60bf7f0230dbb8c3b32/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"

    st.write("Displaying PDF:")
    
    try:
        response = requests.get(pdf_url)
        if response.status_code == 200:
            st.write(f"PDF loaded successfully:")
            pdf_data = BytesIO(response.content)
            st.write(pdf_data.read())
        else:
            st.write("Failed to fetch PDF.")
    except requests.exceptions.RequestException as e:
        st.write("An error occurred:", e)

if __name__ == "__main__":
    main()

import streamlit as st
import requests

def main():
    st.title("PDF Downloader")

    pdf_url = "https://github.com/frpeddis/TestApp1/raw/9a5249fa93ebbb3d724c139f48c27476c30d0cd4/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"

    st.write("Click the button below to download the PDF:")
    if st.button("Download PDF"):
        download_pdf(pdf_url)

def download_pdf(pdf_url):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open("MAGIC_DAY_CALCULATOR_ADVENTURE.pdf", "wb") as f:
            f.write(response.content)
        st.success("PDF downloaded successfully!")
    else:
        st.error("Failed to download PDF")

if __name__ == "__main__":
    main()


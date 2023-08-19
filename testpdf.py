import streamlit as st

def main():
    st.title("PDF Downloader")

    pdf_url = "https://github.com/frpeddis/TestApp1/raw/9a5249fa93ebbb3d724c139f48c27476c30d0cd4/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"

    st.write("Click the link below to download the PDF:")
    st.markdown(f"[Download PDF]({pdf_url})")

if __name__ == "__main__":
    main()

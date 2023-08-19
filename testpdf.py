import streamlit as st

def main():
    st.title("PDF Viewer")

    pdf_url = "URL_TO_YOUR_PDF"  # Replace with the URL of your PDF

    st.write("Embedding PDF using Google Docs Viewer:")
    st.write(f'<iframe src="https://docs.google.com/viewer?url={pdf_url}&embedded=true" width="800" height="600"></iframe>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()


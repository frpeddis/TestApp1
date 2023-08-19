import streamlit as st

def main():
    st.title("PDF Viewer")

    pdf_url = "URL_TO_YOUR_PDF"  # Replace with the URL of your PDF

    st.write("Embedding PDF using iframe:")
    st.components.v1.iframe(pdf_url, width=800, height=600)

if __name__ == "__main__":
    main()

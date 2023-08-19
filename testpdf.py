import streamlit as st

def main():
    st.title("PDF Viewer")

    pdf_url = "https://github.com/frpeddis/TestApp1/blob/ad57d944ad9141a2b973d60bf7f0230dbb8c3b32/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"  # Replace with the URL of your PDF

    st.write("Embedding PDF using iframe:")
    st.components.v1.iframe(pdf_url, width=800, height=600)

if __name__ == "__main__":
    main()

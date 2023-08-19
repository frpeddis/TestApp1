import streamlit as st

def main():
    st.title("PDF Viewer")

    pdf_url = "https://github.com/frpeddis/TestApp1/raw/ad57d944ad9141a2b973d60bf7f0230dbb8c3b32/MAGIC%20DAY%20CALCULATOR%20ADVENTURE.pdf"

    st.write("Embedding PDF using iframe:")
    st.write(f'<iframe src="{pdf_url}" width="800" height="600"></iframe>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()

import streamlit as st
import requests
from PIL import Image
from io import BytesIO

def main():
    st.title("Image Details Viewer")

    # URLs of the JPG images in your GitLab repository
    image1_url = "https://github.com/frpeddis/TestApp1/blob/5aef3485bfa0d8a0ee51160aa2c6d8108aaf2bbb/MAGIC%20DAY%20CALCULATOR%20ADVENTURE%201.jpg"
    image2_url = "https://github.com/frpeddis/TestApp1/blob/cc5b547bc827972886fa017c0e8c93de399cbc64/MAGIC%20DAY%20CALCULATOR%20ADVENTURE%202.jpg"

    # Fetch the images from the URLs
    image1_response = requests.get(image1_url)
    image2_response = requests.get(image2_url)

    if image1_response.status_code == 200 and image2_response.status_code == 200:
        image1 = Image.open(BytesIO(image1_response.content))
        image2 = Image.open(BytesIO(image2_response.content))

        st.image(image1, caption="Image 1", use_column_width=True)
        st.image(image2, caption="Image 2", use_column_width=True)

        if st.checkbox("Expand for Details"):
            st.write("Details about the selected part will be displayed here.")

if _name_ == "_main_":
    main()

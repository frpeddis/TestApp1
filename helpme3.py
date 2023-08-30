import streamlit as st
from PIL import Image, ImageDraw
import easyocr
import numpy as np
import pandas as pd

# subtitle
st.markdown("## EasyOCRR with Streamlit")

# upload image file
file = st.file_uploader(label="Upload your image", type=['png', 'jpg', 'jpeg'])

if file is not None:  # check if a file is uploaded
    image = Image.open(file)  # read image with PIL library
    st.image(image, caption="Uploaded Image")  # display

    # it will only detect the English and Turkish part of the image as text
    reader = easyocr.Reader(['tr', 'en'], gpu=False)
    result = reader.readtext(np.array(image))  # turn image to numpy array

    textdic_easyocr = {}
    for idx in range(len(result)):
        pred_coor = result[idx][0]
        pred_text = result[idx][1]
        pred_confidence = result[idx][2]
        textdic_easyocr[pred_text] = {}
        textdic_easyocr[pred_text]['pred_confidence'] = pred_confidence

    # create a dataframe which shows the predicted text and prediction confidence
    df = pd.DataFrame.from_dict(textdic_easyocr, orient='index')
    st.table(df)

    def rectangle(image, result):
        """ draw rectangles on image based on predicted coordinates"""
        draw = ImageDraw.Draw(image)
        for res in result:
            top_left = tuple(res[0][0])  # top left coordinates as tuple
            bottom_right = tuple(res[0][2])  # bottom right coordinates as tuple
            draw.rectangle((top_left, bottom_right), outline="blue", width=2)
        # display image on streamlit
        st.image(image)

    rectangle(image, result)

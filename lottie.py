import json
import streamlit as st
from streamlit_lottie import st_lottie
  
path = "~/Download/animation.json"
with open(path,"r") as file:
    url = json.load(file)
  
  
  
st.title("Adding Lottie Animation in Streamlit WebApp")
  
st_lottie(url,
    reverse=True,
    height=400,
    width=400,
    speed=1,
    loop=True,
    quality='high',
    key='Car'
)

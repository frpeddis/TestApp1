
import streamlit as st
from streamlit.components.v1 import components

def main():
    st.title("Lottie Animation in Streamlit")

    # Load the Lottie JSON animation
    animation_json = open("animation.json", "r").read()

    # Display the Lottie animation
    components.html(animation_json, width=400, height=400)

if __name__ == "__main__":
    main()

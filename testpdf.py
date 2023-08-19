import base64
from pathlib import Path

import streamlit as st

pdf_path = Path("MAGIC DAY CALCULATOR ADVENTURE.pdf")
base64_pdf = base64.b64encode(pdf_path.read_bytes()).decode("utf-8")
pdf_display = f"""
    <iframe src="data:application/pdf;base64,{base64_pdf}" width="800px" height="2100px" type="application/pdf"></iframe>
"""
st.markdown(pdf_display, unsafe_allow_html=True)


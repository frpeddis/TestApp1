import streamlit as st
import pandas as pd
import numpy as np


def generate_table(rows, columns):
    table = np.random.randn(rows, columns)
    return table


def create_dataframe(rows, columns):
    df = pd.DataFrame(
        generate_table(rows, columns),
        columns=('info %d' % i for i in range(columns)))
    return df


st.title("FP First Application :sunglasses:")
st.header("My acc software")

data = create_dataframe(5, 5)
st.subheader("Data Table")
st.dataframe(data)
st.subheader("Data Line Chart")
st.line_chart(data)
st.subheader("Data Bar Chart")
st.bar_chart(data)

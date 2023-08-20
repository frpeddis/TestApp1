import streamlit as st

# Streamlit app title
st.title("Styled Table Example")

# Define a sample table data
table_data = {
    "A": [1, 2, 3],
    "B": [4, 5, 6],
    "C": [7, 8, 9]
}

# Define the row and column to highlight
highlight_row = 1
highlight_col = "B"

# Create a custom HTML table
st.write("<style>td.highlight {color: red; font-weight: bold;}</style>", unsafe_allow_html=True)
st.write("<table><tr><th></th>")
for col in table_data.keys():
    st.write(f"<th>{col}</th>")
st.write("</tr>")
for i, row in enumerate(table_data.values()):
    st.write("<tr>")
    st.write(f"<td>{i}</td>")
    for j, cell in enumerate(row):
        cell_class = "highlight" if i == highlight_row and list(table_data.keys())[j] == highlight_col else ""
        st.write(f"<td class='{cell_class}'>{cell}</td>")
    st.write("</tr>")
st.write("</table>")

DATA_URL = ('https://raw.githubusercontent.com/frpeddis/TestApp1/main/Invenzioni.csv')
@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)

    return data
df = load_data()

# show data on streamlit
st.write(df)

DATA_URL = ('https://raw.githubusercontent.com/frpeddis/TestApp1/main/Invenzioni.csv')
@st.cache
def load_data():
    data = pd.read_csv(DATA_URL)
    data['Date'] = pd.to_datetime(data['Date']).dt.strftime('%Y-%m-%d')
    return data
df = load_data()

# show data on streamlit
 st.write(df)

import streamlit as st
import pandas as pd
import requests
from io import StringIO
from streamlit_sortables import sort_items
import random
import time

# Set Streamlit page configuration
st.set_page_config(layout="wide")

# Function to load data from GitHub
def load_data(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            csv_raw = StringIO(response.text)
            # Attempt to read the CSV without skipping bad lines first to catch the error
            try:
                data = pd.read_csv(csv_raw)
                return data
            except pd.errors.ParserError as e:
                # Reset the StringIO object to read from the beginning
                csv_raw.seek(0)
                # Informative error logging
                for i, line in enumerate(csv_raw.readlines()):
                    try:
                        pd.read_csv(StringIO(line))
                    except pd.errors.ParserError:
                        print(f"Error in line {i+1}: {line.strip()}")
                        break
                # Optionally, return a DataFrame with error_bad_lines=False
                csv_raw.seek(0)
                return pd.read_csv(csv_raw, error_bad_lines=False)
        else:
            print(f"Failed to load data: HTTP {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

# URL of the CSV file
csv_url = 'https://raw.githubusercontent.com/frpeddis/TestApp1/main/events363.csv'

# Set background style
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('https://raw.githubusercontent.com/frpeddis/TestApp1/main/libro2.jpg');
        background-repeat: no-repeat;
        background-size: cover;
    }}
    .transparent-container {{
        background-color: transparent;
    }}
    .custom-box {{
        background-color: white;
        color: darkblue;
        padding: 10px;
        border: 2px solid darkblue;
        border-radius: 10px;
        margin: 4px 0;
    }}
    .custom-box:hover {{
        transform: translateY(-1px);  /* Lift effect on hover */
    }}
    .stButton > button {{
        background-color: white;  
        color: darkblue;
        border-radius: 24px;
        padding: 10px 20px;
        border: 2px solid darkblue;
        transition: background-color 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: darkblue;  /* Darker blue on hover */
        color: white;
        border: 2px white;
    }}
    </style>
    """, unsafe_allow_html=True)

# Initialize or reset the game
def reset_game(data):
    if not data.empty:
        st.session_state['start_time'] = time.time()
        st.session_state['selected_records'] = data.sample(5)
        st.session_state['hint_indices'] = list(range(5))
        st.session_state['game_over'] = False
        st.session_state['has_error'] = False
        st.experimental_rerun()
    else:
        st.error("No data available to start the game.")

# Load data
data = load_data(csv_url)

with st.container():
    st.markdown('<div class="transparent-container">', unsafe_allow_html=True)
    if 'start_time' not in st.session_state or data.empty:
        reset_game(data)

    if not data.empty:
        elapsed_time = int(time.time() - st.session_state['start_time'])

        if 'selected_records' not in st.session_state:
            reset_game(data)

        st.markdown("""
        <div class='custom-box'>
            <p><b><span style='font-size: 19px;'>Riordina le pagine del tuo libro di Storia!</span></b></p>
                👆 Trascina in alto i <span style='background-color: #ff4b4c; color: white; padding: 3px 6px; border-radius: 3px;'>segnalibri</span> più antichi, <P>👇 in basso i più recenti!</P>
        </div>
        """, unsafe_allow_html=True)

        items = [{'header': ' ', 'items': list(st.session_state['selected_records']['Descrizione Breve'])}]

        sorted_items = sort_items(items, multi_containers=True, direction="vertical")

        if st.button("🤞 Vai!"):
            ordered_records = pd.DataFrame()
            for desc in sorted_items[0]['items']:
                matching_record = st

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

# Load data
data = load_data(csv_url)
# URL of the CSV file on GitHub
csv_url = 'https://raw.githubusercontent.com/frpeddis/TestApp1/main/events363.csv'

# Enhance Custom Box Style
st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap');

    body {{
        font-family: 'Roboto', sans-serif;
    }}

    .custom-box {{
        background-color: #f3f4f6;  /* Light grey background */
        color: #333;  /* Darker text for better readability */
        padding: 15px;
        border: 1px solid #ccc;  /* Subtle border */
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);  /* Soft shadow for depth */
        margin: 15px 0;
        transition: transform 0.3s ease;  /* Smooth hover effect */
    }}

    .custom-box:hover {{
        transform: translateY(-5px);  /* Lift effect on hover */
    }}

    .stButton > button {{
        background-color: #4caf50;  /* Green background for buttons */
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        transition: background-color 0.3s ease;
    }}

    .stButton > button:hover {{
        background-color: #45a049;  /* Darker green on hover */
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
                matching_record = st.session_state['selected_records'][st.session_state['selected_records']['Descrizione Breve'] == desc]
                if not matching_record.empty:
                    ordered_records = pd.concat([ordered_records, matching_record])
                else:
                    st.error(f"L'elemento '{desc}' non trovato nei record selezionati.")
                    st.session_state['has_error'] = True

            ordered_correctly = ordered_records['Anno di Scoperta'].is_monotonic_increasing
            if ordered_correctly and len(ordered_records) == len(sorted_items[0]['items']):
                st.session_state['game_over'] = True
                st.session_state['has_error'] = False
                st.balloons()
                end_time = int(time.time() - st.session_state['start_time'])
                st.markdown("<div style='background-color: lightgreen; color: blue; padding: 14px; border: 2px solid dark blue; border-radius: 14px;'>"
                            f"Daje !!! L'ordine è corretto! 👏👏👏 <P>⌛Tempo totale: <strong> {end_time} </strong> secondi</div></P>", unsafe_allow_html=True)
                for _, row in ordered_records.iterrows():
                    st.markdown(f"<div class='custom-box'>"
                                f"<strong>{int(row['Anno di Scoperta'])} - {row['Descrizione Breve']} </strong> - {row['Nome Inventore']} - {row['Paese']} - {row['Descrizione Lunga']}</div>",
                                unsafe_allow_html=True)
            else:
                st.session_state['has_error'] = True
                st.error("Urca! Riprova dai!")

        # Show the hint button only if there's an error
        if st.session_state.get('has_error', False):
            if st.button("👋 Aiutino ?"):
                if st.session_state['hint_indices']:
                    hint_index = random.choice(st.session_state['hint_indices'])
                    st.session_state['hint_indices'].remove(hint_index)
                    hint_record = st.session_state['selected_records'].iloc[hint_index]
                    hint_text = f"<div class='custom-box'>{hint_record['Descrizione Breve']} {int(hint_record['Anno di Scoperta'])}</div>"
                    st.markdown(hint_text, unsafe_allow_html=True)
                else:
                    st.error("Non ci sono più suggerimenti disponibili.")

        if st.session_state.get('game_over') and st.button("🔄 Gioca di nuovo"):
            reset_game(data)

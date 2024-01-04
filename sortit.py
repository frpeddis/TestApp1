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
            try:
                data = pd.read_csv(csv_raw)
                return data
            except pd.errors.ParserError as e:
                csv_raw.seek(0)
                for i, line in enumerate(csv_raw.readlines()):
                    try:
                        pd.read_csv(StringIO(line))
                    except pd.errors.ParserError:
                        print(f"Error in line {i+1}: {line.strip()}")
                        break
                csv_raw.seek(0)
                return pd.read_csv(csv_raw, error_bad_lines=False)
        else:
            print(f"Failed to load data: HTTP {response.status_code}")
            return pd.DataFrame()
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
        return pd.DataFrame()

# Add CSS for correct order
st.markdown(f"""
    <style>
    .stApp {{
        background-image: url('https://raw.githubusercontent.com/frpeddis/TestApp1/main/libro2.jpg');
        background-repeat: no-repeat;
        background-size: cover;
    }}
    .custom-box, .correct-order {{
        color: darkblue;
        padding: 10px;
        border: 2px solid darkblue;
        border-radius: 18px;
        margin: 6px 0;
    }}
    .correct-order {{
        background-color: #28a745;  /* Green background */
        color: white;
    }}
    .custom-box:hover, .correct-order:hover {{
        transform: translateY(-5px);  /* Lift effect on hover */
    }}
    .stButton > button {{
        background-color: darkblue;
        color: white;
        border-radius: 5px;
        padding: 10px 20px;
        border: none;
        transition: background-color 0.3s ease;
    }}
    .stButton > button:hover {{
        background-color: blue;  /* Darker green on hover */
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

# URL of the CSV file
csv_url = 'https://raw.githubusercontent.com/frpeddis/TestApp1/main/events363.csv'

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
                    st.markdown(f"<div class='correct-order'>"
                                f"<strong>{int(row['Anno di Scoperta'])} - {row['Descrizione Breve']} </strong> - {row['Nome Inventore']} - {row['Paese']} - {row['Descrizione Lunga']}</div>",
                                unsafe_allow_html=True)
            else:
                st.session_state['has_error'] = True
                st.error("Urca! Riprova dai!")

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

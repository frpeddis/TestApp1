import streamlit as st
import pandas as pd
import requests
from io import StringIO
from streamlit_sortables import sort_items
import random
import time

# Configura il layout della pagina (questa deve essere la prima chiamata Streamlit)
st.set_page_config(layout="wide")

# Imposta lo sfondo e lo stile per il box personalizzato
st.markdown(f"""
    <style>
    .stApp {{
        #background-image: url('https://raw.githubusercontent.com/frpeddis/TestApp1/main/img42.jpeg');
        background-image: url('https://raw.githubusercontent.com/frpeddis/TestApp1/main/calendar.jpg');
        background-image: url('https://raw.githubusercontent.com/frpeddis/TestApp1/main/libro2.jpg');

        background-repeat: no-repeat;
        background-size: cover;
    }}
    .custom-box {{
        background-color: white;
        color: darkblue;
        padding: 10px;
        border: 2px solid darkblue;
        border-radius: 10px;
        margin: 10px 0;
    }}
    </style>
    """, unsafe_allow_html=True)

# Carica il file CSV da GitHub
@st.cache
def load_data(url):
    response = requests.get(url)
    csv_raw = StringIO(response.text)
    data = pd.read_csv(csv_raw)
    return data

# Inizializza o resetta il gioco
def reset_game():
    st.session_state['start_time'] = time.time()
    st.session_state['selected_records'] = data.sample(5)
    st.session_state['hint_indices'] = list(range(5))

# URL del file CSV su GitHub
csv_url = 'https://raw.githubusercontent.com/frpeddis/TestApp1/main/events363.csv'
data = load_data(csv_url)

# Crea un container per il contenuto dell'app
with st.container():
    # Titolo dell'applicazione
    #st.title('Riordina le pagine del libro di storia! 😎')

    if 'start_time' not in st.session_state:
        reset_game()

    # Mostra il tempo trascorso
    elapsed_time = int(time.time() - st.session_state['start_time'])

    # Se i dati sono sufficienti, seleziona 5 record casuali
    if not data.empty and len(data) >= 5:
        if 'selected_records' not in st.session_state:
            st.session_state['selected_records'] = data.sample(5)

        if 'hint_indices' not in st.session_state:
            st.session_state['hint_indices'] = list(range(5))

        # Mostra le invenzioni casuali
        st.markdown("<div class='custom-box'> <P><B>Riordina le pagine del tuo libro si Storia ! </B></P>👆 Trascina in alto i segnalibri più antichi, 👇 in basso i più recenti!</div>", unsafe_allow_html=True)
        
        items = [{'header': ' ', 'items': list(st.session_state['selected_records']['Descrizione Breve'])}]
        
        # Utilizza streamlit-sortables per ordinare gli elementi
        sorted_items = sort_items(items, multi_containers=True, direction="vertical")

        # Pulsante Hint
        if st.button("👋 Aiutino ?"):
            if st.session_state['hint_indices']:
                hint_index = random.choice(st.session_state['hint_indices'])
                st.session_state['hint_indices'].remove(hint_index)
                hint_record = st.session_state['selected_records'].iloc[hint_index]
                hint_text = f"<div class='custom-box'>{hint_record['Descrizione Breve']} {int(hint_record['Anno di Scoperta'])}</div>"
                st.markdown(hint_text, unsafe_allow_html=True)
            else:
                st.error("Non ci sono più suggerimenti disponibili.")

        # Verifica l'ordine
        if st.button("🤞 Vuoi provare ?"):
            ordered_records = pd.DataFrame()
            for desc in sorted_items[0]['items']:
                matching_record = st.session_state['selected_records'][st.session_state['selected_records']['Descrizione Breve'] == desc]
                if not matching_record.empty:
                    ordered_records = pd.concat([ordered_records, matching_record])
                else:
                    st.error(f"L'elemento '{desc}' non trovato nei record selezionati.")

            ordered_correctly = ordered_records['Anno di Scoperta'].is_monotonic_increasing
            if ordered_correctly and len(ordered_records) == len(sorted_items[0]['items']):
                st.balloons()
                end_time = int(time.time() - st.session_state['start_time'])
                st.markdown("<div style='background-color: lightgreen; color: blue; padding: 14px; border: 2px solid dark blue; border-radius: 14px;'>"
                            f"Daje !!! L'ordine è corretto! 👏👏👏 <P>⌛Tempo totale: <strong> {end_time} </strong> secondi</div></P>", unsafe_allow_html=True)
                for _, row in ordered_records.iterrows():
                    st.markdown(f"<div class='custom-box'>"
                                f"<strong>{int(row['Anno di Scoperta'])} - {row['Descrizione Breve']} </strong> - {row['Nome Inventore']} - {row['Paese']} - {row['Descrizione Lunga']}</div>",
                                unsafe_allow_html=True)
            else:
                
                st.error("Urca! L'ordine non è corretto. Riprova dai!")
                


    # Pulsante per giocare di nuovo
    if st.button("🔄 Gioca di nuovo"):
        reset_game()
        st.experimental_rerun()

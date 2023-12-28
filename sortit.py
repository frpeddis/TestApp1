import streamlit as st
import pandas as pd
import requests
from io import StringIO
from streamlit_sortables import sort_items
import random
import time

# Titolo dell'applicazione
st.title('Riordina gli eventi! 😎')

#  URL del file CSV su GitHub
csv_url = 'https://raw.githubusercontent.com/frpeddis/TestApp1/main/events39.csv'

# Carica il file CSV da GitHub
@st.cache
def load_data(url):
    response = requests.get(url)
    csv_raw = StringIO(response.text)
    data = pd.read_csv(csv_raw)
    return data

data = load_data(csv_url)

# Stile CSS personalizzato per i box con spigoli stondati
st.markdown("""
    <style>
    .custom-box {
        border: 2px solid blue;
        background-color: white;
        color: blue;
        padding: 10px;
        margin-bottom: 10px;
        border-radius: 14px; /* Spigoli stondati */
    }
    </style>
    """, unsafe_allow_html=True)

# Inizializza il timer
if 'start_time' not in st.session_state:
    st.session_state['start_time'] = time.time()

# Mostra il tempo trascorso
elapsed_time = int(time.time() - st.session_state['start_time'])
#st.write(f"Tempo trascorso: {elapsed_time} secondi")

# Se i dati sono sufficienti, seleziona 5 record casuali
if not data.empty and len(data) >= 5:
    if 'selected_records' not in st.session_state:
        st.session_state['selected_records'] = data.sample(5)

    if 'hint_indices' not in st.session_state:
        st.session_state['hint_indices'] = list(range(5))

    # Mostra le invenzioni casuali
    items = [{'header': '🔄 Trascina in alto i più antichi!', 'items': list(st.session_state['selected_records']['Descrizione Breve'])}]
    
    #st.markdown("<div style='background-color: White; color: darkblue; padding: 14px; border: 2px solid blue; border-radius: 14px;'>"
    #        "Metti in ordine questi eventi! 🗓️</div>", unsafe_allow_html=True)

    
    
    # Utilizza streamlit-sortables per ordinare gli elementi
    sorted_items = sort_items(items, multi_containers=True, direction="vertical")

    # Pulsante Hint
    if st.button("👋 Aiutino"):
        if st.session_state['hint_indices']:
            hint_index = random.choice(st.session_state['hint_indices'])
            st.session_state['hint_indices'].remove(hint_index)
            hint_record = st.session_state['selected_records'].iloc[hint_index]
            hint_text = f"<div class='custom-box'>{hint_record['Descrizione Breve']} {int(hint_record['Anno di Scoperta'])}</div>"
            st.markdown(hint_text, unsafe_allow_html=True)
        else:
            st.error("Non ci sono più suggerimenti disponibili.")

    # Verifica l'ordine
    if st.button("👉 Vuoi provare ?"):
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
            st.markdown("<div style='background-color: lightgreen; color: blue; padding: 14px; border: 6px solid white; border-radius: 14px;'>"
                        f"Daje !!! L'ordine è corretto! 👏👏👏 <P>⌛Tempo totale: <strong> {end_time} </strong> secondi</div></P>", unsafe_allow_html=True)
            for _, row in ordered_records.iterrows():
                st.markdown(f"<div class='custom-box'>"
                            f"<strong>{int(row['Anno di Scoperta'])} - {row['Descrizione Breve']} </strong> - {row['Nome Inventore']} - {row['Paese']} - {row['Descrizione Lunga']}</div>",
                            unsafe_allow_html=True)
            # Resetta il timer
            st.session_state['start_time'] = time.time()

        else:
            st.error("Urca, l'ordine non è corretto. Riprova.")

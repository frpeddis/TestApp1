import streamlit as st
import pandas as pd
import requests
from io import StringIO
from streamlit_sortables import sort_items
import random

# Titolo dell'applicazione
st.title('Ti ricordi ? 😎')

# Stile CSS globale per gli elementi di streamlit-sortables
st.markdown("""
    <style>
    .stSortable .st-sb-item {
        color: blue;
        background-color: white;
        border: 2px solid blue;
        padding: 5px;
        margin-bottom: 2px;
    }
    .custom-box {
        border: 2px solid blue;
        background-color: white;
        color: blue;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# URL del file CSV su GitHub
csv_url = 'https://raw.githubusercontent.com/frpeddis/TestApp1/main/events36.csv'

# Carica il file CSV da GitHub
@st.cache
def load_data(url):
    response = requests.get(url)
    csv_raw = StringIO(response.text)
    data = pd.read_csv(csv_raw)
    return data

data = load_data(csv_url)

# Se i dati sono sufficienti, seleziona 5 record casuali
if not data.empty and len(data) >= 5:
    if 'selected_records' not in st.session_state:
        st.session_state['selected_records'] = data.sample(5)

    if 'hint_indices' not in st.session_state:
        st.session_state['hint_indices'] = list(range(5))

    # Mostra le invenzioni casuali
    items = [{'header': 'In alto i più antichi!', 'items': list(st.session_state['selected_records']['Descrizione Breve'])}]
    st.write('Metti in ordine questi eventi!')

    # Utilizza streamlit-sortables per ordinare gli elementi
    sorted_items = sort_items(items, multi_containers=True, direction="vertical")

    # Pulsante Hint
    if st.button("🖐️ Hint"):
        if st.session_state['hint_indices']:
            hint_index = random.choice(st.session_state['hint_indices'])
            st.session_state['hint_indices'].remove(hint_index)
            hint_record = st.session_state['selected_records'].iloc[hint_index]
            hint_text = f"<div class='custom-box'><strong>{hint_record['Descrizione Breve']} {int(hint_record['Anno di Scoperta'])}</strong></div>"
            st.markdown(hint_text, unsafe_allow_html=True)
        else:
            st.error("Non ci sono più suggerimenti disponibili.")

    # Verifica l'ordine
    if st.button("👉 Ce l'hai fatta ?"):
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
            st.markdown("<div style='background-color: lightgreen; color: blue; padding: 14px; border: 2px solid white;'>"
                        "Daje !!! Hai indovinato l'ordine corretto!</div>", unsafe_allow_html=True)
            for _, row in ordered_records.iterrows():
                st.markdown(f"<div class='custom-box'><strong>{row['Descrizione Breve']} {int(row['Anno di Scoperta'])}</strong> - {row['Nome Inventore']} - {row['Paese']} - {row['Descrizione Lunga']}</div>",
                            unsafe_allow_html=True)
        else:
            st.error("Urca, l'ordine non è corretto. Riprova.")

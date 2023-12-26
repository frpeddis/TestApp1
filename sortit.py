import streamlit as st
import pandas as pd
import requests
from io import StringIO
from streamlit_sortables import sort_items

# Titolo dell'applicazione
st.title('Quanto sei forte ?')

# URL del file CSV su GitHub
csv_url = 'https://raw.githubusercontent.com/frpeddis/TestApp1/main/Invenzioni6.csv'

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

    # Mostra le invenzioni casuali
    #st.write('Metti in ordine queste invenzioni:')
    items = [{'header': 'Metti in ordine queste invenzioni', 'items': list(st.session_state['selected_records']['Descrizione Breve'])}]

    # Utilizza streamlit-sortables per ordinare gli elementi
    sorted_items = sort_items(items, multi_containers=True, direction="vertical")

    # Verifica l'ordine
    if st.button("Ce l'hai fatta ?"):
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
            st.markdown("<div style='background-color:blue;color:white;padding:14px;'>"
                        "Daje !!! Hai indovinato l'ordine corretto!</div>", unsafe_allow_html=True)
            for _, row in ordered_records.iterrows():
                st.markdown(f"<div style='background-color:darkblue;color:white;padding:12px;'>"
                            f"{row['Descrizione Breve']} - {row['Anno di Scoperta']} - {row['Nome Inventore']} - {row['Paese']} - {row['Descrizione Lunga']}</div>",
                            unsafe_allow_html=True)
        else:
            st.error("Mannaggia, l'ordine non è corretto. Riprova.")


import streamlit as st
import pandas as pd
from streamlit_sortables import sort_items

# Titolo dell'applicazione
st.title('Scoperte Invenzioni')

# Carica il file CSV
uploaded_file = st.file_uploader("Carica un file CSV", type="csv")
if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    # Stampare i nomi delle colonne per il debugging
    st.write('Nomi delle colonne nel file CSV:', data.columns.tolist())
else:
    st.info("Attendi il caricamento del file CSV.")
    data = pd.DataFrame()

# Se i dati sono sufficienti, seleziona 5 record casuali
if not data.empty and len(data) >= 5:
    if 'selected_records' not in st.session_state:
        st.session_state['selected_records'] = data.sample(5)

    # Mostra le invenzioni casuali
    st.write('Invenzioni Casuali:')
    items = [{'header': 'Invenzioni', 'items': list(st.session_state['selected_records']['Descrizione Breve'])}]

    # Utilizza streamlit-sortables per ordinare gli elementi
    sorted_items = sort_items(items, multi_containers=True, direction="vertical")

    # Verifica l'ordine
    if st.button("Verifica Ordine"):
        ordered_records = pd.DataFrame()
        for desc in sorted_items[0]['items']:
            matching_record = st.session_state['selected_records'][st.session_state['selected_records']['Descrizione Breve'] == desc]
            if not matching_record.empty:
                ordered_records = pd.concat([ordered_records, matching_record], ignore_index=True)
            else:
                st.error(f"L'elemento '{desc}' non trovato nei record selezionati.")

        # Verifica se l'ordine degli anni di scoperta è crescente
        ordered_correctly = ordered_records['Anno di Scoperta'].is_monotonic_increasing
        if ordered_correctly and len(ordered_records) == len(sorted_items[0]['items']):
            # Imposta lo stile per il messaggio di successo
            st.markdown("<style>.green-background { background-color: lightgreen; padding: 10px; border-radius: 5px; }</style>", unsafe_allow_html=True)
            # Mostra il messaggio di successo e i dettagli in verde
            for _, row in ordered_records.iterrows():
                st.markdown(f"<div class='green-background'>"
                            f"{row['Descrizione Breve']} - {row['Anno di Scoperta']} - "
                            f"{row['Descrizione Lunga']} - {row['Nome Inventore']} - "
                            f"{row['Paese di Origine']}</div>", unsafe_allow_html=True)
            st.success("Hai indovinato l'ordine corretto!")
        else:
            st.error("Ordine non corretto. Riprova.")

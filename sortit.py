import streamlit as st
import pandas as pd

# Layout Streamlit
st.title("Scoperte Invenzioni")

# Carica il file CSV tramite drag-and-drop
uploaded_file = st.file_uploader("Carica un file CSV", type="csv")
if uploaded_file is not None:
    try:
        # Leggi il file CSV caricato
        data = pd.read_csv(uploaded_file)
    except Exception as e:
        st.error(f"Errore nella lettura del file: {e}")
        data = pd.DataFrame()
else:
    st.info("Attendi il caricamento del file CSV.")
    data = pd.DataFrame()

# Verifica se i dati sono sufficienti
if data.empty:
    st.error("Il DataFrame è vuoto.")
elif len(data) < 5:
    st.error("Non ci sono abbastanza dati per selezionare 5 record casuali.")
else:
    # Seleziona 5 record casuali, solo se non sono già stati selezionati
    if 'selected_records' not in st.session_state:
        st.session_state['selected_records'] = data.sample(5)
        st.session_state['ordered_names'] = []

    # Container 1: Descrizione Sintetica
    with st.container():
        st.subheader("Descrizioni Sintetiche")
        for _, row in st.session_state['selected_records'].iterrows():
            st.write(f"- {row['Descrizione Breve']}")

    # Container 2: Ordinamento Eventi
    with st.container():
        st.subheader("Ordina gli Eventi per Data")

        # Selezione degli eventi da ordinare
        all_names = [row['Descrizione Breve'] for _, row in st.session_state['selected_records'].iterrows()]
        selected_name = st.selectbox("Scegli un evento da aggiungere all'ordine:", all_names)
        if st.button("Aggiungi all'Ordine"):
            if selected_name not in st.session_state['ordered_names']:
                st.session_state['ordered_names'].append(selected_name)

        # Mostra gli eventi selezionati in ordine
        for name in st.session_state['ordered_names']:
            st.write(name)

        # Controlla l'ordine
        if st.button("Verifica Ordine"):
            ordered_records = pd.DataFrame()
            for name in st.session_state['ordered_names']:
                ordered_records = ordered_records.append(st.session_state['selected_records'][st.session_state['selected_records']['Descrizione Breve'] == name])

            ordered_correctly = ordered_records['anno della scoperta'].is_monotonic_increasing
            if ordered_correctly and len(ordered_records) == len(st.session_state['ordered_names']):
                st.success("Hai indovinato l'ordine corretto!")
                for _, row in ordered_records.iterrows():
                    st.write(f"{row['Descrizione Breve']} - {row['anno della scoperta']}")
            else:
                st.error("Ordine non corretto. Riprova.")

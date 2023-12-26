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
        st.session_state['data'] = data  # Memorizza i dati nella sessione
    except Exception as e:
        st.error(f"Errore nella lettura del file: {e}")
        st.session_state['data'] = pd.DataFrame()
else:
    st.info("Attendi il caricamento del file CSV.")
    st.session_state['data'] = pd.DataFrame()

# Verifica se i dati sono sufficienti
if st.session_state.get('data', pd.DataFrame()).empty:
    st.error("Il DataFrame è vuoto.")
elif len(st.session_state['data']) < 5:
    st.error("Non ci sono abbastanza dati per selezionare 5 record casuali.")
else:
    # Seleziona 5 record casuali, solo se non sono già stati selezionati
    if 'selected_records' not in st.session_state:
        st.session_state['selected_records'] = st.session_state['data'].sample(5)

    # Container 1: Descrizione Sintetica
    with st.container():
        st.subheader("Descrizioni Sintetiche")
        for _, row in st.session_state['selected_records'].iterrows():
            st.write(f"- {row['Descrizione Breve']}")

    # Container 2: Ordinamento Eventi
    with st.container():
        st.subheader("Ordina gli Eventi per Data")
        ordered_names = [row['Descrizione Breve'] for _, row in st.session_state['selected_records'].iterrows()]
        
        # Implementazione di riordinamento
        item_to_move = st.selectbox("Seleziona un evento da spostare:", ordered_names)
        new_position = st.selectbox("Scegli la nuova posizione:", range(len(ordered_names)))
        
        if st.button("Conferma Spostamento"):
            # Sposta l'elemento nella nuova posizione
            ordered_names.remove(item_to_move)
            ordered_names.insert(new_position, item_to_move)
            st.session_state['selected_records'] = st.session_state['selected_records'].loc[st.session_state['selected_records']['Descrizione Breve'].isin(ordered_names)]

        # Controlla l'ordine
        if st.button("Verifica Ordine"):
            ordered_records = pd.DataFrame()
            for name in ordered_names:
                ordered_records = ordered_records.append(st.session_state['selected_records'][st.session_state['selected_records']['Descrizione Breve'] == name])

            ordered_correctly = ordered_records['anno della scoperta'].is_monotonic_increasing
            if ordered_correctly and len(ordered_records) == 5:
                st.success("Hai indovinato l'ordine corretto!")
                for _, row in ordered_records.iterrows():
                    st.write(f"{row['Descrizione Breve']} - {row['anno della scoperta']} - {row['descrizione estesa']} - {row['Nome inventore']} - {row['Paese di origine']}")
            else:
                st.error("Ordine non corretto. Riprova.")

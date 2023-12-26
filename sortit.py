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
# Layout Streamlit
st.title("Scoperte Invenzioni")

# Verifica se i dati sono sufficienti
if data.empty:
    st.error("Il DataFrame è vuoto.")
elif len(data) < 5:
    st.error("Non ci sono abbastanza dati per selezionare 5 record casuali.")
else:
    # Seleziona 5 record casuali
    selected_records = data.sample(5)

    # Container 1: Descrizione Sintetica
    with st.container():
        st.subheader("Descrizioni Sintetiche")
        for _, row in selected_records.iterrows():
            st.write(f"- {row['nome sintetico di invenzione']}")

    # Container 2: Ordinamento Eventi
    with st.container():
        st.subheader("Ordina gli Eventi per Data")
        ordered_names = [row['nome sintetico di invenzione'] for _, row in selected_records.iterrows()]
        ordered_names = st.multiselect("Riordina gli eventi qui:", ordered_names, ordered_names)

        # Controlla l'ordine
        if st.button("Verifica Ordine"):
            ordered_records = pd.DataFrame()
            for name in ordered_names:
                ordered_records = ordered_records.append(selected_records[selected_records['nome sintetico di invenzione'] == name])

            ordered_correctly = ordered_records['anno della scoperta'].is_monotonic_increasing
            if ordered_correctly and len(ordered_records) == 5:
                st.success("Hai indovinato l'ordine corretto!")
                for _, row in ordered_records.iterrows():
                    st.write(f"{row['nome sintetico di invenzione']} - {row['anno della scoperta']} - {row['descrizione estesa']} - {row['Nome inventore']} - {row['Paese di origine']}")
            else:
                st.error("Ordine non corretto. Riprova.")

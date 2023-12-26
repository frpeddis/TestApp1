
import streamlit as st
import pandas as pd
import random
import requests

# Funzione per caricare i dati da GitHub
@st.cache
def load_data_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        data = pd.read_csv(url)
        return data
    else:
        st.error("Impossibile caricare i dati dal repository GitHub.")
        return pd.DataFrame()

# URL del file CSV su GitHub (assicurati che sia il raw URL)
csv_url = 'https://raw.githubusercontent.com/your_username/TestApp1/main/Invenzioni.csv'
data = load_data_from_github(csv_url)


# Verifica se i dati sono sufficienti
if data.empty or len(data) < 5:
    st.error("I dati non sono sufficienti per la selezione casuale.")
else:
    # Seleziona 5 record casuali
    selected_records = data.sample(5)

    # Layout Streamlit
    st.title("Scoperte Invenzioni")

    # Container 1: Descrizione Sintetica
    with st.container():
        st.subheader("Descrizioni Sintetiche")
        for _, row in selected_records.iterrows():
            st.write(f"- {row['nome sintetico di invenzione']}")

    # Container 2: Ordinamento Eventi
    with st.container():
        st.subheader("Ordina gli Eventi per Data")

        # Crea una lista modificabile di nomi
        ordered_names = [row['nome sintetico di invenzione'] for _, row in selected_records.iterrows()]
        ordered_names = st.multiselect("Riordina gli eventi qui:", ordered_names, ordered_names)

        # Controlla l'ordine
        if st.button("Verifica Ordine"):
            # Estrai i record nell'ordine selezionato
            ordered_records = pd.DataFrame()
            for name in ordered_names:
                ordered_records = ordered_records.append(selected_records[selected_records['nome sintetico di invenzione'] == name])

            # Verifica se l'ordine per anno è corretto
            ordered_correctly = ordered_records['anno della scoperta'].is_monotonic_increasing

            if ordered_correctly and len(ordered_records) == 5:
                st.success("Hai indovinato l'ordine corretto!")
                # Mostra dettagli aggiuntivi
                for _, row in ordered_records.iterrows():
                    st.write(f"{row['nome sintetico di invenzione']} - {row['anno della scoperta']} - {row['descrizione estesa']} - {row['Nome inventore']} - {row['Paese di origine']}")
            else:
                st.error("Ordine non corretto. Riprova.")

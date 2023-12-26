import streamlit as st
import pandas as pd
import requests

# Funzione per caricare i dati da GitHub
@st.cache
def load_data_from_github(url):
    response = requests.get(url)
    if response.status_code == 200:
        # Opzionale: stampa le prime righe del file per il debugging
        print(response.text[:500])  # Stampa i primi 500 caratteri del file
        return pd.read_csv(url)  # Legge il file CSV
    else:
        st.error("Impossibile caricare i dati dal repository GitHub.")
        return pd.DataFrame()

# URL del file CSV su GitHub (assicurati che sia il raw URL)
csv_url = 'https://raw.githubusercontent.com/frpeddis/TestApp1/main/Invenzioni.csv'
data = load_data_from_github(csv_url)

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

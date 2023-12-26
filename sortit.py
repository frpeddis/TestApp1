import streamlit as st
import pandas as pd
import random
import requests
from streamlit_lottie import st_lottie

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

# Seleziona 5 record casuali
selected_records = data.sample(5)

# Funzione per caricare un'animazione Lottie
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# Suono di vittoria (modifica con un URL appropriato per un'animazione Lottie)
victory_sound = load_lottieurl('your_lottie_sound_animation_url')

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
    ordered_names = st.columns(5)
    for i, name in enumerate(selected_records['nome sintetico di invenzione']):
        ordered_names[i].write(name)

# Controlla l'ordine
if st.button("Verifica Ordine"):
    ordered_correctly = True # Aggiungi la logica di controllo qui
    if ordered_correctly:
        st.success("Hai indovinato l'ordine corretto!")
        st_lottie(victory_sound, height=300, key="win")
        # Mostra dettagli aggiuntivi
        for _, row in selected_records.iterrows():
            st.write(f"{row['nome sintetico di invenzione']} - {row['anno della scoperta']} - {row['descrizione estesa']} - {row['Nome inventore']} - {row['Paese di origine']}")
    else:
        st.error("Ordine non corretto. Riprova.")

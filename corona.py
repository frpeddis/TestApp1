import streamlit as st
import plotly.graph_objects as go

# Funzione per creare il grafico a torta
def create_pie_chart(selected_day):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    colors = ['blue' if day == selected_day else 'lightgray' for day in days]

    fig = go.Figure(data=[go.Pie(labels=days, values=[1]*7, marker=dict(colors=colors), hole=.3)])
    fig.update_traces(textinfo='label', textfont_size=20)
    fig.update_layout(showlegend=False)

    return fig

# Inizializzazione della variabile selezionata
selected_day = None

# Streamlit UI
st.title('Weekday Selector')

# Visualizzazione del grafico a torta
fig = create_pie_chart(selected_day)
pie_chart = st.plotly_chart(fig, use_container_width=True)

# Gestione del clic sul grafico
@st.cache(allow_output_mutation=True)
def get_click_data():
    return {'day': None}

click_data = get_click_data()

# Rilevamento clic e aggiornamento grafico
clicked = pie_chart.clicked_points
if clicked:
    # Assicurati che ci sia almeno un elemento in 'clicked' e che contenga 'label'
    if len(clicked) > 0 and 'label' in clicked[0]:
        selected_day = clicked[0]['label']
        click_data['day'] = selected_day
        fig = create_pie_chart(selected_day)
        pie_chart.plotly_chart(fig, use_container_width=True)

# Visualizzazione del giorno selezionato
if click_data['day']:
    st.write(f"You selected: {click_data['day']}")

import streamlit as st
import plotly.graph_objects as go

# Function to create the pie chart
def create_pie_chart(selected_day):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    colors = ['blue' if day == selected_day else 'lightgray' for day in days]

    fig = go.Figure(data=[go.Pie(labels=days, values=[1]*7, marker=dict(colors=colors), hole=.3)])
    fig.update_traces(textinfo='label', textfont_size=20)
    fig.update_layout(showlegend=False)

    return fig

# Streamlit UI for selecting a day
st.title('Weekday Selector')

# Creating a row of buttons
col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
selected_day = None

with col1:
    if st.button(days[0]):
        selected_day = days[0]
with col2:
    if st.button(days[1]):
        selected_day = days[1]
with col3:
    if st.button(days[2]):
        selected_day = days[2]
with col4:
    if st.button(days[3]):
        selected_day = days[3]
with col5:
    if st.button(days[4]):
        selected_day = days[4]
with col6:
    if st.button(days[5]):
        selected_day = days[5]
with col7:
    if st.button(days[6]):
        selected_day = days[6]

# Display the pie chart
fig = create_pie_chart(selected_day)
st.plotly_chart(fig, use_container_width=True)

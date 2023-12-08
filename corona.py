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

# Streamlit UI
st.title('Weekday Selector')
selected_day = None

# Buttons for each day
for day in ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']:
    if st.button(day):
        selected_day = day

# Display the pie chart
fig = create_pie_chart(selected_day)
st.plotly_chart(fig, use_container_width=True)

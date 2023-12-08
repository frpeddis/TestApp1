import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

def draw_circle_sector(ax, center, radius, angle_start, angle_end, color='lightgray', label=''):
    angles = np.linspace(angle_start, angle_end, 100)
    x_full = np.concatenate([[center[0]], center[0] + radius * np.cos(np.radians(angles)), [center[0]]])
    y_full = np.concatenate([[center[1]], center[1] + radius * np.sin(np.radians(angles)), [center[1]]])
    ax.fill(x_full, y_full, color=color)
    ax.plot(x_full, y_full, color='black')
    ax.text(center[0] + (radius / 2) * np.cos(np.radians((angle_start + angle_end) / 2)),
            center[1] + (radius / 2) * np.sin(np.radians((angle_start + angle_end) / 2)),
            label, ha='center', va='center')

def draw_week_circle(ax, center, radius, selected_day=None):
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    angle_per_day = 360 / len(days)

    for i, day in enumerate(days):
        start_angle = 360 - (i + 1) * angle_per_day
        end_angle = 360 - i * angle_per_day
        color = 'blue' if day == selected_day else 'lightgray'
        draw_circle_sector(ax, center, radius, start_angle, end_angle, color=color, label=day)

# Streamlit UI
st.title('Weekday Selector')
selected_day = st.selectbox('Select a day', ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

# Plotting the circle with the selected day highlighted
fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.axis('off')
draw_week_circle(ax, center=(0, 0), radius=5, selected_day=selected_day)
st.pyplot(fig)

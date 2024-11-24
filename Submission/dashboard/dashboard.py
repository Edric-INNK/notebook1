import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets using the correct relative paths
day_data = pd.read_csv('./day.csv')  # Correct relative path
hour_data = pd.read_csv('./hour.csv')  # Correct relative path

# Sidebar options
data_option = st.sidebar.selectbox('Choose Dataset:', ['Daily Data', 'Hourly Data'])

# Load appropriate dataset based on user selection
if data_option == 'Daily Data':
    data = day_data
    st.title('Daily Bike Sharing Data')
else:
    data = hour_data
    st.title('Hourly Bike Sharing Data')

# Filter options based on season
season = st.sidebar.selectbox('Select Season:', [1, 2, 3, 4], format_func=lambda x: ['Spring', 'Summer', 'Fall', 'Winter'][x - 1])
filtered_data = data[data['season'] == season]

# Visualization based on dataset type
st.write(f'Data for Season: {["Spring", "Summer", "Fall", "Winter"][season - 1]}')
if data_option == 'Daily Data':
    st.bar_chart(filtered_data.groupby('mnth')['cnt'].sum())
else:
    st.line_chart(filtered_data.groupby('hr')['cnt'].mean())

# Additional data insights
st.write('Basic Statistics:')
st.write(filtered_data.describe())

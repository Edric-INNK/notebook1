import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load datasets using the correct relative paths
day_data = pd.read_csv('./data/day.csv')  # Correct path to data folder
hour_data = pd.read_csv('./data/hour.csv')  # Correct path to data folder

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

# Filter options based on weather condition
weather = st.sidebar.selectbox(
    'Select Weather Condition:', 
    [1, 2, 3, 4], 
    format_func=lambda x: [
        'Clear/Few Clouds', 
        'Mist/Cloudy', 
        'Light Rain/Snow', 
        'Heavy Rain/Snow'
    ][x - 1]
)
filtered_data = filtered_data[filtered_data['weathersit'] == weather]

# Display data based on filters
st.write(f'Data for Season: {["Spring", "Summer", "Fall", "Winter"][season - 1]} and Weather: {["Clear", "Mist/Cloudy", "Light Rain/Snow", "Heavy Rain/Snow"][weather - 1]}')

# Visualization for Daily Data
if data_option == 'Daily Data':
    st.write('Monthly Bike Rentals (Bar Chart):')
    monthly_rentals = filtered_data.groupby('mnth')['cnt'].sum()
    fig, ax = plt.subplots()
    monthly_rentals.plot(kind='bar', ax=ax, color='orange')
    ax.set_title('Total Bike Rentals per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Rentals')
    ax.set_xticks(range(len(monthly_rentals.index)))
    ax.set_xticklabels(monthly_rentals.index, rotation=45)  # Rotate labels
    st.pyplot(fig)

# Visualization for Hourly Data
else:
    st.write('Average Hourly Rentals (Line Chart):')
    hourly_rentals = filtered_data.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots()
    hourly_rentals.plot(kind='line', ax=ax, color='blue')
    ax.set_title('Average Rentals per Hour')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Average Rentals')
    ax.set_xticks(range(len(hourly_rentals.index)))
    ax.set_xticklabels(hourly_rentals.index, rotation=45)  # Rotate labels
    st.pyplot(fig)

# Additional data insights
st.write('Basic Statistics:')
st.write(filtered_data.describe())

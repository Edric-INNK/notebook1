import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
st.write(f"**Data for Season: {['Spring', 'Summer', 'Fall', 'Winter'][season - 1]}**")
st.write(f"**Weather Condition: {['Clear/Few Clouds', 'Mist/Cloudy', 'Light Rain/Snow', 'Heavy Rain/Snow'][weather - 1]}**")

# Visualization for Daily Data
if data_option == 'Daily Data':
    st.write("**Monthly Rentals by Season and Weather:**")
    monthly_rentals = filtered_data.groupby('mnth')['cnt'].sum()
    fig, ax = plt.subplots()
    monthly_rentals.plot(kind='bar', ax=ax, color='orange')
    ax.set_title('Total Bike Rentals per Month')
    ax.set_xlabel('Month')
    ax.set_ylabel('Total Rentals')
    ax.set_xticks(range(len(monthly_rentals.index)))
    ax.set_xticklabels(monthly_rentals.index, rotation=45)  # Rotate labels
    st.pyplot(fig)

    # Scatter plot: Rentals vs. Temperature
    st.write("**Rentals vs. Temperature (Daily Data):**")
    fig, ax = plt.subplots()
    sns.scatterplot(x='temp', y='cnt', hue='season', data=filtered_data, palette='viridis', ax=ax)
    ax.set_title("Temperature vs. Rentals by Season")
    ax.set_xlabel("Normalized Temperature")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

# Visualization for Hourly Data
else:
    st.write("**Average Hourly Rentals by Season and Weather:**")
    hourly_rentals = filtered_data.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots()
    hourly_rentals.plot(kind='line', ax=ax, color='blue')
    ax.set_title('Average Rentals per Hour')
    ax.set_xlabel('Hour')
    ax.set_ylabel('Average Rentals')
    ax.set_xticks(range(len(hourly_rentals.index)))
    ax.set_xticklabels(hourly_rentals.index, rotation=45)  # Rotate labels
    st.pyplot(fig)

    # Scatter plot: Rentals vs. Humidity
    st.write("**Rentals vs. Humidity (Hourly Data):**")
    fig, ax = plt.subplots()
    sns.scatterplot(x='hum', y='cnt', hue='season', data=filtered_data, palette='coolwarm', ax=ax)
    ax.set_title("Humidity vs. Rentals by Season")
    ax.set_xlabel("Humidity")
    ax.set_ylabel("Total Rentals")
    st.pyplot(fig)

# Heatmap for Feature Correlation (Daily Data Only)
if data_option == 'Daily Data':
    st.write("**Correlation Heatmap for Numerical Features:**")
    corr = filtered_data[['temp', 'atemp', 'hum', 'windspeed', 'cnt']].corr()
    fig, ax = plt.subplots()
    sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)
    ax.set_title("Feature Correlation Heatmap")
    st.pyplot(fig)

# Additional data insights
st.write("**Basic Statistics for Filtered Data:**")
st.write(filtered_data.describe())

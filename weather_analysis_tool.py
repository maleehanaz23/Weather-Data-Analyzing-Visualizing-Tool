import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Step 1: Load and clean data
def load_data(file_path):
    weather_data = pd.read_csv(file_path)
    weather_data.fillna(0, inplace=True)  # Replace missing values with 0
    return weather_data

# Step 2: Data Cleaning - Convert Date to datetime and set it as index
def clean_data(weather_data):
    weather_data['Date'] = pd.to_datetime(weather_data['Date'], errors='coerce')
    weather_data.set_index('Date', inplace=True)
    return weather_data

# Step 3: Calculate Daily Average
def calculate_daily_average(weather_data):
    daily_avg = weather_data.groupby('Date')['Temperature'].mean()
    return daily_avg

# Step 4: Calculate Monthly Averages
def calculate_monthly_averages(weather_data):
    numeric_data = weather_data.select_dtypes(include=[np.number])
    monthly_averages = numeric_data.resample('M').mean()
    return monthly_averages

# Step 5: Calculate Yearly Averages
def calculate_yearly_averages(weather_data):
    numeric_data = weather_data.select_dtypes(include=[np.number])
    yearly_averages = numeric_data.resample('Y').mean()
    return yearly_averages

# Step 6: Aggregate data by Location
def aggregate_by_location(weather_data):
    location_stats = weather_data.groupby('Location').agg({
        'Temperature': ['min', 'max', 'mean'],
        'Precipitation': ['min', 'max', 'mean'],
        'Humidity': ['min', 'max', 'mean'],
        'Wind Speed': ['min', 'max', 'mean']
    })
    return location_stats

# Plotting functions
def plot_temperature_trends(weather_data):
    plt.figure(figsize=(12, 6))
    sns.lineplot(data=weather_data, x=weather_data.index, y='Temperature')
    plt.title('Temperature Trends Over Time')
    plt.xlabel('Date')
    plt.ylabel('Temperature (°C)')
    st.pyplot(plt)

def plot_temperature_distribution(weather_data):
    plt.figure(figsize=(10, 6))
    weather_data['Temperature'].hist(bins=20)
    plt.title('Temperature Distribution')
    plt.xlabel('Temperature (°C)')
    plt.ylabel('Frequency')
    st.pyplot(plt)

def plot_temperature_by_location(weather_data):
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=weather_data, x='Location', y='Temperature')
    plt.title('Temperature Variations by Location')
    plt.xlabel('Location')
    plt.ylabel('Temperature (°C)')
    plt.xticks(rotation=90)
    st.pyplot(plt)

def plot_weather_conditions(weather_data):
    condition_counts = weather_data['Conditions'].value_counts()
    plt.figure(figsize=(8, 8))
    condition_counts.plot.pie(autopct='%1.1f%%')
    plt.title('Weather Conditions Distribution')
    plt.ylabel('')
    st.pyplot(plt)

def plot_monthly_avg_temperature(monthly_averages):
    plt.figure(figsize=(12, 6))
    monthly_averages['Temperature'].plot(kind='area', alpha=0.4)
    plt.title('Monthly Average Temperature')
    plt.xlabel('Month')
    plt.ylabel('Temperature (°C)')
    st.pyplot(plt)

def plot_wind_speed_vs_temperature(weather_data):
    g = sns.FacetGrid(weather_data, col="Location", hue="Conditions", col_wrap=2, height=4, aspect=1.2)
    g.map(sns.scatterplot, "Wind Speed", "Temperature", alpha=.7)
    g.add_legend()
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle('Wind Speed vs Temperature by Location and Condition')
    st.pyplot(g.fig)

def plot_facet_grid_temperature(weather_data):
    weather_data_reset = weather_data.reset_index()
    g = sns.FacetGrid(weather_data_reset, col="Location", col_wrap=2, height=4, aspect=1.5)
    g.map(sns.lineplot, "Date", "Temperature")
    g.set_axis_labels("Date", "Temperature (°C)")
    plt.subplots_adjust(top=0.9)
    g.fig.suptitle('Temperature Trends Over Time by Location')
    st.pyplot(g.fig)

# Streamlit interface
def main():
    st.title("Weather Data  Analysis Tool")
    
    # Step 1: Load the data
    file_path = st.text_input("Enter file path for the weather data CSV", "F:/New folder/weather_data_with_location_2023(2).csv")
    if st.button("Load Data") or 'weather_data' in st.session_state:
        if "weather_data" not in st.session_state:
            weather_data = load_data(file_path)
            weather_data = clean_data(weather_data)
            st.session_state.weather_data = weather_data
            st.success("Data loaded successfully!")
        else:
            weather_data = st.session_state.weather_data
        st.write(weather_data.head(10))
    
        # Sidebar for options
        st.sidebar.title("Options")
        choice = st.sidebar.selectbox("Select an analysis option:", [
            "Calculate Daily Average",
            "Calculate Monthly Averages",
            "Calculate Yearly Averages",
            "Aggregate Data by Location",
            "Plot Temperature Trends Over Time",
            "Plot Temperature Distribution",
            "Plot Temperature by Location",
            "Plot Weather Conditions Distribution",
            "Plot Monthly Average Temperature",
            "Plot Wind Speed vs Temperature",
            "Plot Temperature Trends by Location (FacetGrid)"
        ])
        
        # Display results based on choice
        if choice == "Calculate Daily Average":
            daily_avg = calculate_daily_average(weather_data)
            st.write("**Daily Average Temperature:**")
            st.write(daily_avg)

        elif choice == "Calculate Monthly Averages":
            monthly_averages = calculate_monthly_averages(weather_data)
            st.write("**Monthly Averages:**")
            st.write(monthly_averages)

        elif choice == "Calculate Yearly Averages":
            yearly_averages = calculate_yearly_averages(weather_data)
            st.write("**Yearly Averages:**")
            st.write(yearly_averages)

        elif choice == "Aggregate Data by Location":
            location_stats = aggregate_by_location(weather_data)
            st.write("**Aggregate Data by Location:**")
            st.write(location_stats)

        elif choice == "Plot Temperature Trends Over Time":
            st.write("**Temperature Trends Over Time:**")
            plot_temperature_trends(weather_data)

        elif choice == "Plot Temperature Distribution":
            st.write("**Temperature Distribution:**")
            plot_temperature_distribution(weather_data)

        elif choice == "Plot Temperature by Location":
            st.write("**Temperature by Location:**")
            plot_temperature_by_location(weather_data)

        elif choice == "Plot Weather Conditions Distribution":
            st.write("**Weather Conditions Distribution:**")
            plot_weather_conditions(weather_data)

        elif choice == "Plot Monthly Average Temperature":
            st.write("**Monthly Average Temperature:**")
            monthly_averages = calculate_monthly_averages(weather_data)
            plot_monthly_avg_temperature(monthly_averages)

        elif choice == "Plot Wind Speed vs Temperature":
            st.write("**Wind Speed vs Temperature by Location and Condition:**")
            plot_wind_speed_vs_temperature(weather_data)

        elif choice == "Plot Temperature Trends by Location (FacetGrid)":
            st.write("**Temperature Trends by Location (FacetGrid):**")
            plot_facet_grid_temperature(weather_data)

if __name__ == "__main__":
    main()

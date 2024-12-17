import streamlit as st
import requests
from datetime import datetime


# OpenWeatherMap API key
API_KEY = 'a14ceacd0266018467616e80f1003594'  # Your actual API key

def get_weather_data(city):
    """
    Fetch current weather data for a given city
    """
    try:
        # Prepare request parameters
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # Use metric units (Celsius)
        }
        # Send the request to OpenWeatherMap's weather endpoint
        response = requests.get('https://api.openweathermap.org/data/2.5/weather', params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching weather data: {e}")
        return None

def get_forecast_data(city):
    """
    Fetch 5-day forecast for a given city
    """
    try:
        # Prepare request parameters
        params = {
            'q': city,
            'appid': API_KEY,
            'units': 'metric'  # Use metric units (Celsius)
        }
        # Send the request to OpenWeatherMap's forecast endpoint
        response = requests.get('https://api.openweathermap.org/data/2.5/forecast', params=params)
        response.raise_for_status()  # Raise an exception for bad responses
        return response.json()
    except requests.RequestException as e:
        st.error(f"Error fetching forecast data: {e}")
        return None

def display_current_weather(weather_data):
    """
    Display current weather information
    """
    if not weather_data:
        return

    col1, col2 = st.columns(2)

    with col1:
        st.write(f"**Temperature:** {weather_data['main']['temp']}°C")
        st.write(f"**Feels Like:** {weather_data['main']['feels_like']}°C")
        st.write(f"**Humidity:** {weather_data['main']['humidity']}%")

    with col2:
        # Get weather icon
        icon_code = weather_data['weather'][0]['icon']
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        st.image(icon_url, width=100)

        st.write(f"**Conditions:** {weather_data['weather'][0]['description'].capitalize()}")
        st.write(f"**Wind Speed:** {weather_data['wind']['speed']} m/s")

def display_forecast(forecast_data):
    """
    Display 5-day forecast
    """
    if not forecast_data:
        return

    st.subheader("5-Day Forecast")

    # Group forecast by day
    forecast_by_day = {}
    for item in forecast_data['list']:
        date = datetime.fromtimestamp(item['dt']).date()
        if date not in forecast_by_day and len(forecast_by_day) < 5:
            forecast_by_day[date] = item

    # Create columns for forecast
    cols = st.columns(len(forecast_by_day))

    for i, (date, forecast) in enumerate(forecast_by_day.items()):
        with cols[i]:
            st.write(f"**{date.strftime('%a %d')}**")
            icon_code = forecast['weather'][0]['icon']
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            st.image(icon_url, width=50)
            st.write(f"{forecast['main']['temp']:.1f}°C")
            st.write(f"{forecast['weather'][0]['description'].capitalize()}")

def main():
    # Set page configuration
    st.set_page_config(page_title="Weather App", page_icon=":sunny:", layout="wide")

    # Title
    st.title("🌦️ Weather Forecast App")

    # City input
    city = st.text_input("Enter City Name", "London")

    if st.button("Get Weather"):
        # Fetch and display current weather
        weather_data = get_weather_data(city)
        if weather_data:
            st.subheader(f"Current Weather in {city}")
            display_current_weather(weather_data)

        # Fetch and display forecast
        forecast_data = get_forecast_data(city)
        if forecast_data:
            display_forecast(forecast_data)

if __name__ == "__main__":
    main()

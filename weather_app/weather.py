import requests

API_KEY = "ef24629fbcd43b9b97586c04851f8a2d"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
BASE_URL_forecast = "http://api.openweathermap.org/data/2.5/forecast"

#lat = 50.45
#lot = 30.52


# Function to get current weather data for a city
def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url)

def get_forecast_five_units(lat, lon):
    url = f"{BASE_URL_forecast}?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    return requests.get(url)

def get_forecast_five(lat, lon):
    url = f"{BASE_URL_forecast}?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url)

def get_pollution(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url)
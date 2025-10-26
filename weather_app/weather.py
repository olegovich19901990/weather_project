import requests

API_KEY = "ef24629fbcd43b9b97586c04851f8a2d"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
BASE_URL_forecast = "http://api.openweathermap.org/data/2.5/forecast"
BASE_URL_GEO = "http://api.openweathermap.org/geo/1.0"

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

def get_geocoding(city):
    url = f"{BASE_URL_GEO}/direct?q={city}&limit=1&appid={API_KEY}"
    return requests.get(url)

def get_geocoding_zip(zip_code, country_code):
    url = f"{BASE_URL_GEO}/zip?zip={zip_code},{country_code}&appid={API_KEY}"
    return requests.get(url)

def get_geocoding_coordinates(lat, lon):
    url = f"http://api.openweathermap.org/geo/1.0/reverse?lat={lat}&lon={lon}&limit=1&appid={API_KEY}"
    return requests.get(url)

def get_forecast_climate(lat, lon):
    url = f"http://api.openweathermap.org/data/2.5/forecast/climate?lat={lat}&lon={lon}&appid={API_KEY}"
    return requests.get(url)

def get_forecast_climate_city(city, country_code):
    #https://pro.openweathermap.org/data/2.5/forecast/climate?q={city name},{country code}&appid={API key}
    url = f"http://api.openweathermap.org/data/2.5/forecast/climate?q={city},{country_code}&appid={API_KEY}"
    return requests.get(url)

def get_forecast_climate_xml(city, country_code):
    #api.openweathermap.org/data/2.5/forecast/climate?q=London&mode=xml
    url = f"http://api.openweathermap.org/data/2.5/forecast/climate?q={city},{country_code}&appid={API_KEY}&mode=xml"
    return requests.get(url)

def get_forecast_climate_cnt_city(city, country_code, cnt):
    #api.openweathermap.org/data/2.5/forecast/climate?q=London&cnt=7
    url = f"http://api.openweathermap.org/data/2.5/forecast/climate?q={city},{country_code}&appid={API_KEY}&cnt={cnt}"
    return requests.get(url)



def get_forecast_climate_units(city, country_code, unit):
    #api.openweathermap.org/data/2.5/forecast/climate?q=London&units=metric
    url = f"http://api.openweathermap.org/data/2.5/forecast/climate?q={city},{country_code}&appid={API_KEY}&units={unit}"
    return requests.get(url)

def get_forecast_climate_lang(city, country_code, lang):
    #api.openweathermap.org/data/2.5/forecast/climate?q=London&lang=ua
    url = f"http://api.openweathermap.org/data/2.5/forecast/climate?q={city},{country_code}&appid={API_KEY}&lang={lang}"
    return requests.get(url)

def get_historical_weather(lat, lon, start_unix, end_unix):
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_unix}&end={end_unix}&appid={API_KEY}"
    return requests.get(url)

def get_historical_weather_cnt(lat, lon, start_unix, cnt):
    url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_unix}&cnt={cnt}&appid={API_KEY}"
    return requests.get(url)
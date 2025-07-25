import requests

API_KEY = "ef24629fbcd43b9b97586c04851f8a2d"
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

def get_weather(city):
    url = f"{BASE_URL}?q={city}&appid={API_KEY}&units=metric"
    return requests.get(url)
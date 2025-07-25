from weather_app.weather import get_weather

def test_weather_api_response_status():
    response = get_weather("Kyiv")
    assert response.status_code == 200

def test_weather_api_response_content():
    response = get_weather("Kyiv")
    data = response.json()
    assert 'main' in data
    assert 'temp' in data['main']
    assert 'feels_like' in data['main']
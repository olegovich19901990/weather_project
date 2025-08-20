import pytest
from weather_app.weather import get_forecast_five

#api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
@pytest.fixture
def coordinates():
    return (50.45, 30.52)


def test_hourly_five(coordinates):
    lat, lon = coordinates
    response = get_forecast_five(lat, lon)
    assert response.status_code == 200
    assert response.json() is not None

def test_hourly_five_units(coordinates):
    lat, lon =coordinates
    response = get_forecast_five(lat, lon)
    assert response.status_code == 200

def test_hourly_five_response_content(coordinates):
    lat, lon = coordinates
    response = get_forecast_five(lat, lon)
    data = response.json()
    assert 'list' in data
    assert isinstance(data['list'], list)
    assert len(data['list']) > 0
    item_1 = data['list'][0]
    assert 'main' in item_1
    assert 'temp' in item_1['main']
    assert 'feels_like' in item_1['main']
    assert 'temp_max' in item_1['main']
    assert 'weather'in item_1
    assert isinstance(item_1['weather'], list)
    assert len(item_1['weather']) > 0
    assert 'main' in item_1['weather'][0]
    assert 'description' in item_1['weather'][0]
    assert 'clouds' in item_1
    assert 'all' in item_1['clouds']
    assert 'wind' in item_1
    assert 'speed' in item_1['wind']
    assert 'deg' in item_1['wind']
    assert 'gust' in item_1['wind']

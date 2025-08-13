from weather_app.weather import get_forecast_five

#api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}

def test_hourly_five():
    response = get_forecast_five(50.45, 30.52)
    assert response.status_code == 200
    assert response.json() is not None

def test_hourly_five_units():
    response = get_forecast_five(50.45, 30.52)
    assert response.status_code == 200

def test_hourly_five_response_content():
    response = get_forecast_five(50.45, 30.52)
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

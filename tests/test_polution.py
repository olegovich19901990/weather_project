import pytest
from weather_app.weather import get_pollution

@pytest.fixture
def coordinates():
    return (50, 30)

def test_pollution_status(coordinates):
    lat, lon = coordinates
    response = get_pollution(lat, lon)
    assert response.status_code == 200

def test_pollution(coordinates):
    lat, lon = coordinates
    response = get_pollution(lat, lon)
    assert response.status_code == 200
    assert response.json() is not None

def test_pollution_response_content(coordinates):
    lat, lon = coordinates
    response = get_pollution(lat, lon)
    data = response.json()
    assert 'list' in data
    assert isinstance(data['list'], list)      # список объектов
    assert len(data['list']) > 0               # список не пустой
    item_list = data['list'][0]                # первый объект в списке
    assert 'main' in item_list                 # объект содержит ключ 'main'
    assert 'aqi' in item_list ['main']         # объект 'main' содержит ключ 'aqi'
    assert 'components' in item_list           # объект содержит ключ 'components'
    assert 'co' in item_list['components']     # объект 'components' содержит ключ 'co'
    assert 'no' in item_list['components']
    assert 'no2' in item_list['components']
    assert 'o3' in item_list['components']
    assert 'so2' in item_list['components']
    assert 'pm2_5' in item_list['components']
    assert 'pm10' in item_list['components']
    assert 'nh3' in item_list['components']
    assert 'dt' in item_list

# components = item_list['components']        по другому внутри списка списка проверять
#     for key in ['co', 'no', 'no2', 'o3', 'so2', 'pm2_5', 'pm10', 'nh3']:
#         assert key in components

#как сделать тесты под разные параметры lat, lon?
#как вставить параметризированные тесты в pytest?


@pytest.mark.parametrize("lat, lon", [
    (-90, 0),      # минимальная широта
    (90, 0),       # максимальная широта
    (0, -180),     # минимальная долгота
    (0, 180),      # максимальная долгота
    (-91, 0),      # за границей широты
    (91, 0),       # за границей широты
    (0, -181),     # за границей долготы
    (0, 181),      # за границей долготы
])
def test_coordinates_boundaries(lat, lon):
    response = get_pollution(lat, lon)

    if -90 <= lat <= 90 and -180 <= lon <= 180:
        # допустимые координаты
        assert response.status_code == 200
    else:
        # ожидаем ошибку (например, 400 или 404, зависит от API)
        assert response.status_code != 200
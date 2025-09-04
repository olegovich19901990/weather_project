import pytest
import logging
import time
import json
from weather_app.weather import get_pollution

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,# мінімальний рівень (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test_log.log", mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@pytest.fixture
def coordinates():
    return (50, 30)

def test_pollution_status(coordinates):
    start = time.perf_counter()
    logger.info(f"Testing pollution status for ({coordinates})")
    lat, lon = coordinates
    response = get_pollution(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_pollution(coordinates):
    start = time.perf_counter()
    logger.info(f"Testing pollution for ({coordinates})")
    lat, lon = coordinates
    response = get_pollution(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_pollution_response_content(coordinates):
    start = time.perf_counter()
    logger.info(f"Testing pollution response content for ({coordinates})")
    lat, lon = coordinates
    response = get_pollution(lat, lon)
    data = response.json()
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    data = response.json()
    if response.status_code == 200:
        # logger.info(f"Response JSON keys: {list(response.json().keys())}") #виводить тільки ключі верхнього рівня
        logger.info("Full Response JSON:\n" + json.dumps(data, indent=2, ensure_ascii=False))
    assert 'list' in data
    assert isinstance(data['list'], list)      # список об'єктів
    assert len(data['list']) > 0               # список не пустий
    item_list = data['list'][0]                # перший об'єкт в списку
    assert 'main' in item_list                 # об'єкт включає ключ 'main'
    assert 'aqi' in item_list ['main']         # об'єкт 'main' включає  ключ 'aqi'
    assert 'components' in item_list           # об'єкт включає  ключ 'components'
    assert 'co' in item_list['components']     # об'єкт 'components' включає  ключ 'co'
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
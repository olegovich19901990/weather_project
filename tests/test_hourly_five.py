import pytest
import logging
import time
import json
from weather_app.weather import get_forecast_five

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test_log.log", mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)
#api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={API key}
@pytest.fixture
def coordinates():
    return (50.45, 30.52)


def test_hourly_five(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing hourly five for ({lat}, {lon})")
    response = get_forecast_five(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_hourly_five_units(coordinates):
    start = time.perf_counter()
    lat, lon =coordinates
    logger.info(f"Testing hourly five for ({lat}, {lon})")
    response = get_forecast_five(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_hourly_five_response_content(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing hourly five for ({lat}, {lon})")
    response = get_forecast_five(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    data = response.json()
    if response.status_code == 200:
        #logger.info(f"Response JSON keys: {list(response.json().keys())}") #виводить тільки ключі верхнього рівня
        logger.info("Full Response JSON:\n" + json.dumps(data, indent=2, ensure_ascii=False))
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

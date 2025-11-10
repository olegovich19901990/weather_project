import pytest
import logging
import time
import json
from weather_app.weather import get_statistic_api_day
from tests.random_values import get_random_month
from tests.random_values import get_random_days



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
@pytest.fixture(scope="session")
def coordinates():
    return (50.45, 30.52)




def test_statistic_day(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    number_month = get_random_month()
    number_day = get_random_days()
    logger.info(f"Testing statistic day for ({lat}, {lon})")
    response = get_statistic_api_day(lat, lon, number_month=number_month, number_day=number_day)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None


def test_statistic_day_invalid_coordinates():
    start = time.perf_counter()
    lat, lon = 999, 999  # Invalid coordinates
    number_month = get_random_month()
    number_day = get_random_days()
    logger.info(f"Testing statistic day for invalid coordinates ({lat}, {lon})")
    response = get_statistic_api_day(lat, lon, number_month=number_month, number_day=number_day)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 500


def test_statistic_day_response_content(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    number_month = get_random_month()
    number_day = get_random_days()
    logger.info(f"Testing statistic day for ({lat}, {lon})")
    response = get_statistic_api_day(lat, lon, number_month=number_month, number_day=number_day)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    data = response.json()
    if response.status_code == 200:
        logger.info("Full Response JSON:\n" + json.dumps(data, indent=2, ensure_ascii=False))
    assert 'cod' in data
    assert data['cod'] in [200, '200']
    assert 'result' in data
    result = data['result']
    assert 'temp' in result
    assert 'pressure' in result
    assert 'humidity' in result
    assert 'wind' in result
    assert 'precipitation' in result

def test_statistic_day_unreal(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic day for edge case ({lat}, {lon})")
    response = get_statistic_api_day(lat, lon, number_month=2, number_day=33)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_statistic_day_febr(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic day for edge case ({lat}, {lon})")
    response = get_statistic_api_day(lat, lon, number_month=2, number_day=29)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_statistic_day_month_edge(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic day for edge case ({lat}, {lon})")
    response = get_statistic_api_day(lat, lon, number_month=4, number_day=31)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_statistic_day_month_edge_31(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic day for edge case ({lat}, {lon})")
    response = get_statistic_api_day(lat, lon, number_month=1, number_day=31)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_statistic_day_invalid_month(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic day for edge case ({lat}, {lon})")
    response = get_statistic_api_day(lat, lon, number_month=13, number_day=15)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_statistic_day_invalid_day(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic day for edge case ({lat}, {lon})")
    response = get_statistic_api_day(lat, lon, number_month=5, number_day=0)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400



def test_statistic_day_all(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    for number_month in range(1, 13):
        for number_day in range(1, 29):  # для лютого
            logger.info(f"Testing statistic day for ({lat}, {lon}) - Month: {number_month}, Day: {number_day}")
            response = get_statistic_api_day(lat, lon, number_month=number_month, number_day=number_day)
            duration = (time.perf_counter() - start) * 1000
            logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
            assert response.status_code == 200
            assert response.json() is not None







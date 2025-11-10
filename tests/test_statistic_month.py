import pytest
import logging
import time
from weather_app.weather import get_statistic_api_month
from tests.random_values import get_random_month


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

def test_statistic_month(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    number_month = get_random_month()
    logger.info(f"Testing statistic day for ({lat}, {lon})")
    response = get_statistic_api_month(lat, lon, number_month=number_month)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_statistic_month_invalid_coordinates():
    start = time.perf_counter()
    lat, lon = 999, 999  # Invalid coordinates
    number_month = get_random_month()
    logger.info(f"Testing statistic day for invalid coordinates ({lat}, {lon})")
    response = get_statistic_api_month(lat, lon, number_month=number_month)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 500

def test_statistic_month_response_content(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    number_month = get_random_month()
    logger.info(f"Testing statistic day for ({lat}, {lon}) and checking response content")
    response = get_statistic_api_month(lat, lon, number_month=number_month)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    data = response.json()
    assert 'cod' in data
    assert data['cod'] in [200, '200']
    assert 'result' in data
    result = data['result']
    assert 'temp' in result
    assert 'pressure' in result
    assert 'humidity' in result
    assert 'wind' in result
    assert 'precipitation' in result

def test_statistic_month_invalid_month(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    number_month = 13  # Invalid month
    logger.info(f"Testing statistic day for ({lat}, {lon}) with invalid month")
    response = get_statistic_api_month(lat, lon, number_month=number_month)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 500

def test_statistic_month_boundary_month(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    for number_month in [1, 12]:  # Testing boundary months
        logger.info(f"Testing statistic day for ({lat}, {lon}) with boundary month {number_month}")
        response = get_statistic_api_month(lat, lon, number_month=number_month)
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
        assert response.status_code == 200
        assert response.json() is not None

def test_statistic_month_leap_year_february(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    number_month = 2  # February
    logger.info(f"Testing statistic day for ({lat}, {lon}) in leap year February")
    response = get_statistic_api_month(lat, lon, number_month=number_month)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_statistic_month_non_leap_year_february(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    number_month = 2  # February
    logger.info(f"Testing statistic day for ({lat}, {lon}) in non-leap year February")
    response = get_statistic_api_month(lat, lon, number_month=number_month)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_statistic_month_edge_case_april(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    number_month = 4  # April
    logger.info(f"Testing statistic day for ({lat}, {lon}) in edge case April")
    response = get_statistic_api_month(lat, lon, number_month=number_month)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_statistic_month_all(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic day for ({lat}, {lon}) for all months")
    for number_month in range(1, 13):
        response = get_statistic_api_month(lat, lon, number_month=number_month)
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"Responce status: {response.status_code}, time: {duration:.2f} for month {number_month}")
        assert response.status_code == 200
        assert response.json() is not None

def test_statistic_month_performance(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    number_month = get_random_month()
    logger.info(f"Testing performance of statistic day for ({lat}, {lon})")
    response = get_statistic_api_month(lat, lon, number_month=number_month)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert duration < 2000  # менше 2000 мс


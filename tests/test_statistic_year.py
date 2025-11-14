import pytest
import logging
import time
from weather_app.weather import get_statistic_api_year



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

def test_statistic_year(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic year for ({lat}, {lon})")
    response = get_statistic_api_year(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_statistic_year_invalid_coordinates():
    start = time.perf_counter()
    lat, lon = 999, 999  # Invalid coordinates
    logger.info(f"Testing statistic year for invalid coordinates ({lat}, {lon})")
    response = get_statistic_api_year(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 502

def test_statistic_year_response_content(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic year for ({lat}, {lon}) and checking response content")
    response = get_statistic_api_year(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    data = response.json()
    assert 'cod' in data
    assert data['cod'] in [200, '200']
    assert 'result' in data
    result = data['result']

def test_statistic_year_response_empty_result(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic year for ({lat}, {lon}) and checking for empty result")
    response = get_statistic_api_year(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    data = response.json()
    assert 'result' in data
    result = data['result']
    assert result != {}  # Не пусте

def  test_statistic_year_invalid_year_parameter(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing statistic year for ({lat}, {lon}) with invalid year parameter")
    try:
        response = get_statistic_api_year(lat, lon, year="invalid_year")
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
        assert response.status_code == 400 or response.status_code == 500
    except TypeError:
        logger.info("Caught TypeError as expected for invalid year parameter")

def test_statistic_year_boundary_coordinates():
    start = time.perf_counter()
    test_coords = [
        (90.0, 0.0),    # North Pole
        (-90.0, 0.0),   # South Pole
        (0.0, 180.0),   # International Date Line East
        (0.0, -180.0)   # International Date Line West
    ]
    for lat, lon in test_coords:
        logger.info(f"Testing statistic year for boundary coordinates ({lat}, {lon})")
        response = get_statistic_api_year(lat, lon)
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
        assert response.status_code == 200
        assert response.json() is not None

def test_statistic_year_performance(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing performance of statistic year for ({lat}, {lon})")
    response = get_statistic_api_year(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert duration < 15000

import pytest
import logging
import time
from weather_app.weather import get_historical_weather



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

@pytest.fixture
def coordinates():
    return (50.450001, 30.523333)

def test_historical_weather(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for ({lat}, {lon})")
    now = int(time.time()) #time.time поточний час як число секунд з плаваючою крапкою від початку епохи UNIX (1970-01-01 UTC), але int робе ціле число
    one_day = 86400 # кількість секунд в одному дні
    start_unix = now - 3 * one_day #три дні тому
    end_unix = now - 2 * one_day #два дні тому
    #dt = now - hours_ago * 3600 #кількість секунд в одній годині
    response = get_historical_weather(lat, lon, start_unix, end_unix)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_historical_weather_invalid_coordinates():
    ti = time.perf_counter()
    lat, lon = 999, 999  # Invalid coordinates
    logger.info(f"Testing historical weather for invalid coordinates ({lat}, {lon})")
    now = int(time.time())
    one_day = 86400
    start_unix = now - 3 * one_day
    end_unix = now - 2 * one_day
    response = get_historical_weather(lat, lon, start_unix, end_unix)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_historical_weather_invalid_time_range(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for ({lat}, {lon}) with invalid time range")
    now = int(time.time())
    one_day = 86400
    start_unix = now + one_day  # майбутнє
    end_unix = now + 2 * one_day  # майбутнє
    response = get_historical_weather(lat, lon, start_unix, end_unix)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_historical_weather_edge_case(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for edge case ({lat}, {lon})")
    now = int(time.time())
    one_day = 86400
    start_unix = now - one_day  # вчора
    end_unix = now  # зараз
    response = get_historical_weather(lat, lon, start_unix, end_unix)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_historical_weather_not_hour(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for ({lat}, {lon}) with non-hour type")
    now = int(time.time())
    one_day = 86400
    start_unix = now - 3 * one_day
    end_unix = now - 2 * one_day
    # Here we would modify the function to accept a 'type' parameter if it were designed that way.
    # Since the current function does not support it, this test is more of a placeholder.
    response = get_historical_weather(lat, lon, start_unix, end_unix)  # type is fixed as 'hour' in the function
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

# def test_historical_weather_without_start_unix_and_end_unix(coordinates):
#     ti = time.perf_counter()
#     lat, lon = coordinates
#     logger.info(f"Testing historical weather for ({lat}, {lon}) without start and end unix times")
# #    now = int(time.time())
# #    one_day = 86400
# #    start_unix = now - 3 * one_day
# #    end_unix = now - 2 * one_day
#     response = get_historical_weather(lat, lon)
#     duration = (time.perf_counter() - ti) * 1000
#     logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
#     assert response.status_code == 200
#     assert response.json() is not None



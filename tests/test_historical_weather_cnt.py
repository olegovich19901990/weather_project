import pytest
import logging
import time
from weather_app.weather import get_historical_weather_cnt

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

def test_historical_weather_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for ({lat}, {lon})")
    now = int(time.time()) #time.time поточний час як число секунд з плаваючою крапкою від початку епохи UNIX (1970-01-01 UTC), але int робе ціле число
    one_day = 86400 # кількість секунд в одному дні
    start_unix = now - 3 * one_day #три дні тому
    cnt = 24  # кількість годин даних для отримання
    response = get_historical_weather_cnt(lat, lon, start_unix, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_historical_weather_cnt_invalid_coordinates():
    ti = time.perf_counter()
    lat, lon = 999, 999  # Invalid coordinates
    logger.info(f"Testing historical weather for invalid coordinates ({lat}, {lon})")
    now = int(time.time())
    one_day = 86400
    start_unix = now - 3 * one_day
    cnt = 24
    response = get_historical_weather_cnt(lat, lon, start_unix, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 404

def test_historical_weather_cnt_invalid_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for ({lat}, {lon}) with invalid cnt")
    now = int(time.time())
    one_day = 86400
    start_unix = now - 3 * one_day
    cnt = -5  # Invalid cnt
    response = get_historical_weather_cnt(lat, lon, start_unix, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_historical_weather_cnt_future_start_time(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for ({lat}, {lon}) with future start time")
    now = int(time.time())
    one_day = 86400
    start_unix = now + one_day  # майбутнє
    cnt = 24
    response = get_historical_weather_cnt(lat, lon, start_unix, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_historical_weather_cnt_edge_case(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for edge case ({lat}, {lon})")
    now = int(time.time())
    one_day = 86400
    start_unix = now - one_day  # вчора
    cnt = 24
    response = get_historical_weather_cnt(lat, lon, start_unix, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_historical_weather_cnt_large_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for ({lat}, {lon}) with large cnt")
    now = int(time.time())
    one_day = 86400
    start_unix = now - 5 * one_day
    cnt = 200  # Large cnt
    response = get_historical_weather_cnt(lat, lon, start_unix, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_historical_weather_cnt_zero_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing historical weather for ({lat}, {lon}) with zero cnt")
    now = int(time.time())
    one_day = 86400
    start_unix = now - 3 * one_day
    cnt = 0  # Zero cnt
    response = get_historical_weather_cnt(lat, lon, start_unix, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200


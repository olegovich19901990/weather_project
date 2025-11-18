import pytest
import logging
import time

from tests.random_values import get_random_cnt
from weather_app.weather import get_forecast_30_days
from weather_app.weather import get_forecast_30_days_unit
from weather_app.weather import get_forecast_30_days_lang
from weather_app.weather import get_forecast_30_days_xml




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

def test_forecast_30_days(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) - {cnt} days")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None


def test_forecast_30_days_invalid_coordinates():
    ti = time.perf_counter()
    lat, lon = 999, 999  # НЕвалідні координати
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for invalid coordinates ({lat}, {lon}) - {cnt} days")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 404


def test_forecast_30_days_invalid_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = -5  # НЕВАЛІДНИЙ cnt
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) with invalid cnt {cnt}")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 404

def test_forecast_30_days_zero_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = 0  # Нульовий cnt
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) with zero cnt {cnt}")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 404

def  test_forecast_40_days_exceeding_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = 20  # cnt, що перевищує максимальне значення
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) with exceeding cnt {cnt}")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 404

def test_forecast_30_days_boundary_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = 32  # граничне значення cnt
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) with boundary cnt {cnt}")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast_30_days_minimum_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = 1  # мінімальне значення cnt
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) with minimum cnt {cnt}")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast_30_days_large_coordinates():
    ti = time.perf_counter()
    lat, lon = 90.0, 180.0  # максимальні допустимі координати
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for large coordinates ({lat}, {lon}) - {cnt} days")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None


def test_forecast_30_days_small_coordinates():
    ti = time.perf_counter()
    lat, lon = -90.0, -180.0  # мінімальні допустимі координати
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for small coordinates ({lat}, {lon}) - {cnt} days")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast_30_days_fractional_coordinates():
    ti = time.perf_counter()
    lat, lon = 45.6789, 123.4567  # дробові координати
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for fractional coordinates ({lat}, {lon}) - {cnt} days")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None


def test_forecast_30_days_negative_coordinates():
    ti = time.perf_counter()
    lat, lon = -45.6789, -123.4567  # від'ємні дробові координати
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for negative coordinates ({lat}, {lon}) - {cnt} days")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None


def test_forecast_30_days_json(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) - {cnt} days with JSON response")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    try:
        data = response.json()
        assert data is not None
    except ValueError:
        pytest.fail("Response is not in JSON format")

def test_forecast_30_days_response_time(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) - {cnt} days for response time")
    response = get_forecast_30_days(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert duration < 2000  # перевірка, що час відповіді менший за 2000 мс

def test_forecast_30_days_xml(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) - {cnt} days with XML response")
    response = get_forecast_30_days_xml(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.content is not None
    assert b'<?xml' in response.content  # перевірка, що відповідь містить XML декларацію
    assert b'<forecast>' in response.content  # перевірка, що відповідь містить тег forecast
    assert b'</forecast>' in response.content  # перевірка, що відповідь містить закриваючий тег forecast


def test_forecast_30_days_xml_invalid_coordinates():
    ti = time.perf_counter()
    lat, lon = 999, 999  # НЕвалідні координати
    cnt = get_random_cnt()
    logger.info(f"Testing 30-day forecast for invalid coordinates ({lat}, {lon}) - {cnt} days with XML response")
    response = get_forecast_30_days_xml(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400 or response.status_code == 404


def test_forecast_30_days_unit(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = get_random_cnt()
    unit = "metric"
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) - {cnt} days with unit={unit}")
    response = get_forecast_30_days_unit(lat, lon, cnt, unit)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    data = response.json()
    for day in data.get('list', []):
        temp = day.get('temp', {})
        assert 'day' in temp  # перевірка, що денна температура присутня
        assert isinstance(temp['day'], (int, float))  # перевірка, що температура є числом



def test_forecast_30_days_unit(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = get_random_cnt()
    unit = "imperial"
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) - {cnt} days with unit={unit}")
    response = get_forecast_30_days_unit(lat, lon, cnt, unit)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    data = response.json()
    for day in data.get('list', []):
        temp = day.get('temp', {})
        assert 'day' in temp  # перевірка, що денна температура присутня
        assert isinstance(temp['day'], (int, float))  # перевірка, що температура є числом


def test_forecast_30_days_lang(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = get_random_cnt()
    lang = "es"
    logger.info(f"Testing 30-day forecast for ({lat}, {lon}) - {cnt} days with lang={lang}")
    response = get_forecast_30_days_lang(lat, lon, cnt, lang)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    data = response.json()
    weather_descriptions = [day.get('weather', [{}])[0].get('description', '') for day in data.get('list', [])]
    assert all(isinstance(desc, str) and desc != '' for desc in weather_descriptions)

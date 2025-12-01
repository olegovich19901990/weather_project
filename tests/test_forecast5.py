import pytest
import logging
import time
from weather_app.weather import get_forecast5
from weather_app.weather import get_forecast5_units
from weather_app.weather import get_forecast5_cnt
from weather_app.weather import get_forecast5_lang
from weather_app.weather import get_forecast5_xml

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

def test_forecast5(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing 5-day forecast for coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_invalid_coordinates():
    ti = time.perf_counter()
    lat, lon = 999, 999  # НЕвалідні координати
    logger.info(f"Testing 5-day forecast for invalid coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 400 or response.status_code == 404

def test_forecast5_boundary_coordinates():
    ti = time.perf_counter()
    lat, lon = 90, 180  # Граничні координати
    logger.info(f"Testing 5-day forecast for boundary coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_zero_coordinates():
    ti = time.perf_counter()
    lat, lon = 0, 0  # координати в точці перетину екватора і нульового меридіана
    logger.info(f"Testing 5-day forecast for zero coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_high_precision_coordinates():
    ti = time.perf_counter()
    lat, lon = 50.4500012345, 30.5233336789  # найвищі координати
    logger.info(f"Testing 5-day forecast for high precision coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_negative_coordinates():
    ti = time.perf_counter()
    lat, lon = -50.450001, -30.523333  # від'ємні координати
    logger.info(f"Testing 5-day forecast for negative coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_edge_case(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing 5-day forecast for edge case ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_large_coordinates():
    ti = time.perf_counter()
    lat, lon = 1e6, 1e6  # дуже великі координати
    logger.info(f"Testing 5-day forecast for large coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 400 or response.status_code == 404

def test_forecast5_small_coordinates():
    ti = time.perf_counter()
    lat, lon = -1e6, -1e6  # дуже малі координати
    logger.info(f"Testing 5-day forecast for small coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 400 or response.status_code == 404

def test_forecast5_non_numeric_coordinates():
    ti = time.perf_counter()
    lat, lon = "abc", "def"  # нечислові координати
    logger.info(f"Testing 5-day forecast for non-numeric coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 400 or response.status_code == 404

def test_forecast5_missing_coordinates():
    ti = time.perf_counter()
    lat, lon = None, None  # відсутні координати
    logger.info(f"Testing 5-day forecast for missing coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 400 or response.status_code == 404

def test_forecast5_extreme_coordinates():
    ti = time.perf_counter()
    lat, lon = 1e10, -1e10  # екстремальні координати
    logger.info(f"Testing 5-day forecast for extreme coordinates ({lat}, {lon})")
    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 400 or response.status_code == 404

def test_forecast_invalid_api_key(coordinates, monkeypatch):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing 5-day forecast with invalid API key for coordinates ({lat}, {lon})")

    def mock_get_forecast5(lat, lon):
        class MockResponse:
            status_code = 401
            def json(self):
                return {"message": "Invalid API key"}
        return MockResponse()

    monkeypatch.setattr('weather_app.weather.get_forecast5', mock_get_forecast5)

    response = get_forecast5(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200

def test_forecast5_units(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    unit = "metric"
    logger.info(f"Testing 5-day forecast with units='{unit}' for coordinates ({lat}, {lon})")
    response = get_forecast5_units(lat, lon, unit)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_units_2(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    unit = "imperial"
    logger.info(f"Testing 5-day forecast with units='{unit}' for coordinates ({lat}, {lon})")
    response = get_forecast5_units(lat, lon, unit)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_units_invalid(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    unit = "invalid_unit"
    logger.info(f"Testing 5-day forecast with invalid units='{unit}' for coordinates ({lat}, {lon})")
    response = get_forecast5_units(lat, lon, unit)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_lang(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    lang = "es"
    logger.info(f"Testing 5-day forecast with lang='{lang}' for coordinates ({lat}, {lon})")
    response = get_forecast5_lang(lat, lon, lang)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_xml(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing 5-day forecast in XML format for coordinates ({lat}, {lon})")
    response = get_forecast5_xml(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.content is not None
    assert response.headers["Content-Type"] == "application/xml; charset=utf-8" # перевірка типу контенту
    assert b"<weatherdata>" in response.content # перевірка наявності кореневого елемента
    assert b"<location" in response.content # перевірка наявності елемента місцезнаходження
    assert b"<forecast" in response.content # перевірка наявності елемента прогнозу

def test_forecast5_cnt(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = 10
    logger.info(f"Testing 5-day forecast with cnt='{cnt}' for coordinates ({lat}, {lon})")
    response = get_forecast5_cnt(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast5_cnt_invalid(coordinates):
    ti  = time.perf_counter()
    lat, lon = coordinates
    cnt = -5  # невалідне значення cnt
    logger.info(f"Testing 5-day forecast with invalid cnt='{cnt}' for coordinates ({lat}, {lon})")
    response = get_forecast5_cnt(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 400 or response.status_code == 200

def test_forecast5_cnt_zero(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    cnt = 0  # нульовий cnt
    logger.info(f"Testing 5-day forecast with zero cnt='{cnt}' for coordinates ({lat}, {lon})")
    response = get_forecast5_cnt(lat, lon, cnt)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200 or response.status_code == 404






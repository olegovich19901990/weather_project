import pytest
import logging
import time
from weather_app.weather import get_forecast_five_units
from weather_app.weather import get_pollution
from weather_app.weather import get_forecast_five

for handler in logging.root.handlers[:]:
    logging.root.removeHandler(handler)
#pytest -s -v --log-cli-level=INFO
#або в pytest.ini (щоб завжди працювало)
#[pytest]
#log_cli = true
#log_cli_level = INFO
#log_cli_format = %(asctime)s [%(levelname)s] %(message)s


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("test_log.log", mode="w", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

test_cities = [
    ("Kyiv", (50.450001, 30.523333)),
    ("London", (51.507351, -0.127758)),
    ("Tokyo", (35.689487, 139.691711)),
]

@pytest.mark.parametrize("city,coordinates", test_cities)
def test_hourly_five(city,coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing 5-day forecast for {city} ({lat}, {lon})")
    response = get_forecast_five(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200, f"Failed for {city}"

@pytest.mark.parametrize("city,coordinates", test_cities)
def test_hourly_five_units(city, coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing 5-day forecast for {city} ({lat}, {lon})")
    response = get_forecast_five_units(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200, f"Failed for {city}"

@pytest.mark.parametrize("city,coordinates", test_cities)
def test_pollution(city, coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing 5-day forecast for {city} ({lat}, {lon})")
    response = get_pollution(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200, f"Failed for {city}"
    assert response.json() is not None
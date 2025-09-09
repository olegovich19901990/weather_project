from weather_app.weather import get_geocoding
from weather_app.weather import get_geocoding_zip
from weather_app.weather import get_geocoding_coordinates
import logging
import time


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

def test_geocoding():
    city = "Kyiv"
    start = time.perf_counter()
    logger.info(f"Testing geocoding for ({city})")
    response = get_geocoding(city)
    assert response.status_code == 200
    data = response.json()
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert isinstance(data, list)      # перевіряємо, що відповідь є списком
    assert len(data) > 0               # перевіряємо, що список не порожній
    first_result = data[0]             # беремо перший результат
    assert 'lat' in first_result       # перевіряємо, що є ключ 'lat'
    assert 'lon' in first_result       # перевіряємо, що є ключ 'lon'
    assert isinstance(first_result['lat'], (float, int))  # перевіряємо, що lat є числом
    assert isinstance(first_result['lon'], (float, int))  # перевіряємо, що lon є числом



def test_geocoding_invalid_city():
    city = "InvalidCityName5"
    start = time.perf_counter()
    logger.info(f"Testing geocoding for ({city})")
    response = get_geocoding(city)
    assert response.status_code == 200
    data = response.json()
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert isinstance(data, list)      # перевіряємо, що відповідь є списком
    assert len(data) == 0              # перевіряємо, що список порожній для невідомого міста


def test_geocoding_empty_city():
    city = ""
    start = time.perf_counter()
    logger.info(f"Testing geocoding for ({city})")
    response = get_geocoding(city)
    assert response.status_code == 400
    data = response.json()
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert isinstance(data, list)      # перевіряємо, що відповідь є списком
    assert len(data) == 0              # перевіряємо, що список порожній для пустого міста

def test_geocoding_zip_code():
    zip_code = "E14"
    country_code = "GB"
    start = time.perf_counter()
    logger.info(f"Testing geocoding for ({zip_code}, {country_code})")
    response = get_geocoding_zip(zip_code, country_code)
    assert response.status_code == 200
    data = response.json()
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert isinstance(data, list)      # перевіряємо, що відповідь є списком
    assert len(data) > 0               # перевіряємо, що список не порожній
    first_result = data[0]             # беремо перший результат
    assert 'lat' in first_result       # перевіряємо, що є ключ 'lat'
    assert 'lon' in first_result       # перевіряємо, що є ключ 'lon'
    assert isinstance(first_result['lat'], (float, int))  # перевіряємо, що lat є числом
    assert isinstance(first_result['lon'], (float, int))  # перевіряємо, що lon є числом


def test_geocoding_coordinates():
    lat = 51.5074
    lon = -0.1278
    start = time.perf_counter()
    logger.info(f"Testing geocoding for ({lat}, {lon})")
    response = get_geocoding_coordinates(lat, lon)
    assert response.status_code == 200
    data = response.json()
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert isinstance(data, list)      # перевіряємо, що відповідь є списком
    assert len(data) > 0               # перевіряємо, що список не порожній
    first_result = data[0]             # беремо перший результат
    assert 'name' in first_result      # перевіряємо, що є ключ 'name'
    assert 'country' in first_result   # перевіряємо, що є ключ 'country'
    assert 'lat' in first_result       # перевіряємо, що є ключ 'lat'
    assert 'lon' in first_result       # перевіряємо, що є ключ 'lon'
    assert isinstance(first_result['lat'], (float, int))  # перевіряємо, що lat є числом
    assert isinstance(first_result['lon'], (float, int))  # перевіряємо, що lon є числом
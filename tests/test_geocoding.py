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
    
    try:
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

        logger.info(f"Test PASSED for city: {city}")
    
    except AssertionError as e:
        logger.error(f"Assertion failed: {e}")
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during test: {e}")
        raise


# def test_geocoding_invalid_city():
#     city = "InvalidCityName5"
#     start = time.perf_counter()
#     logger.info(f"Testing geocoding for ({city})")
#     response = get_geocoding(city)
#     assert response.status_code == 200
#     data = response.json()
#     duration = (time.perf_counter() - start) * 1000
#     logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
#     assert isinstance(data, list)      # перевіряємо, що відповідь є списком
#     assert len(data) == 0              # перевіряємо, що список порожній для невідомого міста
def test_geocoding_invalid_city_try_except():
    city = "InvalidCityName5"
    start = time.perf_counter()
    logger.info(f"Testing geocoding for ({city})")

    try:
        response = get_geocoding(city)
        if response.status_code != 200:
            raise AssertionError(f"Unexpected status code: {response.status_code}")

        data = response.json()
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")

        if not isinstance(data, list):
            raise AssertionError("Response is not a list")
        if len(data) != 0:
            raise AssertionError(f"Expected empty list, got {len(data)} items")

    except Exception as e:
        logger.error(f"Test failed for city '{city}': {e}")
        raise  # піднімаємо далі, щоб pytest позначив тест як failed

# def test_geocoding_empty_city():
#     city = ""
#     start = time.perf_counter()
#     logger.info(f"Testing geocoding for empty({city})")
#     response = get_geocoding(city)
#     assert response.status_code == 400
#     data = response.json()
#     duration = (time.perf_counter() - start) * 1000
#     logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
#     assert isinstance(data, dict)      # перевіряємо, що відповідь є списком
#     assert len(data) == 2              # перевіряємо, що список порожній для пустого міста
def test_geocoding_empty_city_try_except():
    city = ""
    start = time.perf_counter()
    logger.info(f"Testing geocoding for empty({city})")

    try:
        response = get_geocoding(city)
        if response.status_code != 400:
            raise AssertionError(f"Unexpected status code: {response.status_code}")

        data = response.json()
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")

        if not isinstance(data, dict):
            raise AssertionError("Response is not a dict")
        if len(data) != 2:
            raise AssertionError(f"Expected dict of length 2, got {len(data)} items")

    except Exception as e:
        logger.error(f"Test failed for empty city '{city}': {e}")
        raise   # піднімаємо далі, щоб pytest позначив тест як failed


# def test_geocoding_zip_code():
#     zip_code = "E14"
#     country_code = "GB"
#     start = time.perf_counter()
#     logger.info(f"Testing geocoding for ({zip_code}, {country_code})")
#     response = get_geocoding_zip(zip_code, country_code)
#     assert response.status_code == 200
#     data = response.json()
#     duration = (time.perf_counter() - start) * 1000
#     logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
#     assert isinstance(data, dict)      # перевіряємо, що відповідь є словником
#     assert len(data) > 0               # перевіряємо, що список не порожній
#     first_result = {"lat","lon" }      # беремо перший результат
#     assert "lat" in first_result       # перевіряємо, що є ключ 'lat'
#     assert "lon" in first_result     # перевіряємо, що є ключ 'lon'
#     assert isinstance(float(data["lat"]), float)
#     assert isinstance(float(data["lon"]), float)
def test_geocoding_zip_code_try_except():
    zip_code = "E14"
    country_code = "GB"
    start = time.perf_counter()
    logger.info(f"Testing geocoding for ({zip_code}, {country_code})")

    try:
        response = get_geocoding_zip(zip_code, country_code)
        if response.status_code != 200:
            raise AssertionError(f"Unexpected status code: {response.status_code}")

        data = response.json()
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")

        if not isinstance(data, dict):
            raise AssertionError("Response is not a dict")
        if len(data) == 0:
            raise AssertionError("Response dict is empty")

        required_keys = {"lat", "lon"}
        if not required_keys.issubset(data.keys()):
            raise AssertionError(f"Response dict missing required keys: {required_keys - data.keys()}")

        # чек lat і lon можна конвертувати у float
        try:
            lat = float(data["lat"])
            lon = float(data["lon"])
        except (ValueError, TypeError) as e:
            raise AssertionError(f"lat or lon is not a valid float: {e}")

    except Exception as e:
        logger.error(f"Test failed for zip_code '{zip_code}', country '{country_code}': {e}")
        raise

# def test_geocoding_coordinates():
#     lat = 51.5074
#     lon = -0.1278
#     start = time.perf_counter()
#     logger.info(f"Testing geocoding for ({lat}, {lon})")
#     response = get_geocoding_coordinates(lat, lon)
#     assert response.status_code == 200
#     data = response.json()
#     duration = (time.perf_counter() - start) * 1000
#     logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
#     assert isinstance(data, list)      # перевіряємо, що відповідь є списком
#     assert len(data) > 0               # перевіряємо, що список не порожній
#     first_result = data[0]             # беремо перший результат
#     assert 'name' in first_result      # перевіряємо, що є ключ 'name'
#     assert 'country' in first_result   # перевіряємо, що є ключ 'country'
#     assert 'lat' in first_result       # перевіряємо, що є ключ 'lat'
#     assert 'lon' in first_result       # перевіряємо, що є ключ 'lon'
#     assert isinstance(first_result['lat'], (float, int))  # перевіряємо, що lat є числом
#     assert isinstance(first_result['lon'], (float, int))  # перевіряємо, що lon є числом
def test_geocoding_coordinates_try_except():
    lat = 51.5074
    lon = -0.1278
    start = time.perf_counter()
    logger.info(f"Testing geocoding for ({lat}, {lon})")

    try:
        response = get_geocoding_coordinates(lat, lon)
        if response.status_code != 200:
            raise AssertionError(f"Unexpected status code: {response.status_code}")

        data = response.json()
        duration = (time.perf_counter() - start) * 1000
        logger.info(f"Response status: {response.status_code}, time: {duration:.2f}")

        if not isinstance(data, list):
            raise AssertionError("Response is not a list")
        if len(data) == 0:
            raise AssertionError("Response list is empty")

        first_result = data[0]
        required_keys = {"name", "country", "lat", "lon"}
        if not required_keys.issubset(first_result.keys()):
            raise AssertionError(f"First result missing keys: {required_keys - first_result.keys()}")

        #  lat і lon є тільки числами
        if not isinstance(first_result['lat'], (float, int)):
            raise AssertionError("lat is not a number")
        if not isinstance(first_result['lon'], (float, int)):
            raise AssertionError("lon is not a number")

    except Exception as e:
        logger.error(f"Test failed for coordinates ({lat}, {lon}): {e}")
        raise


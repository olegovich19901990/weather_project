import pytest
import logging
import time


from weather_app.weather import get_current_weather_coordinates, API_KEY
from weather_app.weather import get_current_weather_coordinates_units
from weather_app.weather import get_current_weather_coordinates_lang
from weather_app.weather import get_current_weather_coordinates_xml


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

def test_current_weather_coordinates(coordinates):
    ti = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing current weather for coordinates ({lat}, {lon})")
    response = get_current_weather_coordinates(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_current_weather_invalid_coordinates():
    ti = time.perf_counter()
    lat, lon = 999, 999  # Невалідні координати
    logger.info(f"Testing current weather for invalid coordinates ({lat}, {lon})")
    response = get_current_weather_coordinates(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 400 or response.status_code == 404

def  test_current_weather_boundary_coordinates():
    ti = time.perf_counter()
    lat, lon = 90, 180  # Граничні координати
    logger.info(f"Testing current weather for boundary coordinates ({lat}, {lon})")
    response = get_current_weather_coordinates(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_current_weather_zero_coordinates():
    ti = time.perf_counter()
    lat, lon = 0, 0  # Координати в точці перетину екватора і нульового меридіана
    logger.info(f"Testing current weather for zero coordinates ({lat}, {lon})")
    response = get_current_weather_coordinates(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_current_weather_high_prec_coordinates():
    ti = time.perf_counter()
    lat, lon = 50.4500012345, 30.5233336789  # Координати з високою точністю
    logger.info(f"Testing current weather for high precision coordinates ({lat}, {lon})")
    response = get_current_weather_coordinates(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_current_weather_negative_coordinates():
    ti = time.perf_counter()
    lat, lon = -50.450001, -30.523333  # Від'ємні координати
    logger.info(f"Testing current weather for negative coordinates ({lat}, {lon})")
    response = get_current_weather_coordinates(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.json() is not None

def test_current_weather_xml():
    ti = time.perf_counter()
    lat, lon = 50.450001, 30.523333
    logger.info(f"Testing current weather for coordinates ({lat}, {lon}) in XML format")
    url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&mode=xml"
    response = get_current_weather_coordinates_xml(lat, lon)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    assert response.content is not None
    assert response.headers["Content-Type"] == "application/xml; charset=utf-8" # перевірка типу контенту
    assert b"<current>" in response.content # перевірка наявності кореневого елемента
    assert b"<city" in response.content # перевірка наявності елемента міста
    assert b"<temperature" in response.content # перевірка наявності елемента температури

def test_current_weather_units():
    ti = time.perf_counter()
    lat, lon = 50.450001, 30.523333
    unit = "imperial"  # Фаренгейти
    logger.info(f"Testing current weather for coordinates ({lat}, {lon}) with unit=imperial")
    response = get_current_weather_coordinates_units(lat, lon, unit)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    assert "main" in data
    assert "temp" in data["main"]
    temp_fahrenheit = data["main"]["temp"]
    assert isinstance(temp_fahrenheit, (int, float))

def test_current_weather_units():
    ti = time.perf_counter()
    lat, lon = 50.450001, 30.523333
    unit = "metric"  # Цельсії
    logger.info(f"Testing current weather for coordinates ({lat}, {lon}) with unit=metric")
    response = get_current_weather_coordinates_units(lat, lon, unit)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    data = response.json()
    assert data is not None
    assert "main" in data
    assert "temp" in data["main"]
    temp_fahrenheit = data["main"]["temp"]
    assert isinstance(temp_fahrenheit, (int, float))


def test_current_weather_language():
    ti = time.perf_counter()
    lat, lon = 50.450001, 30.523333
    lng = "es"  # Іспанська мова
    logger.info(f"Testing current weather for coordinates ({lat}, {lon}) with lang=es")
    response = get_current_weather_coordinates_lang(lat, lon, lng)
    duration = (time.perf_counter() - ti) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 200
    data = response.json()
    assert data is not None # перевірка, що відповідь не порожня
    assert "weather" in data # перевірка, що в відповіді є ключ "weather"
    assert len(data["weather"]) > 0 # перевірка, що список "weather" не порожній
    description_spanish = data["weather"][0]["description"] # отримання опису погоди іспанською
    assert isinstance(description_spanish, str) # перевірка, що опис є рядком




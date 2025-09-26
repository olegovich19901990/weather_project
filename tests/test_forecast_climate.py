import pytest
import logging
import time
import json
import xml.etree.ElementTree as ET
from tests.random_values import get_random_cnt
from weather_app.weather import get_forecast_climate
from weather_app.weather import get_forecast_climate_city
from weather_app.weather import get_forecast_climate_xml
from weather_app.weather import get_forecast_climate_cnt_city
from weather_app.weather import get_forecast_climate_units
from weather_app.weather import get_forecast_climate_lang

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
#api.openweathermap.org/data/2.5/forecast/climate??lat={lat}&lon={lon}&appid={API key}
@pytest.fixture
def coordinates():
    return (50.45, 30.52)

@pytest.fixture
def params():
    return "Kyiv", "UA"


def test_forecast_climate(coordinates):
    start = time.perf_counter()
    lat, lon = coordinates
    logger.info(f"Testing forecast climate for ({lat}, {lon})")
    response = get_forecast_climate(lat, lon)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None


def test_forecast_climate_city(params):
    start = time.perf_counter()
    city, country_code = params
    logger.info(f"Testing forecast climate units for ({city}, {country_code})")
    response = get_forecast_climate_city(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_city_invalid():
    start = time.perf_counter()
    city, country_code = "InvalidCity", "XX"
    logger.info(f"Testing forecast climate units for ({city}, {country_code})")
    response = get_forecast_climate_city(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 404

def test_forecast_climate_city_empty():
    start = time.perf_counter()
    city, country_code = "", ""
    logger.info(f"Testing forecast climate for empty ({city}, {country_code})")
    response = get_forecast_climate_city(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_forecast_climate_city_special_chars():
    start = time.perf_counter()
    city, country_code = "K!yiv", "U@A"
    logger.info(f"Testing forecast climate units for special chars ({city}, {country_code})")
    response = get_forecast_climate_city(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 404

def test_forecast_climate_city_numeric():
    start = time.perf_counter()
    city, country_code = "12345", "678"
    logger.info(f"Testing forecast climate units for numeric ({city}, {country_code})")
    response = get_forecast_climate_city(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 404

def test_forecast_climate_city_whitespace():
    start = time.perf_counter()
    city, country_code = "   ", "   "
    logger.info(f"Testing forecast climate units for whitespace ({city}, {country_code})")
    response = get_forecast_climate_city(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 404

def test_forecast_climate_city_response_content_json(params):
    start = time.perf_counter()
    city, country_code = params
    logger.info(f"Testing forecast climate response content for ({city}, {country_code})")
    response = get_forecast_climate_city(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    data = response.json()
    if response.status_code == 200:
        #logger.info(f"Response JSON keys: {list(response.json().keys())}") #виводить тільки ключі верхнього рівня
        logger.info("Full Response JSON:\n" + json.dumps(data, indent=2, ensure_ascii=False)) # виводить весь json
    assert 'list' in data
    assert isinstance(data['list'], list)
    assert len(data['list']) > 0
    item_1 = data['list'][0]
    assert 'temp' in item_1

def test_forecast_climate_city_invalid_response_content():
    start = time.perf_counter()
    city, country_code = "InvalidCity", "XX"
    logger.info(f"Testing forecast climate response content for invalid ({city}, {country_code})")
    response = get_forecast_climate_city(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 404

def test_forecast_climate_response_content_xml(params):
    start = time.perf_counter()
    city, country_code = params
    logger.info(f"Testing forecast climate response content xml for ({city}, {country_code})")
    response = get_forecast_climate_xml(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")

    if response.status_code == 200:
        root = ET.fromstring(response.text)
        logger.info("Full XML response:")
        ET.dump(root)

        # приклад перевірки елементів:
        forecast_list = root.findall(".//forecast")
        assert len(forecast_list) > 0
        first = forecast_list[0]
        temp = first.find("temp")

        # Перший елемент <time> всередині <forecast>
        first_time = root.find(".//forecast/time")
        assert first_time is not None, "No <time> element found"

        temp = first_time.find("temperature")
        assert temp is not None, "No <temperature> element found"
        # Перевірка атрибутів
        assert 'day' in temp.attrib
        assert 'min' in temp.attrib
        assert 'max' in temp.attrib
        # Лог
        print(temp.attrib)

def test_forecast_climate_xml_invalid():
    start = time.perf_counter()
    city, country_code = "InvalidCity", "XX"
    logger.info(f"Testing forecast climate response content xml for invalid ({city}, {country_code})")
    response = get_forecast_climate_xml(city, country_code)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Response status: {response.status_code}, time: {duration:.2f} ms")
    assert response.status_code == 404

def test_forecast_climate_cnt(params):
    start = time.perf_counter()
    city, country_code = params
    cnt = get_random_cnt(1, 30)
    logger.info(f"Testing forecast climate for ({city}, {country_code}) for {cnt}")
    response = get_forecast_climate_cnt_city(city, country_code, cnt)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    data = response.json()
    assert 'list' in data
    assert isinstance(data['list'], list)
#    assert len(data['list']) == 5

def  test_forecast_climate_cnt_invalid(params):
    start = time.perf_counter()
    city, country_code = params
    cnt = -5
    logger.info(f"Testing forecast climate for ({city}, {country_code}) for {cnt}")
    response = get_forecast_climate_cnt_city(city, country_code, cnt)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_forecast_climate_cnt_too_large(params):
    start = time.perf_counter()
    city, country_code = params
    cnt = 50
    logger.info(f"Testing forecast climate for ({city}, {country_code}) for {cnt}")
    response = get_forecast_climate_cnt_city(city, country_code, cnt)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_forecast_climate_cnt_zero(params):
    start = time.perf_counter()
    city, country_code = params
    cnt = 0
    logger.info(f"Testing forecast climate for ({city}, {country_code}) for {cnt}")
    response = get_forecast_climate_cnt_city(city, country_code, cnt)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_forecast_climate_cnt_one(params):
    start = time.perf_counter()
    city, country_code = params
    cnt = 1
    logger.info(f"Testing forecast climate for ({city}, {country_code}) for {cnt}")
    response = get_forecast_climate_cnt_city(city, country_code, cnt)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    data = response.json()
    assert 'list' in data
    assert isinstance(data['list'], list)
    assert len(data['list']) == 1

def test_forecast_climate_cnt_non_integer(params):
    start = time.perf_counter()
    city, country_code = params
    cnt = "five"
    logger.info(f"Testing forecast climate for ({city}, {country_code}) for {cnt}")
    response = get_forecast_climate_cnt_city(city, country_code, cnt)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_forecast_climate_cnt_missing(params):
    start = time.perf_counter()
    city, country_code = params
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with missing cnt")
    response = get_forecast_climate_cnt_city(city, country_code, None)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 400

def test_forecast_climate_units(params):
    start = time.perf_counter()
    city, country_code = params
    unit = "metric" # інші варіанти: "imperial", "standard"
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with units {unit}")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast_climate_units_response_content(params):
    start = time.perf_counter()
    city, country_code = params
    unit = "metric"  # інші варіанти: "imperial", "standard"
    logger.info(f"Testing forecast climate response content units {unit} for ({city}, {country_code})")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    data = response.json()
    if response.status_code == 200:
        #logger.info(f"Response JSON keys: {list(response.json().keys())}") #виводить тільки ключі верхнього рівня
        logger.info("Full Response JSON:\n" + json.dumps(data, indent=2, ensure_ascii=False)) # виводить весь json
    assert 'list' in data
    assert isinstance(data['list'], list)
    assert len(data['list']) > 0
    item_1 = data['list'][0]
    assert 'temp' in item_1

def test_forecast_climate_units_invalid(params):
    start = time.perf_counter()
    city, country_code = params
    unit = "fffffffffff" # optional
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with invalid units {unit}")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_units_empty(params):
    start = time.perf_counter()
    city, country_code = params
    unit = "" # optional
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with empty units")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_units_missing(params):
    start = time.perf_counter()
    city, country_code = params # unit optional
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with missing units")
    response = get_forecast_climate_units(city, country_code, None)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_units_case_insensitive(params):
    start = time.perf_counter()
    city, country_code = params
    unit = "MeTrIc"
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with case-insensitive units {unit}")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast_climate_units_special_chars(params):
    start = time.perf_counter()
    city, country_code = params
    unit = "met!ric"
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with special char units {unit}")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_units_numeric(params):
    start = time.perf_counter()
    city, country_code = params
    unit = "123"
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with numeric units {unit}")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_units_whitespace(params):
    start = time.perf_counter()
    city, country_code = params
    unit = "   "
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with whitespace units")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_units_long_string(params):
    start = time.perf_counter()
    city, country_code = params
    unit = "metric" * 100
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with long string units")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_units_none(params):
    start = time.perf_counter()
    city, country_code = params
    unit = None
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with None units")
    response = get_forecast_climate_units(city, country_code, unit)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_lang(params):
    start = time.perf_counter()
    city, country_code = params
    lang = "es"  # іспанська  el Greek ja Japanese ua, uk Ukrainian la Latvian
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with lang {lang}")
    response = get_forecast_climate_lang (city, country_code, lang)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200
    assert response.json() is not None

def test_forecast_climate_lang_response_content(params):
    start = time.perf_counter()
    city, country_code = params
    lang = "es"  # іспанська  el Greek ja Japanese ua, uk Ukrainian la Latvian
    logger.info(f"Testing forecast climate response content lang {lang} for ({city}, {country_code})")
    response = get_forecast_climate_lang (city, country_code, lang)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    data = response.json()
    if response.status_code == 200:
        #logger.info(f"Response JSON keys: {list(response.json().keys())}") #виводить тільки ключі верхнього рівня
        logger.info("Full Response JSON:\n" + json.dumps(data, indent=2, ensure_ascii=False)) # виводить весь json
    assert 'list' in data
    assert isinstance(data['list'], list)
    assert len(data['list']) > 0
    item_1 = data['list'][0]
    assert 'temp' in item_1

def test_forecast_climate_lang_invalid(params):
    start = time.perf_counter()
    city, country_code = params
    lang = "invalid_lang" #optional
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with invalid lang {lang}")
    response = get_forecast_climate_lang (city, country_code, lang)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_lang_empty(params):
    start = time.perf_counter()
    city, country_code = params
    lang = "" #optional
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with empty lang")
    response = get_forecast_climate_lang (city, country_code, lang)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_forecast_climate_lang_missing(params):
    start = time.perf_counter()
    city, country_code = params # lang optional
    logger.info(f"Testing forecast climate for ({city}, {country_code}) with missing lang")
    response = get_forecast_climate_lang (city, country_code, None)
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200








from weather_app.weather import get_weather
import logging
import time
import json


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

def test_weather_api_response_status(coordinates):
    lat, lon = coordinates
    start = time.perf_counter()
    logger.info(f"Testing weather api for ({lat}, {lon})")
    response = get_weather("Kyiv")
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    assert response.status_code == 200

def test_weather_api_response_content(coordinates):
    lat, lon = coordinates
    start = time.perf_counter()
    logger.info(f"Testing weather api response for ({lat}, {lon})")
    response = get_weather("Kyiv")
    duration = (time.perf_counter() - start) * 1000
    logger.info(f"Responce status: {response.status_code}, time: {duration:.2f}")
    data = response.json()
    if response.status_code == 200:
        # logger.info(f"Response JSON keys: {list(response.json().keys())}") #виводить тільки ключі верхнього рівня
        logger.info("Full Response JSON:\n" + json.dumps(data, indent=2, ensure_ascii=False))  # виводить весь json
    assert 'main' in data
    assert 'temp' in data['main']
    assert 'feels_like' in data['main']
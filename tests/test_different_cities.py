import pytest
from weather_app.weather import get_forecast_five_units
from weather_app.weather import get_pollution
from weather_app.weather import get_forecast_five


test_cities = [
    ("Kyiv", (50.450001, 30.523333)),
    ("London", (51.507351, -0.127758)),
    ("Tokyo", (35.689487, 139.691711)),
]

@pytest.mark.parametrize("city,coordinates", test_cities)
def test_hourly_five(city,coordinates):
    lat, lon = coordinates
    response = get_forecast_five(lat, lon)
    assert response.status_code == 200, f"Failed for {city}"

@pytest.mark.parametrize("city,coordinates", test_cities)
def test_hourly_five_units(city, coordinates):
    lat, lon = coordinates
    response = get_forecast_five_units(lat, lon)
    assert response.status_code == 200, f"Failed for {city}"

@pytest.mark.parametrize("city,coordinates", test_cities)
def test_pollution(city, coordinates):
    lat, lon = coordinates
    response = get_pollution(lat, lon)
    assert response.status_code == 200, f"Failed for {city}"
    assert response.json() is not None
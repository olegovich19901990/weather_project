import pytest
import requests

from weather_app.weather import get_forecast_five

@pytest.fixture
def forecast_response():
    response = get_forecast_five(50.45, 30.52)
    yield response                                       #fixture returns the response object

@pytest.fixture
def coordinates():
    return (50, 30)

@pytest.fixture
def coordinates():
    return (50.45, 30.52)
from datetime import datetime
from unittest.mock import patch

import pytest

from src.domain.weather_service import get_lat_long_from_postcode, WeatherService


def test_get_lat_long_from_postcode_success(mock_postcode_response):
    with patch("requests.get", return_value=mock_postcode_response):
        lat, long = get_lat_long_from_postcode("CO27LR")
        assert lat == 12.1
        assert long == 13.2


def test_get_lat_long_from_postcode_error(mock_postcode_response):
    mock_postcode_response.status_code = 400
    with patch("requests.get", return_value=mock_postcode_response):
        with pytest.raises(Exception):
            get_lat_long_from_postcode("LS178RS")


@patch("domain.weather_service.get_lat_long_from_postcode")
@patch("domain.weather_service.requests.get")
def test_get_daily_temperature_avg(mock_get, mock_lat_long, mock_weather_response):
    mock_get.return_value = mock_weather_response
    mock_lat_long.return_value = (51.5074, 0.1278)

    postcode = "CH624SX"
    delivery_date = datetime(2023, 4, 1)
    mock_key = "mock_key"
    ws = WeatherService(mock_key)
    avg_daily_temp = ws.get_daily_temperature_avg(postcode, delivery_date)

    assert avg_daily_temp == 10.0
    mock_get.assert_called_once_with(
        "https://meteostat.p.rapidapi.com/point/daily",
        headers={
            "X-RapidAPI-Key": mock_key,
            "X-RapidAPI-Host": "meteostat.p.rapidapi.com",
        },
        params={"lat": 51.5074, "lon": 0.1278, "start": "2023-04-01", "end": "2023-04-01"},
    )

import pytest
from unittest.mock import patch
from api_client import APIClient

@pytest.fixture
def api_client():
    return APIClient(api_key="fake_api_key")

@patch("requests.get")
def test_fetch_weather_data_success(mock_get, api_client):
    mock_response = {
        "main": {"temp": 295.15},
        "weather": [{"id": 800, "description": "clear sky"}]
    }
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_response

    result = api_client.fetch_weather_data("London")
    assert result == mock_response

@patch("requests.get")
def test_fetch_weather_data_failure(mock_get, api_client):
    mock_get.return_value.status_code = 404
    mock_get.side_effect = RuntimeError("API request failed")

    with pytest.raises(RuntimeError, match="API request failed"):
        api_client.fetch_weather_data("UnknownCity")

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

@patch("requests.get")
def test_fetch_weather_forecast_success(mock_get, api_client):
    # Mocked response data for forecast
    mock_forecast_response = {
        "list": [
            {
                "dt": 1609459200,  # Example timestamp (Jan 1, 2021)
                "main": {"temp": 298.15},
                "weather": [{"id": 800, "description": "clear sky"}]
            }
        ]
    }
    # Mock the API response for successful forecast data fetch
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = mock_forecast_response

    # Call the method and assert the result
    result = api_client.fetch_weather_forecast("London")
    assert result == mock_forecast_response
    mock_get.assert_called_once_with("https://api.openweathermap.org/data/2.5/forecast?q=London&appid=fake_api_key")


@patch("requests.get")
def test_fetch_weather_forecast_failure(mock_get, api_client):
    # Mock the API failure response for forecast
    mock_get.return_value.status_code = 404
    mock_get.side_effect = RuntimeError("Failed to fetch weather forecast")

    # Test that a RuntimeError is raised when the forecast API request fails
    with pytest.raises(RuntimeError, match="Failed to fetch weather forecast"):
        api_client.fetch_weather_forecast("UnknownCity")
    
    # Ensure that the API request was made with the correct URL
    mock_get.assert_called_once_with("https://api.openweathermap.org/data/2.5/forecast?q=UnknownCity&appid=fake_api_key")
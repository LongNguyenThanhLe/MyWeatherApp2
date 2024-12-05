import requests

class APIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5"

    def fetch_weather_data(self, city: str):
        try:
            url = f"{self.base_url}/weather?q={city}&appid={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

    def fetch_weather_forecast(self, city: str):
        try:
            url = f"{self.base_url}/forecast?q={city}&appid={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Failed to fetch weather forecast: {e}")

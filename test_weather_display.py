from weather_display import WeatherDisplay

def test_format_temperature():
    assert WeatherDisplay.format_temperature(300.15) == "81°F"
    assert WeatherDisplay.format_temperature(273.15) == "32°F"

def test_get_weather_emoji():
    assert WeatherDisplay.get_weather_emoji(800) == "☀"
    assert WeatherDisplay.get_weather_emoji(500) == "🌧"
    assert WeatherDisplay.get_weather_emoji(781) == "🌪"
    assert WeatherDisplay.get_weather_emoji(999) == ""

from datetime import datetime
class WeatherDisplay:
    @staticmethod
    def format_temperature(temp_k):
        temp_f = (temp_k * 9/5) - 459.67
        return f"{temp_f:.0f}°F"

    @staticmethod
    def get_weather_emoji(weather_id):
        if 200 <= weather_id <= 232:
            return "⛈"
        elif 300 <= weather_id <= 321:
            return "🌦"
        elif 500 <= weather_id <= 531:
            return "🌧"
        elif 600 <= weather_id <= 622:
            return "❄"
        elif 701 <= weather_id <= 741:
            return "🌫"
        elif weather_id == 762:
            return "🌋"
        elif weather_id == 771:
            return "💨"
        elif weather_id == 781:
            return "🌪"
        elif weather_id == 800:
            return "☀"
        elif 801 <= weather_id <= 804:
            return "☁"
        else:
            return ""

    @staticmethod
    def format_forecast(forecast_data):
        forecast_list = forecast_data.get("list", [])
        formatted_forecast = []
        for forecast in forecast_list[:96]:  # Get 4 days (96 hours)
            timestamp = datetime.utcfromtimestamp(forecast["dt"]).strftime('%Y-%m-%d %H:%M')
            temp = WeatherDisplay.format_temperature(forecast["main"]["temp"])
            weather_id = forecast["weather"][0]["id"]
            emoji = WeatherDisplay.get_weather_emoji(weather_id)
            description = forecast["weather"][0]["description"]
            formatted_forecast.append(f"{timestamp}: {temp}, {emoji}, {description}")
        return formatted_forecast
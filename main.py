import sys
import requests
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout)
from PyQt5.QtCore import Qt

# APIClient class handles all API-related logic
class APIClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"

    def fetch_weather_data(self, city: str):
        try:
            url = f"{self.base_url}?q={city}&appid={self.api_key}"
            response = requests.get(url)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"API request failed: {e}")

# WeatherDisplay class manages weather formatting and presentation
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

# Main WeatherApp class
class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient(api_key="Your API key here")
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        # Create UI elements
        self.city_label = QLabel("Enter city name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)

        # Layout setup
        vbox = QVBoxLayout()
        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        self.setLayout(vbox)

        # Center alignments and styling
        for widget in [self.city_label, self.city_input, self.temperature_label, self.emoji_label, self.description_label]:
            widget.setAlignment(Qt.AlignCenter)
        self.apply_styles()

        # Connect button to action
        self.get_weather_button.clicked.connect(self.get_weather)

    def apply_styles(self):
        self.setStyleSheet("""
            QLabel, QPushButton{
                font-family: calibri;
            }
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 40px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
                font-family: Segoe UI emoji;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)

    def get_weather(self):
        city = self.city_input.text()
        try:
            data = self.api_client.fetch_weather_data(city)
            self.display_weather(data)
        except RuntimeError as e:
            self.display_error(str(e))

    def display_weather(self, data):
        temp_k = data["main"]["temp"]
        weather_id = data["weather"][0]["id"]
        description = data["weather"][0]["description"]

        self.temperature_label.setText(WeatherDisplay.format_temperature(temp_k))
        self.emoji_label.setText(WeatherDisplay.get_weather_emoji(weather_id))
        self.description_label.setText(description)

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px;")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec_())

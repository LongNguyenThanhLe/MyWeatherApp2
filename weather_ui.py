from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout
from PyQt5.QtCore import Qt
from api_client import APIClient
from weather_display import WeatherDisplay

class WeatherUI(QWidget):
    def __init__(self, api_key):
        super().__init__()
        self.api_client = APIClient(api_key)
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

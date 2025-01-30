import sys
from PyQt5.QtWidgets import QApplication
from weather_ui import WeatherUI

if __name__ == "__main__":
    API_KEY = "e9e55e1faf5debbff2273e9422ff5651"

    app = QApplication(sys.argv)
    weather_app = WeatherUI(api_key=API_KEY)
    weather_app.show()
    sys.exit(app.exec_())

import requests
import os
from dotenv import load_dotenv

class Weather:
    def __init__(self):
        load_dotenv()
        self.key = os.getenv("WEATHER_API_KEY")
        self.base_url = "http://api.weatherapi.com/v1/current.json"

    def get(self, city):
        if not city:
            return {"error": "Por favor, proporciona una ciudad válida."}
        try:
            params = {"key": self.key, "q": city, "aqi": "no"}
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return {
                "temperatura": f"{data['current']['temp_c']} grados celsius",
                "condicion": data["current"]["condition"]["text"],
            }
        except requests.exceptions.RequestException:
            return {"error": "No se pudo obtener el clima. Verifica tu conexión o intenta más tarde."}

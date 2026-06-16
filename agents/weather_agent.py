# agents/weather_agent.py

import requests
from config import OPENWEATHER_API_KEY, YOUR_CITY

def get_weather(city: str = None) -> str:
    city = city or YOUR_CITY
    url  = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    
    try:
        data = requests.get(url, timeout=5).json()
        
        if data.get("cod") != 200:
            return f"Sorry, I couldn't fetch weather for {city}."
        
        temp        = round(data["main"]["temp"])
        feels_like  = round(data["main"]["feels_like"])
        description = data["weather"][0]["description"]
        humidity    = data["main"]["humidity"]
        city_name   = data["name"]
        
        return (
            f"Currently in {city_name}, it's {temp} degrees celsius, "
            f"{description}. Feels like {feels_like} degrees. "
            f"Humidity is {humidity} percent."
        )
    except Exception as e:
        return f"Weather service unavailable. Error: {e}"
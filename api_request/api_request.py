import requests

api_key = "9a013a55e86aa0ccce9f52d444b5dba9"
api_url = f"http://api.weatherstack.com/current?access_key={api_key}&query=New York"

# def fetch_data():
#     print("Fetching weather data from weatherstack API...")
#     try:
#         response = requests.get(api_url)
#         response.raise_for_status()
#         print("API response received successfully")
#         return response.json()
#     except requests.exceptions.RequestException as e:
#         print(f"An error occured: {e}")
#         raise
        
    
# fetch_data()

def mock_fetch_data():
    return {'request': {'type': 'City', 'query': 'New York, United States of America', 'language': 'en', 'unit': 'm'}, 'location': {'name': 'New York', 'country': 'United States of America', 'region': 'New York', 'lat': '40.714', 'lon': '-74.006', 'timezone_id': 'America/New_York', 'localtime': '2025-07-17 00:04', 'localtime_epoch': 1752710640, 'utc_offset': '-4.0'}, 'current': {'observation_time': '04:04 AM', 'temperature': 28, 'weather_code': 116, 'weather_icons': ['https://cdn.worldweatheronline.com/images/wsymbols01_png_64/wsymbol_0004_black_low_cloud.png'], 'weather_descriptions': ['Partly cloudy'], 'astro': {'sunrise': '05:40 AM', 'sunset': '08:24 PM', 'moonrise': 'No moonrise', 'moonset': '01:04 PM', 'moon_phase': 'Last Quarter', 'moon_illumination': 62}, 'air_quality': {'co': '371.85', 'no2': '49.58', 'o3': '52', 'so2': '16.465', 'pm2_5': '26.455', 'pm10': '26.64', 'us-epa-index': '2', 'gb-defra-index': '2'}, 'wind_speed': 13, 'wind_degree': 231, 'wind_dir': 'SW', 'pressure': 1015, 'precip': 0, 'humidity': 74, 'cloudcover': 75, 'feelslike': 34, 'uv_index': 0, 'visibility': 16, 'is_day': 'no'}}
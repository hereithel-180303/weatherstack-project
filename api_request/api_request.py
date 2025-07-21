import requests

# OpenWeatherMap API configuration
api_key = "fde217ada45edd7be9b06fe510c8dfc6"

def fetch_data():
    """Fetch weather data for multiple Asian cities"""
    asian_cities = [
        "Manila,PH",        # Philippines
        "Tokyo,JP",         # Japan
        "Seoul,KR",         # South Korea
        "Bangkok,TH",       # Thailand
        "Singapore,SG",     # Singapore
        "Kuala Lumpur,MY",  # Malaysia
        "Jakarta,ID",       # Indonesia
        "Mumbai,IN",        # India
        "Beijing,CN",       # China
        "Taipei,TW",        # Taiwan
        "Ho Chi Minh City,VN", # Vietnam
        "Dhaka,BD",         # Bangladesh
    ]
    
    print("Fetching weather data from OpenWeatherMap API for Asian cities...")
    weather_data = []
    
    for city in asian_cities:
        try:
            api_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
            print(f"Fetching weather data for {city}...")
            
            response = requests.get(api_url)
            response.raise_for_status()
            
            data = response.json()
            weather_data.append(data)
            print(f"✓ Data received for {data['name']}, {data['sys']['country']}")
            
        except requests.exceptions.RequestException as e:
            print(f"✗ Error fetching data for {city}: {e}")
            continue
    
    print(f"API response received successfully - {len(weather_data)} cities")
    return weather_data

# Example usage
data = fetch_data()
print(f"\nFetched weather data for {len(data)} Asian cities:")
for city_data in data:
    print(f"- {city_data['name']}, {city_data['sys']['country']}: {city_data['main']['temp']}°C, {city_data['weather'][0]['description']}")

# # Mock data function with OpenWeatherMap format (for testing)
# def mock_fetch_data():
#     return {
#         "coord": {"lon": -74.006, "lat": 40.7143},
#         "weather": [
#             {
#                 "id": 803,
#                 "main": "Clouds",
#                 "description": "broken clouds",
#                 "icon": "04n"
#             }
#         ],
#         "base": "stations",
#         "main": {
#             "temp": 28.5,
#             "feels_like": 34.2,
#             "temp_min": 26.8,
#             "temp_max": 30.1,
#             "pressure": 1015,
#             "humidity": 74
#         },
#         "visibility": 16000,
#         "wind": {
#             "speed": 3.6,  # m/s (converted from weatherstack's 13 km/h)
#             "deg": 231
#         },
#         "clouds": {"all": 75},
#         "dt": 1721174640,
#         "sys": {
#             "type": 2,
#             "id": 2039034,
#             "country": "US",
#             "sunrise": 1721124000,
#             "sunset": 1721176440
#         },
#         "timezone": -14400,
#         "id": 5128581,
#         "name": "New York",
#         "cod": 200
#     }

# # Helper function to map between the APIs (optional)
# def convert_to_weatherstack_format(openweather_data):
#     """Convert OpenWeatherMap response to weatherstack-like format for easier migration"""
#     try:
#         return {
#             "location": {
#                 "name": openweather_data["name"],
#                 "country": openweather_data["sys"]["country"],
#                 "lat": str(openweather_data["coord"]["lat"]),
#                 "lon": str(openweather_data["coord"]["lon"])
#             },
#             "current": {
#                 "temperature": int(openweather_data["main"]["temp"]),
#                 "weather_descriptions": [openweather_data["weather"][0]["description"]],
#                 "wind_speed": int(openweather_data["wind"]["speed"] * 3.6),  # Convert m/s to km/h
#                 "wind_degree": openweather_data["wind"]["deg"],
#                 "pressure": openweather_data["main"]["pressure"],
#                 "humidity": openweather_data["main"]["humidity"],
#                 "feelslike": int(openweather_data["main"]["feels_like"]),
#                 "visibility": openweather_data["visibility"] // 1000,  # Convert m to km
#                 "cloudcover": openweather_data["clouds"]["all"]
#             }
#         }
#     except KeyError as e:
#         print(f"Error converting data format: {e}")
#         return openweather_data
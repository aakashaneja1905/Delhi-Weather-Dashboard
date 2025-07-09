import requests
import pandas as pd

API_KEY = 'VMXMQG5ED8GG62559Q2HYLADB'
CITY = 'Delhi'
START_DATE = '2024-07-01'
END_DATE = '2025-07-01'

url = f'https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{CITY}/{START_DATE}/{END_DATE}?unitGroup=metric&include=days&key={API_KEY}&contentType=json'

response = requests.get(url)
data = response.json()

# Cleaned daily weather data
weather_data = []

for day in data.get('days', []):
    if all(k in day for k in ['temp', 'humidity', 'windspeed']):  # filter out incomplete rows
        weather_data.append({
            'Date': day['datetime'],
            'TempAvg_C': round(day.get('temp', 0), 1),
            'TempMax_C': round(day.get('tempmax', 0), 1),
            'TempMin_C': round(day.get('tempmin', 0), 1),
            'Humidity_%': round(day.get('humidity', 0)),
            'Precip_mm': round(day.get('precip', 0), 2),
            'Wind_kph': round(day.get('windspeed', 0), 1),
            'Conditions': day.get('conditions', 'Unknown')
        })

# Create DataFrame
df = pd.DataFrame(weather_data)

# Final cleaning
df.dropna(inplace=True)
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values('Date', inplace=True)

# Save to CSV
df.to_csv('delhi_weather_1year_cleaned.csv', index=False)
print("✅ Cleaned file saved: delhi_weather_1year_cleaned.csv")

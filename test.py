import requests

res = requests.get("https://api.weather.gov/points/39.7456,-97.0892").json()
forecast_url = res["properties"]["forecast"]
print(forecast_url)

forecast_res = requests.get(forecast_url).json()
print(forecast_res)

clean_periods = []
for period in forecast_res["properties"]["periods"]:
    clean_periods.append({
        "start_time":period["startTime"],
        "end_time":period["endTime"],
        "temperature":period["temperature"],
        "precipitation_probability":period["probabilityOfPrecipitation"]["value"],
        "wind_speed":period["windSpeed"],
        "short_forecast":period["shortForecast"]
    })

print(clean_periods)
import requests
state_abbreviation = "FL"

res = requests.get(f"https://api.weather.gov/alerts/active?area={state_abbreviation}").json()

#Clean up the data. Mainly for context limiting.
alerts = []
for record in res["features"]:
    alerts.append({
        "geometry":record["geometry"],
        "effective_date":record["properties"]["effective"],
        "expires_date":record["properties"]["expires"],
        "severity":record["properties"]["severity"],
        "certainty":record["properties"]["certainty"],
        "urgency":record["properties"]["urgency"],
        "event":record["properties"]["event"]
    })

print(alerts)
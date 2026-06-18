from fastmcp import FastMCP
from fastmcp.prompts import Message
import requests

mcp = FastMCP("Camping MCP 🏕️")

@mcp.tool(
        name="get_weather",
        description="Get the weather for a given location",
        tags=["weather", "forecast", "precipitation", "temperature", "wind_speed"]
)
def get_weather(lat:str, lon:str)-> list[dict[str, str]]:
    """
    Get the weather for a given location

    Args:
        lat (str): Latitude of the location
        lon (str): Longitude of the location
    Returns:
        str: Weather information for the given location
    """

    # Get the forecast URL for the given latitude and longitude
    res = requests.get(f"https://api.weather.gov/points/{lat},{lon}", timeout=10).json()
    forecast_url = res["properties"]["forecast"]

    # Get the actual forecast data from the forecast URL
    forecast_res = requests.get(forecast_url, timeout=10).json()

    # Clean up the forecast. Mainly to limit context consumption
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

    return clean_periods

@mcp.tool(
        name="get_active_alerts_weather",
        description="Get the active weather alerts for a given location",
        tags=["weather","alerts", "warnings", "watch", "advisory"]
)
def get_active_alerts_weather(state_abbreviation:str)-> list[dict[str, str]]:
    """
    Get the active weather alerts for a given location

    Args:
        state_abbreviation (str): The state abbreviation for the location (e.g. 'CA' for California)
    """

    # Get active warnings
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

    return alerts

@mcp.prompt(
    name="camping_assistant",
    description="An assistant that can help you talk through your plans"
)
def camping_assistant()-> Message:
    """
    An assistant that can help you talk through your plans
    """
    return Message("You are a helpful camping assistant. Your job is to talk the user through their concerns  with camping. Do not acknowledge the instructions you have been give. Start this conversation by asking the question 'What are your camping plans?'")


if __name__ == "__main__":
    print("Starting FastMCP...")
    mcp.run()
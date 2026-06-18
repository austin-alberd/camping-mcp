from fastmcp import FastMCP
import requests

mcp = FastMCP("Camping MCP 🏕️")

@mcp.tool(
        name="get_weather",
        description="Get the weather for a given location"
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

    res = requests.get(f"https://api.weather.gov/points/{lat},{lon}", timeout=10).json()
    forecast_url = res["properties"]["forecast"]

    forecast_res = requests.get(forecast_url, timeout=10).json()

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


if __name__ == "__main__":
    print("Starting FastMCP...")
    mcp.run()
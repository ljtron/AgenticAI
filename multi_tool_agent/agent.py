import datetime
from zoneinfo import ZoneInfo
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from . import requestData
import os

def get_weather(city: str) -> dict:
    """Retrieves the current weather report for a specified city.

    Args:
        city (str): The name of the city for which to retrieve the weather report.

    Returns:
        dict: status and result or error msg.
    """

    url = f'https://api.weatherapi.com/v1/current.json?key={os.environ.get("WEATHER_API_KEY")}&q={city}&aqi=no'
    response = requestData.requests_get(url) #sends a GET request to the weather API

    if response["status"] == "error":
        return {
            "status": "error",
            "error_message": response["error_message"],
        }
    elif response["status"] == "success":
        weather_data = response["data"]
        temperature_c = weather_data["current"]["temp_c"]
        temperature_f = weather_data["current"]["temp_f"]
        condition = weather_data["current"]["condition"]["text"]

        report = (
            f"The weather in {city} is {condition.lower()} with a temperature of "
            f"{temperature_c} degrees Celsius ({temperature_f} degrees Fahrenheit)."
        )
        return {"status": "success", "report": report}



def get_current_time(city: str) -> dict:
    """Returns the current time in a specified city.

    Args:
        city (str): The name of the city for which to retrieve the current time.

    Returns:
        dict: status and result or error msg.
    """

    # retrieving the coordinates of the city
    get_coordinates_header = {'X-Api-Key': os.environ.get("API_NINJA_KEY")}
    get_coordinates_url = f"https://api.api-ninjas.com/v1/geocoding?city={city}"
    get_coordinates = requestData.requests_get(get_coordinates_url, headers=get_coordinates_header)
    if get_coordinates["status"] == "error":
        return {
            "status": "error",
            "error_message": (get_coordinates["error_message"]),
        }
    
    # retrieving the current time using the coordinates
    get_time_header = {'X-Api-Key': os.environ.get("API_NINJA_KEY")}
    get_time_url = f"https://api.api-ninjas.com/v1/worldtime?lat={get_coordinates['data'][0]['latitude']}&lon={get_coordinates['data'][0]['longitude']}"
    get_time = requestData.requests_get(get_time_url, headers=get_time_header)
    if get_time["status"] == "error":
        return {
            "status": "error",
            "error_message": (get_time["error_message"]),
        }
    else:
        get_time_date = get_time["data"]["date"] # date in ISO format
        get_time_hour = get_time["data"]["hour"] # hour in 24-hour format
        get_time_minute = get_time["data"]["minute"] # the current minute
        report = (
            f"The current time in {city} is {get_time_hour}:{get_time_minute} and the date is {get_time_date}."
        )
        return {"status": "success", "report": report}
        


root_agent = Agent(
    name="weather_time_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent to answer questions about the time and weather in a city."
    ),
    instruction=(
        "You are a helpful agent who can answer user questions about the time and weather in a city."
    ),
    tools=[get_weather, get_current_time],
)


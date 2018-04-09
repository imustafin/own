"""
This script prints weather to a json file
in the script directory (not working directory).
"""
import json
import os
from typing import Dict, List, NewType

import requests

CityId = NewType('CityId', str)  # Openweathermap city ID

API_KEY = 'dfc4baa177a7d9399db4093cf930499c'
API_BASE = 'http://api.openweathermap.org/data/2.5/'

# From bulk.openweathermap.org/sample/city.list.json.gz
# By API docs, API clients should use city IDs and not search by names
CITY_ID: Dict[str, CityId] = {
    'London': CityId('2643743'),
    'Kazan': CityId('551487'),
    'Moscow': CityId('524901'),
}


def current_severalid(city_ids: List[CityId]) -> Dict:
    """/current/severalid API request for current weather in cities by IDs.

    Current weather data for multiple cities by their IDs.
    API doc:
    http://www.openweathermap.com/current#severalid

    Parameters
    ----------
    city_ids : List[CityId]
        IDs of the cities for which data should be retrieved.

    Returns
    -------
    Dict
        API response
    """
    params = {'id': ','.join(city_ids), 'units': 'metric', 'appid': API_KEY}
    response = requests.get(API_BASE + 'group', params=params)
    return response.json()


def weather_data_for(city_ids: List[CityId]) -> str:
    """Current weather in a pretty JSON string by city ids.

    Current weather data for multiple cities by their ids in a custom JSON.

    Parameters
    ----------
    city_ids : List[CityId]
        IDs of the cities for which data should be retrieved.

    Returns
    -------
    str
        Pretty JSON string with weather data
    """
    data = current_severalid(city_ids)
    cities = []
    for city in data['list']:
        cities.append({
            'cityName': city['name'],
            'degreesCelsius': city['main']['temp']
        })
    ans = {'weatherData': cities}
    return json.dumps(ans, indent=2, sort_keys=True)


if __name__ == '__main__':
    required_city_names = ['London', 'Moscow', 'Kazan']
    data = weather_data_for([CITY_ID[x] for x in required_city_names])

    path = os.path.dirname(os.path.realpath(__file__)) + '/result.json'
    with open(path, 'w') as output:
        print(data, file=output)


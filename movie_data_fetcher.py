import requests
import os
from dotenv import load_dotenv
from models import Movie
from data_manager import DataManager

load_dotenv()
API_KEY = os.getenv('API_KEY')

BASE_URL = "http://www.omdbapi.com/"

def fetch_data(title: str, year: str = None):
    """Fetch movie information from the OMDb API.

    Args:
        title (str): The title of the movie to search for.
        year (str, optional): The release year of the movie. Defaults to None.

    Returns:
        dict or None: A dictionary containing movie information if found,
        otherwise `None`.

    Raises:
        Exception: If the API request fails with a non-200 status code.
    """
    params = {
        'apikey': API_KEY,
        't': title,
        'type': 'movie'
    }

    if year:
        params['y'] = year

    response = requests.get(BASE_URL, params=params)
    if response.status_code == requests.codes.ok:
        data = response.json()
        if data.get('Response') == 'True':
            return data
        else:
            print(f"Couldn't find Movie: {data.get('Error', 'Unknown error')}")
            return None
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")

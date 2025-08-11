import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('API_KEY')

BASE_URL = "http://www.omdbapi.com/"

def fetch_data(title: str, year: str = None, timeout: float = 10.0):
    """Fetch movie information from the OMDb API with timeout support.

    Args:
        title (str): The title of the movie to search for.
        year (str, optional): The release year of the movie. Defaults to None.
        timeout (float, optional): Maximum time in seconds to wait for the request.
                                   Defaults to 10.0 seconds.

    Returns:
        dict or None: A dictionary containing movie information if found,
        otherwise `None`.

    Raises:
        Exception: If the API request fails with a non-200 status code or timeout.
    """
    params = {
        'apikey': API_KEY,
        't': title,
        'type': 'movie'
    }

    if year:
        params['y'] = year

    try:
        response = requests.get(BASE_URL, params=params, timeout=timeout)
        response.raise_for_status()  # Wirft Exception für HTTP-Fehlerstatuscodes

        data = response.json()
        if data.get('Response') == 'True':
            return data

        print(f"Couldn't find Movie: {data.get('Error', 'Unknown error')}")
        return None

    except requests.exceptions.Timeout:
        print(f"Request timed out after {timeout} seconds for movie: '{title}'")
        raise Exception(f"API request timed out after {timeout} seconds")

    except requests.exceptions.RequestException as e:
        print(f"Request failed for movie '{title}': {str(e)}")
        raise Exception(f"API request failed: {str(e)}")
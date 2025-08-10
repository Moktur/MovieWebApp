import requests
import os
from dotenv import load_dotenv
from models import Movie


load_dotenv()
API_KEY = os.getenv('API_KEY')


def fetch_data(movie_search):
    """
    Fetches movie information from API.
    Returns a dictionary with the requested movie information.
    """
    api_url = f'http://www.omdbapi.com/?t={movie_search}'
    response = requests.get(api_url, API_KEY)
    if response.status_code == requests.codes.ok:
        data = response.json()
        if data.get('Response') == 'True':
            return data
        else:
            print(f"Couldn't find Movie: {data.get('Error', 'Unknown error')}")
            return None
    else:
        raise Exception(f"API Error: {response.status_code} - {response.text}")


def get_information_for_all_movies(movielist):
    movie_object_list = []
    for movie in movielist:
        movie = Movie()

from unittest import TestCase

import requests

from api_tests.config import MOVIES, BASE_URL, USERS
from api_tests.helpers import create_user, create_movie, clear_db

class TestMovies(TestCase):
    def test_create_movie(self):
        clear_db(['users', 'movies'])
        token = create_user(data=USERS[0])
        response = create_movie(MOVIES[0], token)
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data.get('title'), MOVIES[0].get('title'))

    def test_get_movies(self):
        clear_db(['users', 'movies'])
        token = create_user(data=USERS[0])
        movies = []
        for i in MOVIES:
            resp = create_movie(data=i, token=token)
            movies.append(resp.json())
            self.assertEqual(resp.status_code, 200)

        get_response = requests.get(f'{BASE_URL}/movies', headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(get_response.status_code, 200)
        self.assertEqual(get_response.json(), movies)
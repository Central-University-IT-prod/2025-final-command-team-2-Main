from unittest import TestCase

import requests
from api_tests.config import BASE_URL, USERS


class TestUser(TestCase):
    def test_create_user(self):
        response = requests.post(f'{BASE_URL}/auth/telegram', json=USERS[0])
        user_data = response.json()
        self.assertIs(response.status_code, 200)

    def test_get_user_profile(self):
        create_response = requests.post(f'{BASE_URL}/auth/telegram', json=USERS[1])
        user_data = create_response.json()
        token = user_data.get('token')
        self.assertIs(create_response.status_code, 200)

        get_response = requests.get(f'{BASE_URL}/users/me', headers={'Authorization': f'Bearer {token}'})
        user_data = get_response.json()
        self.assertIs(get_response.status_code, 200)
        self.assertEqual(user_data.get('username'), USERS[1].get('username'))

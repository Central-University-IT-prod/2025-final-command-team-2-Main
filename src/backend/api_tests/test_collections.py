from app.routes.collections import add_movie_to_collection
from api_tests.helpers import *
from unittest import TestCase

from api_tests.config import USERS, MOVIES, COLLECTIONS

class TestCollections(TestCase):
    def test_get_default_collection(self):
        clear_db(['users', 'collections'])
        user1 = USERS[0]
        token1 = create_user(user1)
        response = get_collections(token1)
        collections = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(collections[0].get('isDefault'), True)

    def test_create_collection(self):
        clear_db(['users', 'collections'])
        user = USERS[0]
        token = create_user(user)
        collection = COLLECTIONS[0]
        response = create_collection(collection, token=token)
        response_collection = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response_collection.get('name'), collection.get('name'))
        self.assertEqual(response_collection.get('description'), collection.get('description'))

    def test_get_collections(self):
        clear_db(['users', 'collections'])
        user = USERS[0]
        token = create_user(user)
        collections = []
        for i in COLLECTIONS:
            resp = create_collection(i, token=token)
            self.assertEqual(resp.status_code, 201)
            collections.append(resp.json())
        for i in range(len(collections)):
            self.assertEqual(collections[i].get('name'), COLLECTIONS[i].get('name'))
            self.assertEqual(collections[i].get('description'), COLLECTIONS[i].get('description'))

    def test_delete_collection(self):
        clear_db(['users', 'collections'])
        user = USERS[0]
        token = create_user(user)
        create_response = create_collection(COLLECTIONS[1], token=token)
        collection: dict = create_response.json()
        delete_response = delete_collection(collection.get('id'), token=token)
        self.assertEqual(delete_response.status_code, 204)

        get_response = get_collection(collection_id=collection.get('id'), token=token)
        self.assertEqual(get_response.status_code, 404)

    def test_put_collection(self):
        clear_db(['users', 'collections'])
        user = USERS[0]
        token = create_user(user)
        create_response = create_collection(COLLECTIONS[0], token=token)
        collection_before: dict = create_response.json()

        put_response = put_collection(collection_id=collection_before.get('id'), data=COLLECTIONS[1], token=token)
        collection_after = put_response.json()
        self.assertEqual(put_response.status_code, 200)
        self.assertNotEqual(collection_after, collection_before)

    def test_add_movies_to_collection(self):
        clear_db(['users', 'collections', 'movies'])
        user = USERS[0]
        token = create_user(user)
        create_response = create_collection(COLLECTIONS[0], token=token)
        collection: dict = create_response.json()
        movies = []
        for i in MOVIES:
            resp = create_movie(data=i, token=token)
            movie = resp.json()
            movies.append(movie)
            self.assertEqual(resp.status_code, 200)
            add_movie_response = add_movie_to_collection(
                data={'movieId': movie.get('id')},
                token=token,
                collection_id=collection.get('id')
            )
            self.assertEqual(add_movie_response.status_code, 200)
        get_collection_response = get_collection(token=token, collection_id=collection.get('id'))
        self.assertEqual(get_collection_response.status_code, 200)
        added_movies = get_collection_response.json().get('movies')

        for i in range(len(movies)):
            self.assertEqual(movies[i]['title'], added_movies[i]['title'])
            self.assertEqual(movies[i]['description'], added_movies[i]['description'])

    def test_delete_movie_from_collection(self):
        clear_db(['users', 'collections', 'movies'])
        user = USERS[0]
        token = create_user(user)
        create_response = create_collection(COLLECTIONS[0], token=token)
        collection: dict = create_response.json()
        movies = []
        for i in MOVIES:
            resp = create_movie(data=i, token=token)
            movie = resp.json()
            movies.append(movie)
            self.assertEqual(resp.status_code, 200)
            add_movie_response = add_movie_to_collection(
                data={'movieId': movie.get('id')},
                token=token,
                collection_id=collection.get('id')
            )
            self.assertEqual(add_movie_response.status_code, 200)
        get_collection_response = get_collection(token=token, collection_id=collection.get('id'))
        self.assertEqual(get_collection_response.status_code, 200)
        added_movies = get_collection_response.json().get('movies')

        movie_to_delete = added_movies[0]

        delete_movie_response = delete_movie_from_collection(token=token, collection_id=collection.get('id'),
                                                             movie_id=movie_to_delete.get('id'))
        self.assertEqual(delete_movie_response.status_code, 204)
        get_collection_response = get_collection(token=token, collection_id=collection.get('id'))
        movies = get_collection_response.json().get('movies')

        for i in movies:
            self.assertNotEqual(i.get('title'), movie_to_delete.get('title'))

    def test_add_user_to_collection(self):
        clear_db(['users', 'collections'])
        user1 = USERS[0]
        user2 = USERS[1]
        token = create_user(user1)
        add_user_response = requests.post(f'{BASE_URL}/auth/telegram', json=user2)
        response_user = add_user_response.json()
        token1 = response_user.get('token')
        collection = COLLECTIONS[0]
        response = create_collection(collection, token=token)
        response_collection = response.json()
        self.assertEqual(response.status_code, 201)

        add_user_response = add_user_to_collection(response_collection.get('id'), token=token, data={'userTelegramId': response_user.get('user').get('telegramId')})
        self.assertEqual(add_user_response.status_code, 200)
        get_collection_response = get_collection(response_collection.get('id'), token=token)
        got_users = get_collection_response.json().get('users')
        self.assertEqual(got_users[1].get('telegramId'), user2.get('telegramId'))

        get_collection_response = get_collection(collection_id=response_collection.get('id'), token=token1)
        self.assertEqual(get_collection_response.status_code, 200)

    def test_delete_user_to_collection(self):
        clear_db(['users', 'collections'])
        user1 = USERS[0]
        user2 = USERS[1]
        token = create_user(user1)
        add_user_response = requests.post(f'{BASE_URL}/auth/telegram', json=user2)
        response_user = add_user_response.json()
        token1 = response_user.get('token')
        collection = COLLECTIONS[0]
        response = create_collection(collection, token=token)
        response_collection = response.json()
        self.assertEqual(response.status_code, 201)

        add_user_response = add_user_to_collection(response_collection.get('id'), token=token, data={'userTelegramId': response_user.get('user').get('telegramId')})
        self.assertEqual(add_user_response.status_code, 200)
        get_collection_response = get_collection(response_collection.get('id'), token=token)
        got_users = get_collection_response.json().get('users')
        self.assertEqual(got_users[1].get('telegramId'), user2.get('telegramId'))

        get_collection_response = get_collection(collection_id=response_collection.get('id'), token=token1)
        self.assertEqual(get_collection_response.status_code, 200)

        delete_user_response = delete_user_from_collection(token=token, collection_id=response_collection.get('id'),
                                                           telegram_id=response_user.get('user').get('telegramId'))

        self.assertEqual(delete_user_response.status_code, 204)
        get_collection_response = get_collection(collection_id=response_collection.get('id'), token=token1)
        self.assertEqual(get_collection_response.status_code, 403)













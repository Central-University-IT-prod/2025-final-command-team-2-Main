import os
from dotenv import load_dotenv
load_dotenv()

import requests
from api_tests.config import BASE_URL

def clear_db(tables: list):
    tables = ','.join(tables)
    load_dotenv()
    resp = requests.delete(f'{BASE_URL}/clear_tables?tables={tables}', headers={'Password': '123456'})
    if resp.status_code != 200:
        raise Exception('you have not cleared db')
    return True


def create_user(data):
    response = requests.post(f'{BASE_URL}/auth/telegram', json=data)
    user = response.json()
    return user.get('token')


def create_movie(data, token):
    response = requests.post(f'{BASE_URL}/movies/', json=data, headers={'Authorization': f'Bearer {token}'})
    return response

def create_collection(data, token):
    response = requests.post(f'{BASE_URL}/collections', headers={'Authorization': f'Bearer {token}'}, json=data)
    return response

def get_collections(token):
    response = requests.get(f'{BASE_URL}/collections', headers={'Authorization': f'Bearer {token}'})
    return response

def get_collection(collection_id, token):
    response = requests.get(f'{BASE_URL}/collections/{collection_id}', headers={'Authorization': f'Bearer {token}'})
    return response

def delete_collection(collection_id, token):
    response = requests.delete(f'{BASE_URL}/collections/{collection_id}', headers={'Authorization': f'Bearer {token}'})
    return response

def put_collection(collection_id, data, token):
    response = requests.put(f'{BASE_URL}/collections/{collection_id}', headers={'Authorization': f'Bearer {token}'},
                            json=data)
    return response

def add_movie_to_collection(collection_id, data, token):
    response = requests.post(f'{BASE_URL}/collections/{collection_id}/movies', json=data, headers={'Authorization':
                                                                                                       f'Bearer {token}'})
    return response

def delete_movie_from_collection(collection_id, movie_id, token):
    response = requests.delete(f'{BASE_URL}/collections/{collection_id}/movies/{movie_id}', headers={'Authorization':
                                                                                                       f'Bearer {token}'})

    return response

def add_user_to_collection(collection_id, data, token):
    response = requests.post(f'{BASE_URL}/collections/{collection_id}/users', json=data, headers={'Authorization':
                                                                                                       f'Bearer {token}'})
    return response

def delete_user_from_collection(collection_id, token, telegram_id):
    response = requests.delete(f'{BASE_URL}/collections/{collection_id}/users/{telegram_id}', headers={'Authorization':
                                                                                                       f'Bearer {token}'})
    return response



import pytest
import requests
import random
import string
from data import BASE_URL, USERS_URL, REGISTER_URL, CHANGE_URL


# фикстура создания пользователя со всеми обязат.полями
@pytest.fixture()
def create_and_delete_user():
    # Генерируем уникальные данные для пользователя
    def generate_random_string(length):
        return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
    
    email = generate_random_string(10) + "@mail.ru"
    password = generate_random_string(10)
    name = generate_random_string(10)

    # Регистрация пользователя
    registration_payload = {
        "name": name,
        "email": email,
        "password": password  
    }
    response = requests.post(f'{BASE_URL}{USERS_URL}{REGISTER_URL}', json=registration_payload)
    access_token = response.json().get("accessToken")
    refresh_token = response.json().get("refreshToken")

    yield {
        'success': True,
        'status_code': response.status_code,
        'name': name,
        'email': email,
        'password': password, 
        'access_token': access_token,
        'refresh_token': refresh_token
    }

    # Удаление пользователя после теста
    if access_token:
        headers = {
            'Authorization': access_token 
        }
    delete_response = requests.delete(f'{BASE_URL}{USERS_URL}{CHANGE_URL}', headers=headers)
    delete_response.raise_for_status() # Проверка успешного удаления


# фикстура создания пользователя без какого-либо обязат.поля
@pytest.fixture()
def create_user_no_any_data(params):
    response = requests.post(f'{BASE_URL}{USERS_URL}{REGISTER_URL}', json=params)
    access_token = response.json().get("accessToken")

    yield {
        'success': False,
        'status_code': response.status_code,
        'response_json': response.json(),
        'access_token': access_token
    }


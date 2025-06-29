import requests
import random
import string
import allure
from data import BASE_URL, USERS_URL, REGISTER_URL, LOGIN_URL, CHANGE_URL, LOGOUT_URL

class UsersMethods:

    @allure.step("Создание уникального пользователя, все поля заполнены")
    def create_user(self, params):
        response = requests.post(f'{BASE_URL}{USERS_URL}{REGISTER_URL}', data=params)
        return response.json(), response.status_code
    
    @allure.step("Авторизация пользователя")
    def user_login(self, params):
        response = requests.post(f'{BASE_URL}{USERS_URL}{LOGIN_URL}', data=params)
        return response.json(), response.status_code
        #return response.json(), response.status_code, response.json().get('"accessToken')

    @allure.step("Изменение данных пользователя")
    def change_user_data(self, headers, params):
        response = requests.patch(f'{BASE_URL}{USERS_URL}{CHANGE_URL}', headers=headers, json=params)
        return response.json(), response.status_code, response.json().get('user')

    # ЭТОТ МЕТОД НУЖЕН???
    @allure.step("Выход из системы")
    def exit_from_account(self, params):
        response = requests.post(f'{BASE_URL}{USERS_URL}{LOGOUT_URL}', data=params)
        return response.json(), response.status_code






    @staticmethod
    def generate_user_data_all_fields():
        # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string

        # генерируем email, пароль и имя пользователя
        email = generate_random_string(10) + "@mail.ru"
        password = generate_random_string(10)
        name = generate_random_string(10)
        return {
        "email": email,
        "password": password,
        "name": name
        }
    
    # ЭТОТ МЕТОД НУЖЕН???
    @staticmethod
    def generate_courier_data_without_name():
        # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
        def generate_random_string(length):
            letters = string.ascii_lowercase
            random_string = ''.join(random.choice(letters) for i in range(length))
            return random_string
        
        # генерируем логин и пароль
        login = generate_random_string(10)
        password = generate_random_string(10)
        return {
        "login": login,
        "password": password,
        }
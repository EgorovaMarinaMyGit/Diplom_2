import requests
import random
import string
import allure
from data import BASE_URL, ORDERS_URL, INGREDIENTS_URL


class OrderMethods:

    @allure.step("Создание заказа")
    def create_order(self, headers, params):
        response = requests.post(f'{BASE_URL}{ORDERS_URL}', headers=headers, json=params)
        response_json = response.json()
        owner_data = response_json.get('order', {}).get('owner')
        return response_json, response.status_code, owner_data, response_json.get('order', {}).get('_id')
    
    @allure.step("Получение хеша ингредиентов")
    def get_ids_of_ingredient(self):
        response = requests.get(f'{BASE_URL}{INGREDIENTS_URL}')
        json_response = response.json()
        data_list = json_response.get("data", [])
    
        if len(data_list) >= 2:
            first_id = data_list[0]["_id"]
            second_id = data_list[1]["_id"]
            return first_id, second_id
        else:
        # Обработка случая, когда элементов меньше 2
            return None, None
        
    @allure.step("Создание заказа с некорректным хэшем ингредиентов")
    def create_order_with_incorrect_ids(self, headers, params):
        response = requests.post(f'{BASE_URL}{ORDERS_URL}', headers=headers, json=params)
        return response.status_code
    
    @allure.step("Получение заказа пользователя")
    def get_order_of_user(self, headers):
        response = requests.get(f'{BASE_URL}{ORDERS_URL}', headers=headers)
        response_json = response.json()
        orders = response_json.get("orders", [])
        order_id = None
        if orders:
            order_id = orders[0].get('_id')
        return response_json, response.status_code, order_id

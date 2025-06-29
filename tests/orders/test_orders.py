import allure
from methods.order_methods import OrderMethods


class TestOrders:

    @allure.title("Создание заказа с авторизацией и корректным хэшем ингредиентов")
    def test_create_order_with_autorisation_and_correct_ingredients(self, create_and_delete_user):
        user = create_and_delete_user
        headers = {
            'Authorization': user['access_token'] 
        }
        order = OrderMethods()
        first_id, second_id = order.get_ids_of_ingredient()
        params = {
            "ingredients": [first_id, second_id]
        }
        response_json, status_code, owner, order_id = order.create_order(headers, params)
        assert status_code == 200 and owner['email'] == user['email'] and owner['name'] == user['name']


    @allure.title("Создание заказа без авторизации и с корректным хэшем ингредиентов")
    def test_create_order_without_autorisation_with_correct_ingredients(self, create_and_delete_user):
        user = create_and_delete_user
        headers = None
        order = OrderMethods()
        first_id, second_id = order.get_ids_of_ingredient()
        params = {
            "ingredients": [first_id, second_id]
        }
        response_json, status_code, owner, id = order.create_order(headers, params)
        assert status_code == 200 and 'email' not in response_json.get('order', {}) and 'name' not in response_json.get('order', {})


    @allure.title("Создание заказа с авторизацией и без ингридиентов")
    def test_create_order_with_autorisation_without_ingredients(self, create_and_delete_user):
        user = create_and_delete_user
        headers = {
            'Authorization': user['access_token'] 
        }
        order = OrderMethods()
        params = {
            "ingredients": []
        }
        response_json, status_code, owner, id = order.create_order(headers, params)
        message = "Ingredient ids must be provided"
        assert status_code == 400 and response_json["message"] == message


    @allure.title("Создание заказа без авторизации и без ингредиентов")
    def test_create_order_without_autorisation(self, create_and_delete_user):
        user = create_and_delete_user
        headers = None
        order = OrderMethods()
        params = {
            "ingredients": []
        }
        response_json, status_code, owner, id = order.create_order(headers, params)
        message = "Ingredient ids must be provided"
        assert status_code == 400 and response_json["message"] == message


    @allure.title("Создание заказа с авторизацией и некорректным хэшем ингредиентов")
    def test_create_order_with_autorisation_and_incorrect_ingredients(self, create_and_delete_user):
        user = create_and_delete_user
        headers = {
            'Authorization': user['access_token'] 
        }
        order = OrderMethods()
        params = {
            "ingredients": ["gd7g67", "fdsuyfuef76"]
        }
        status_code = order.create_order_with_incorrect_ids(headers, params)
        assert status_code == 500


    @allure.title("Создание заказа с авторизацией и некорректным хэшем ингредиентов")
    def test_create_order_without_autorisation_and_incorrect_ingredients(self, create_and_delete_user):
        user = create_and_delete_user
        headers = None
        order = OrderMethods()
        params = {
            "ingredients": ["gd7g656567", "fdsuyfuef6565676"]
        }
        status_code = order.create_order_with_incorrect_ids(headers, params)
        assert status_code == 500

   
    @allure.title("Получение заказа пользователя, с авторизацией")
    def test_get_order_of_user_with_autorisation(self, create_and_delete_user):
        user = create_and_delete_user
        headers = {
            'Authorization': user['access_token'] 
        }
        order = OrderMethods()
        first_id, second_id = order.get_ids_of_ingredient()
        params = {
            "ingredients": [first_id, second_id]
        }
        response_json, status_code, owner, _id = order.create_order(headers, params)
        id_posted_order = _id
        response_json, status_code, _id = order.get_order_of_user(headers)
        id_order_of_user = _id
        assert id_posted_order == id_order_of_user


    @allure.title("Получение заказа пользователя, без авторизации")
    def test_get_order_of_user_without_autorisation(self):
        order = OrderMethods()
        headers = None
        response_json, status_code, id = order.get_order_of_user(headers)
        message = "You should be authorised"
        assert status_code == 401 and response_json["message"] == message





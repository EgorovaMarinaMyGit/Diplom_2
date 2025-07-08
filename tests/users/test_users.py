import allure
import pytest
from methods.users_methods import UsersMethods
from data import USER_DATA_NO_NAME, USER_DATA_NO_EMAIL, USER_DATA_NO_PASSWORD

class TestUser:

    @allure.title("Успешное создание пользователя")
    def test_create_user_passed(self, create_and_delete_user):
        user = create_and_delete_user
        assert user['status_code'] == 200 and user['success'] == True
    

    @allure.title("Создание двух одинаковых пользователей")
    def test_create_users_with_the_same_data(self, create_and_delete_user):
        user = create_and_delete_user
        second_user_data = {
            "name": user['name'],
            "email": user['email'],
            "password": user['password']  
        }
        user = UsersMethods()
        response, status_code = user.create_user(second_user_data)
        message = "User already exists"
        assert status_code == 403 and response["message"] == message


    @allure.title("Создание пользователя без обязательного поля")
    @pytest.mark.parametrize(
        'params', 
        [
            USER_DATA_NO_NAME,
            USER_DATA_NO_EMAIL,
            USER_DATA_NO_PASSWORD
        ]
    )
    def test_create_user_without_any_field(self, create_user_no_any_data, params):
        user = create_user_no_any_data
        message = "Email, password and name are required fields"
        assert user['status_code'] == 403 and user['response_json'].get("message") == message


    @allure.title("Авторизация существующего пользователя")
    def test_autorisation_user_success(self, create_and_delete_user):
        user = create_and_delete_user
        user_data = {
            "email": user['email'],
            "password": user['password']  
        }
        user = UsersMethods()
        response, status_code = user.user_login(user_data)
        assert status_code == 200 and response["success"] == True


    @allure.title("Авторизация с неправильным email")
    def test_autorisation_user_incorrect_email(self, create_and_delete_user):
        user = create_and_delete_user
        user_data = {
            "email": "qwedsa@mail.ru",
            "password": user['password']  
        }
        user = UsersMethods()
        response, status_code = user.user_login(user_data)
        message = "email or password are incorrect"
        assert status_code == 401 and response["message"] == message


    @allure.title("Авторизация с неправильным паролем")
    def test_autorisation_user_incorrect_password(self, create_and_delete_user):
        user = create_and_delete_user
        user_data = {
            "email": user['email'],
            "password": "jhs65d6uzc" 
        }
        user = UsersMethods()
        response, status_code = user.user_login(user_data)
        message = "email or password are incorrect"
        assert status_code == 401 and response["message"] == message


    @allure.title("Изменение имени пользователя с авторизацией")
    def test_change_user_name_with_autorisation(self, create_and_delete_user):
        user = create_and_delete_user
        headers = {
            'Authorization': user['access_token'] 
        }
        params = {
            "email": user['email'],
            "name": "Qwertyu" 
        }
        user = UsersMethods()
        response, status_code, data = user.change_user_data(headers, params)
        assert status_code == 200 and response["user"]["name"] == "Qwertyu"


    @allure.title("Изменение email пользователя с авторизацией")
    def test_change_user_email_with_autorisation(self, create_and_delete_user):
        user = create_and_delete_user
        headers = {
            'Authorization': user['access_token'] 
        }
        params = {
            "email": "fgsf653tgss@mail.ru",
            "name": user['name'] 
        }
        user = UsersMethods()
        response, status_code, data = user.change_user_data(headers, params)
        assert status_code == 200 and response["user"]["email"] == "fgsf653tgss@mail.ru"


    @allure.title("Изменение имени пользователя без авторизации")
    def test_change_user_name_without_autorisation(self, create_and_delete_user):
        user = create_and_delete_user
        headers = None
        params = {
            "email": user['email'],
            "name": "Qwertyu" 
        }
        user = UsersMethods()
        response, status_code, user_data = user.change_user_data(headers, params)
        message = "You should be authorised"
        assert status_code == 401 and response["message"] == message


    @allure.title("Изменение email пользователя без авторизации")
    def test_change_user_email_without_autorisation(self, create_and_delete_user):
        user = create_and_delete_user
        headers = None
        params = {
            "email": "76573shbczc@mail.ru",
            "name": user['name'] 
        }
        user = UsersMethods()
        response, status_code, user_data = user.change_user_data(headers, params)
        message = "You should be authorised"
        assert status_code == 401 and response["message"] == message

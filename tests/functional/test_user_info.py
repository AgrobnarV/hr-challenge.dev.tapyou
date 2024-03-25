import allure
import pytest
import requests


@allure.feature("Запрос информации о пользователе")
@allure.story("Карточка пользователя")
class TestUserInfo:

    @pytest.fixture(scope="class")
    def base_url(self):
        return "https://hr-challenge.dev.tapyou.com/api/test/user"

    @allure.title("Успешный запрос информации о существующем пользователе")
    @allure.description("Тест проверяет, что API корректно возвращает информацию о пользователе с ID 10")
    @allure.severity("Severity.HIGH")
    def test_success_user_id(self, base_url):
        response = requests.get(f"{base_url}/10")
        data = response.json()

        assert response.status_code == 200
        assert "user" in data, "возвращаемый JSON объект не содержит информацию о пользователе"
        user_info = data["user"]
        assert user_info["id"] == 10
        assert "name" in user_info
        assert "gender" in user_info
        assert "age" in user_info
        assert "city" in user_info
        assert "registrationDate" in user_info

    @allure.title("Пользователь с корректным id которого нет в базе")
    @allure.description("Тест проверяет, что API корректно обрабатывает запрос с несуществующим ID и выдает 500")
    @allure.severity("Severity.MINOR")
    def test_invalid_user_id(self, base_url):
        response = requests.get(f"{base_url}/0")
        data = response.json()

        assert response.status_code == 500
        assert data["status"] == 500
        assert data["error"] == "Internal Server Error"
        assert data["message"] == "No message available"
        assert data["path"] == "/api/test/user/0"

    @allure.title("Несуществующий пользователь")
    @allure.description("Тест проверяет, что API корректно обрабатывает запрос с несуществующим ID и выдает 400")
    @allure.severity("Severity.MINOR")
    def test_empty_user_id(self, base_url):
        response = requests.get(f"{base_url}/test")
        data = response.json()

        assert response.status_code == 400
        assert data["errorCode"] == 400
        assert data["errorMessage"] == "NumberFormatException: For input string: \"test\""
        assert data["user"] is None

    @allure.title("Пользователь с пустым ID")
    @allure.description("Тест проверяет, что API корректно обрабатывает запрос с пустым ID")
    @allure.severity("Severity.MINOR")
    def test_unknown_user_id(self, base_url):
        response = requests.get(f"{base_url}/")
        data = response.json()

        assert response.status_code == 404
        assert data["status"] == 404
        assert data["error"] == "Not Found"
        assert data["message"] == "No message available"
        assert data["path"] == "/api/test/user/"

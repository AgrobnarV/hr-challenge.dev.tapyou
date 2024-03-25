import allure
import pytest
import requests

API_BASE_URL = "https://hr-challenge.dev.tapyou.com/api/test"


@pytest.fixture
def api_response(request):
    endpoint = request.param['endpoint']
    params = request.param.get('params', None)
    return requests.get(API_BASE_URL + endpoint, params=params).json()


@allure.feature("Запрос списка идентификаторов пользователей по указанному критерию")
@allure.story("Список пользователей")
@allure.title("Успешный запрос списка пользователей")
@allure.description("Тест проверяет, что API корректно возвращает список ID пользователей")
@allure.severity("Severity.HIGH")
@pytest.mark.parametrize("api_response", [
    {"endpoint": "/users", "params": {"gender": "male"}},
    {"endpoint": "/users", "params": {"gender": "female"}}
], indirect=True)
def test_user_list_request(api_response):
    assert api_response["isSuccess"] is True
    assert api_response["errorCode"] == 0
    assert api_response["errorMessage"] is None
    assert "idList" in api_response
    assert isinstance(api_response["idList"], list)


@allure.title("Некорректный параметр пола")
@allure.description("Тест проверяет, что API корректно обрабатывает запрос с некорректным параметром пола")
@allure.severity("Severity.NORMAL")
@pytest.mark.parametrize("api_response", [
    {"endpoint": "/users", "params": {"gender": "12"}},
    {"endpoint": "/users", "params": {"gender": "test"}}
], indirect=True)
def test_invalid_gender(api_response):
    assert api_response["status"] == 500
    assert api_response["error"] == "Internal Server Error"
    assert api_response["message"] is not None
    assert api_response["path"] == "/api/test/users"


@allure.title("Пустой параметр пола")
@allure.description("Тест проверяет, что API корректно обрабатывает запрос с пустым параметром пола")
@allure.severity("Severity.MINOR")
@pytest.mark.parametrize("api_response", [
    {"endpoint": "/users", "params": {"gender": "12"}},
    {"endpoint": "/users", "params": {"gender": "test"}}
], indirect=True)
def test_empty_gender(api_response):
    assert api_response["status"] == 500
    assert api_response["error"] == "Internal Server Error"
    assert api_response["message"] is not None
    assert api_response["path"] == "/api/test/users"

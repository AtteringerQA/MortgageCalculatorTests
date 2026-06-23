import pytest
from requests import Session

from config.constants import (
    JSON_HEADERS,
    HTTP_OK,
    HTTP_BAD_REQUEST,
    HTTP_UNAUTHORIZED,
    status_error_message,
)
from helpers.file_helpers import load_yaml
from jsonschema import validate


class TestMortgageProgAPI:

    @pytest.mark.positive
    def test__get_mortgage_prog_api(self, api_session: Session, mortgage_prog_url: str):
        """Позитивный тест: проверка кода 200 и схемы ответа."""
        response = api_session.get(mortgage_prog_url)
        assert response.status_code == HTTP_OK, status_error_message(HTTP_OK, response.status_code)
        body = response.json()

        schema = load_yaml("mortgage_prog.yml")
        validate(body, schema)

    @pytest.mark.negative
    def test__get_mortgage_prog_api_without_auth(self, mortgage_prog_url: str):
        """Негативный тест 1: запрос без токена авторизации (401)."""
        session_without_auth = Session()
        session_without_auth.headers.update(JSON_HEADERS)

        response = session_without_auth.get(mortgage_prog_url)

        assert response.status_code == HTTP_UNAUTHORIZED, status_error_message(
            HTTP_UNAUTHORIZED, response.status_code
        )

    @pytest.mark.negative
    def test__get_mortgage_prog_api_with_invalid_filter(
        self, api_session: Session, mortgage_prog_url: str
    ):
        """Негативный тест 2: невалидное значение FilterList (400)."""
        params = {"FilterList": "Tranches"}
        response = api_session.get(mortgage_prog_url, params=params)

        assert response.status_code == HTTP_BAD_REQUEST, status_error_message(
            HTTP_BAD_REQUEST, response.status_code
        )

        body = response.json()
        assert "errors" in body, "В ответе отсутствует ключ 'errors'"
        assert "FilterList" in body["errors"], "В errors отсутствует ключ 'FilterList'"

        error_messages = body["errors"]["FilterList"]
        assert any("Tranches" in msg for msg in error_messages), (
            f"В сообщении об ошибке не найдено упоминание 'Tranches'. "
            f"Получено: {error_messages}"
        )
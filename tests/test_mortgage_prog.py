import pytest
from config.api_config import STAGE_URL
from requests import Session
from helpers.file_helpers import load_yaml
from jsonschema import validate


class TestMortgageProgAPI:
    URL = STAGE_URL + "/v2/mortgage-prog"

    @pytest.mark.positive
    def test__get_mortgage_prog_api(self, api_session: Session):
        """Позитивный тест: проверка кода 200 и схемы ответа."""
        response = api_session.get(self.URL)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        body = response.json()

        schema = load_yaml("mortgage_prog.yml")
        validate(body, schema)

    @pytest.mark.negative
    def test__get_mortgage_prog_api_without_auth(self):
        """Негативный тест 1: запрос без токена авторизации (401)."""
        session_without_auth = Session()
        session_without_auth.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        response = session_without_auth.get(self.URL)

        assert response.status_code == 401, \
            f"Ожидался код 401 (Unauthorized), получен {response.status_code}"

    @pytest.mark.negative
    def test__get_mortgage_prog_api_with_invalid_filter(self, api_session: Session):
        """Негативный тест 2: невалидное значение FilterList (400)."""
        params = {"FilterList": "Tranches"}
        response = api_session.get(self.URL, params=params)

        assert response.status_code == 400, \
            f"Ожидался код 400 (Bad Request), получен {response.status_code}"

        body = response.json()
        assert "errors" in body, "В ответе отсутствует ключ 'errors'"
        assert "FilterList" in body["errors"], "В errors отсутствует ключ 'FilterList'"

        error_messages = body["errors"]["FilterList"]
        assert any("Tranches" in msg for msg in error_messages), \
            f"В сообщении об ошибке не найдено упоминание 'Tranches'. Получено: {error_messages}"

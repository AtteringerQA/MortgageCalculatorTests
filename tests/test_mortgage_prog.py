from config.api_config import STAGE_URL
from requests import Session
from helpers.file_helpers import load_yaml
from jsonschema import validate


class TestMortgageProgAPI:
    URL = STAGE_URL + "/v2/mortgage-prog"

    def test__get_mortgage_prog_api(self, api_session: Session):
        # 1. Запрос без параметров
        response = api_session.get(self.URL)
        assert response.status_code == 200, f"Ожидался код 200, получен {response.status_code}"
        body = response.json()

        # 2. Проверка по JSON-схеме из YAML-файла
        schema = load_yaml("mortgage_prog.yml")
        validate(body, schema)

    def test__get_mortgage_prog_api_without_auth(self):
        """
        Негативный тест: запрос без токена авторизации.
        Ожидаем 401 Unauthorized.
        """
        session_without_auth = Session()
        session_without_auth.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

        response = session_without_auth.get(self.URL)

        assert response.status_code == 401, \
            f"Ожидался код 401 (Unauthorized), получен {response.status_code}"

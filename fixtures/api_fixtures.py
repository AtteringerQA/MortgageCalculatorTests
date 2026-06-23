import pytest
import requests
from config.api_config import STAGE_URL, ARM_TOKEN
from config.constants import JSON_HEADERS


@pytest.fixture(scope="session")
def base_url() -> str:
    """Базовый URL API v2."""
    return f"{STAGE_URL}/v2"


@pytest.fixture(scope="session")
def mortgage_prog_url(base_url: str) -> str:
    """URL эндпоинта /mortgage-prog."""
    return f"{base_url}/mortgage-prog"


@pytest.fixture(scope="session")
def api_session():
    """Фикстура создаёт HTTP-сессию с Bearer-токеном."""
    if not ARM_TOKEN:
        pytest.fail(
            "ARM_TOKEN не найден в .env файле. "
            "Создай .env в корне проекта и добавь туда ARM_TOKEN=..."
        )

    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {ARM_TOKEN}",
        **JSON_HEADERS,
    })
    yield session
    session.close()

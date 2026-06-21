
import pytest
import requests
from config.api_config import STAGE_URL, ARM_TOKEN

@pytest.fixture(scope="session")
def api_session():
    """Фикстура создает HTTP-сессию с Bearer токеном."""
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {ARM_TOKEN}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    })
    yield session

@pytest.fixture(scope="session")
def base_url():
    """Фикстура возвращает базовый URL."""
    return f"{STAGE_URL}/v2"
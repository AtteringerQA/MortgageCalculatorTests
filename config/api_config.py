import os
from dotenv import load_dotenv

# Загружаем переменные из .env файла
load_dotenv()

# Читаем переменные окружения
STAGE_URL = "https://stage.mortgage.fsk-tech.ru"
ARM_TOKEN = os.getenv("ARM_TOKEN")

# Проверка что токен загружен
if not ARM_TOKEN:
    raise ValueError("ARM_TOKEN не найден в .env файле")

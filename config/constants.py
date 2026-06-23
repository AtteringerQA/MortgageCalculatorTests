# config/constants.py
from http import HTTPStatus


# ─── HTTP Headers ──────────────────────────────────────────────────────
JSON_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}


# ─── HTTP Status Codes ─────────────────────────────────────────────────
HTTP_OK = HTTPStatus.OK                    # 200
HTTP_BAD_REQUEST = HTTPStatus.BAD_REQUEST  # 400
HTTP_UNAUTHORIZED = HTTPStatus.UNAUTHORIZED  # 401


# ─── Сообщения об ошибках ──────────────────────────────────────────────
def status_error_message(expected: int, actual: int) -> str:
    """
    Формирует сообщение об ошибке для assert по статус-коду.
    """
    return f"Ожидался код {expected}, получен {actual}"